# src/agent.py
import json
import operator
from typing import Annotated, Sequence, TypedDict, Literal, Optional, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src.dependencies import get_current_llm
from src.tools import tools
from src.config import config
from src.trace import get_trace

# ---------------------------------------------------------------------------
# 1. State Definition
# ---------------------------------------------------------------------------
# ToolPlan is the structured output of the planner node. It tells the executor
# exactly which tool calls to make — no more, no less.
class ToolPlan(TypedDict):
    api_class: str          # e.g., "CUSTOMERS"
    version: Optional[str]  # e.g., "v1", "v2", or None for latest
    query: str              # The semantic search query to use

class QueryTracker(TypedDict):
    """Tracks each sub-query through the pipeline with its status and result."""
    api_class: str          # e.g., "CUSTOMERS", "INVOICES"
    version: Optional[str]  # e.g., "v1", "v2", or None
    query: str              # The semantic search query
    status: str             # "pending" | "covered" | "not_found" | "unavailable" | "budget_exceeded"
    reason: Optional[str]   # Why unavailable/not_found/budget_exceeded

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Replaces step_count. Tracks individual tool calls across ALL turns.
    tool_call_budget: int
    # The structured plan produced by the planner, consumed by the executor.
    tool_plan: Optional[List[ToolPlan]]
    # Whether the planner determined it needs clarification from the user.
    needs_clarification: bool
    rephrase_count: int
    # Intent classification: "new_intent" or "follow_up"
    # Used for automatic session management
    intent_type: Optional[str]
    # Structured tracking of each sub-query and its result through the pipeline
    query_tracker: Optional[List[QueryTracker]]
    # Restructurer analysis text — injected only into synthesizer, not into messages
    restructurer_analysis: Optional[str]
    # Accumulated operation log for context-aware multi-turn planning.
    # Each entry records what was searched in a given turn so the planner
    # can intelligently handle "do the same for X" patterns.
    conversation_context: Optional[List[dict]]
    # Active scope: tracks which API class(es) and version(s) are currently
    # being discussed. Updated deterministically after each turn from the
    # query_tracker. The planner reads this on follow-ups to preserve the
    # version structure (e.g., v1+v2 comparison context).
    # Shape: {"api_classes": ["CUSTOMERS"], "versions": ["v1", "v2"]}
    active_scope: Optional[dict]

# ---------------------------------------------------------------------------
# 2. LLM Initialization (per-request via context variable)
# ---------------------------------------------------------------------------
# The LLM is now fetched per-request to support user-provided API keys.
# Use get_llm_plain() and get_llm_with_tools() in node functions.

def get_llm_plain():
    """Get the current request's LLM without tools bound (for planning/synthesis)."""
    return get_current_llm()

def get_llm_with_tools_bound():
    """Get the current request's LLM with tools bound (for executor)."""
    return get_current_llm().bind_tools(tools)

tool_node = ToolNode(tools)

# ---------------------------------------------------------------------------
# 3. Helper: Read config values
# ---------------------------------------------------------------------------
def _cfg(path: str, default):
    """Dot-path config reader, e.g., 'agent.max_tool_calls'."""
    parts = path.split(".")
    node = config
    for p in parts:
        if not isinstance(node, dict):
            return default
        node = node.get(p, {})
    return node if node != {} else default

MAX_TOOL_CALLS   = _cfg("agent.max_tool_calls", 6)      # Hard limit on total individual tool invocations
MAX_REPHRASE     = _cfg("agent.max_rephrase_attempts", 1)
MAX_CONTEXT_TURNS = _cfg("agent.max_context_turns", 10)  # Max operation-log turns injected into planner
KNOWN_API_CLASSES = _cfg("agent.known_api_classes",
    ["ACCOUNTS", "CUSTOMERS", "PAYMENT_INTENTS", "TRANSFERS",
     "SUBSCRIPTIONS", "PRODUCTS", "REFUNDS", "PRICES"])

# ---------------------------------------------------------------------------
# 4. Planner Node
# ---------------------------------------------------------------------------
# The planner's job is to parse user intent ONCE and produce a minimal,
# structured list of tool calls. The executor then follows this plan exactly.
# This is the primary defense against synonym spam: the plan constrains
# what the executor is allowed to search for.

_PLANNER_SYSTEM = f"""You are a query planner for a Stripe API documentation assistant.

Your job is to analyze the user's question and produce a minimal execution plan.

Known API classes: {", ".join(KNOWN_API_CLASSES)}
Known versions: v1, v2

Output a JSON object with this schema:
{{
  "intent_type": "follow_up",
  "needs_clarification": false,
  "clarification_question": null,
  "plan": [
    {{
      "api_class": "CUSTOMERS",
      "version": "v1",
      "query": "create a customer payload and required fields"
    }}
  ]
}}

Intent Classification:
- "new_intent": The query is about a completely different topic/API than previous conversation
- "follow_up": The query continues or relates to the previous conversation topic
- For the FIRST message in a conversation (no history), always use "new_intent"

Examples:
  Previous: "How to create a customer?"
  Current: "What about updating it?" → "follow_up" (same topic: customers)
  
  Previous: "Show me customer creation"
  Current: "How do I create a payment intent?" → "new_intent" (different API)
  
  Previous: "Compare customers v1 vs v2"
  Current: "What are the main differences?" → "follow_up" (continuing comparison)
  
  Previous: "Difference between v1 and v2 for creating customers and products?"
  Current: "do the same for prices api" → "follow_up" (replicate comparison structure)
    ↳ Plan should have: [{{api_class: "PRICES", version: "v1", ...}}, {{api_class: "PRICES", version: "v2", ...}}]

Pattern Recognition:
- Phrases like "do the same for X", "also for X", "what about X" indicate follow-up
- When follow-up references a different API, inherit the structure (e.g., version comparison) from previous query
- If previous query compared v1 vs v2, the follow-up should generate separate plan items for v1 and v2

Using ACTIVE SCOPE (if present):
The ACTIVE SCOPE tells you which API class(es) and version(s) are currently being discussed.
Example: {{"api_classes": ["CUSTOMERS"], "versions": ["v1", "v2"]}}

CRITICAL rules for follow-up queries:
1. If the user asks a follow-up WITHOUT explicitly mentioning an API class or version,
   generate plan items for EVERY combination of (api_class, version) in the active scope.
   Example: scope has CUSTOMERS with [v1, v2], user asks "what about address fields?"
   → Plan MUST have 2 items: CUSTOMERS v1 address fields + CUSTOMERS v2 address fields.
2. If the user explicitly narrows the version ("just v1", "only v2"), produce plan items
   for only that version. The scope will be updated automatically after execution.
3. If the user adds a version ("also check v2"), add plan items for the new version
   alongside existing ones.
4. If the user switches to a different API ("do the same for SUBSCRIPTIONS"), apply the
   same version structure to the new API class.
5. A null or absent version in scope means "latest" (no version comparison active).

Using the CONVERSATION OPERATION LOG (if present):
The operation log is a structured record of every turn in the session: the user's query
and the exact operations (api_class, version, query, status) that were executed.
When the user says "do the same for X", "repeat for X", "also for X but for Y":
1. Look at ALL operations in the log that targeted the original API class.
2. Replicate each operation for the new API class X, preserving versions and query topics.
3. If too many operations would exceed the tool call budget (max {MAX_TOOL_CALLS}), combine
   related queries into broader searches (e.g., merge "address fields" + "error codes" into one query).
4. Always preserve the version structure: if v1 + v2 were queried, query v1 + v2 for X.

Rules:
1. If the query is ambiguous across API classes and cannot be resolved by context, set
   needs_clarification=true and provide clarification_question. Do NOT produce a plan.
2. Each plan item maps to EXACTLY ONE tool call. Do not add synonym alternatives.
3. For cross-version comparisons, produce one item per version (max 2).
4. For multi-entity queries, produce one item per distinct entity.
5. If no version is specified, set version to null — the tool resolves "latest" automatically.
6. Keep queries semantic and concise (under 12 words).
7. Produce the minimum number of plan items necessary. For a single-entity single-version
   query, the plan MUST have exactly 1 item.
8. CRITICAL - API Class Validation: You MUST ONLY use API classes from the known list above.
   The known list is: {", ".join(KNOWN_API_CLASSES)}
   
   FORBIDDEN: Do NOT use any API class that is not explicitly in this list.
   - ✓ CORRECT: "products" → PRODUCTS (in list)
   - ✓ CORRECT: "prices api" → PRICES (in list) 
   - ✗ WRONG: "invoices" → INVOICES (NOT in list - use UNKNOWN instead)
   - ✗ WRONG: "balances" → BALANCES (NOT in list - use UNKNOWN instead)
   
   If user mentions an API not in the known list, set api_class to "UNKNOWN".

Respond ONLY with the JSON object. No explanation."""

def planner_node(state: AgentState) -> dict:
    """
    Analyzes the user's latest message and produces a structured retrieval plan.
    This runs once per user turn, before any tool calls.
    
    Context-aware: Uses conversation history to understand follow-up questions
    and clarifications.
    """
    trace = get_trace()
    if trace:
        trace.start_node("planner", {"description": "Analyzing query and building retrieval plan"})

    # Find the last human message
    user_message = next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        None
    )
    if not user_message:
        if trace:
            trace.end_node("planner", {"result": "no_user_message"})
        return {"tool_plan": [], "needs_clarification": False, "intent_type": "new_intent"}

    print("\n[Planner] Analyzing query and building plan...")
    
    # Build context-aware prompt
    # Include previous conversation for context (especially for clarifications/follow-ups)
    messages = state.get("messages", [])
    
    # Inject active scope and operation log if available
    planner_system_content = _PLANNER_SYSTEM
    active_scope = state.get("active_scope")
    if active_scope:
        scope_json = json.dumps(active_scope)
        planner_system_content += f"\n\nACTIVE SCOPE:\n{scope_json}"
        print(f"[Planner] Active scope: {scope_json}")

    conv_context = state.get("conversation_context") or []
    if conv_context:
        # Trim to most recent N turns to avoid blowing up the context window
        trimmed = conv_context[-MAX_CONTEXT_TURNS:]
        context_json = json.dumps(trimmed, indent=2)
        planner_system_content += f"\n\nCONVERSATION OPERATION LOG (last {len(trimmed)} of {len(conv_context)} turns):\n{context_json}"
        print(f"[Planner] Injecting operation log ({len(trimmed)}/{len(conv_context)} turn(s), max={MAX_CONTEXT_TURNS})")
    
    if len(messages) > 1:
        # Multi-turn conversation: include recent history for context
        print(f"[Planner] Using conversation context ({len(messages)} total messages)")
        # Take last N messages for context (excluding the current one we're planning for)
        context_messages = messages[:-1][-10:]  # Last 10 messages for context
        
        # Build prompt with history
        prompt_messages = [SystemMessage(content=planner_system_content)]
        prompt_messages.extend(context_messages)
        prompt_messages.append(HumanMessage(content=user_message.content))
    else:
        # First turn: no conversation history
        prompt_messages = [
            SystemMessage(content=planner_system_content),
            HumanMessage(content=user_message.content)
        ]

    response = get_llm_plain().invoke(prompt_messages)

    try:
        # Log the raw response for debugging
        print(f"[Planner DEBUG] Raw LLM response type: {type(response)}")
        print(f"[Planner DEBUG] Raw LLM response content: '{response.content[:200] if response.content else 'EMPTY'}'")
        
        if not response.content or not response.content.strip():
            print("[Planner] ERROR: LLM returned empty response. Falling back to free-form agent.")
            return {"needs_clarification": False, "tool_plan": [], "intent_type": "new_intent"}
        
        # Strip markdown fences if the model added them
        raw = response.content.strip()
        # Remove various markdown code fence formats
        if raw.startswith("```"):
            # Remove opening fence with optional language specifier
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw.rsplit("\n", 1)[0] if "\n" in raw else raw[:-3]
        raw = raw.strip()
        
        print(f"[Planner DEBUG] Cleaned JSON string: '{raw[:200]}'")
        
        plan_data = json.loads(raw)
        
        # Extract intent type (default to "new_intent" if not provided)
        intent_type = plan_data.get("intent_type", "new_intent")
        print(f"[Planner] Intent classification: {intent_type}")

        if plan_data.get("needs_clarification"):
            q = plan_data.get("clarification_question", "Could you clarify your request?")
            print(f"[Planner] Ambiguous query. Asking for clarification: {q}")
            if trace:
                trace.end_node("planner", {
                    "result": "needs_clarification",
                    "intent_type": intent_type,
                    "clarification_question": q
                })
            return {
                "needs_clarification": True,
                "tool_plan": [],
                "intent_type": intent_type,
                "messages": [AIMessage(content=q)]
            }

        plan: List[ToolPlan] = plan_data.get("plan", [])
        
        # Build query tracker and separate valid/invalid plan items
        query_tracker: List[QueryTracker] = []
        valid_plan = []
        known_str = ", ".join(KNOWN_API_CLASSES)
        
        for item in plan:
            api_class = item.get('api_class', '').upper()
            version = item.get('version')
            query = item.get('query', '')
            
            if api_class == "UNKNOWN":
                # Explicitly unknown - track as unavailable, no tool call
                query_tracker.append({
                    "api_class": api_class,
                    "version": version,
                    "query": query,
                    "status": "unavailable",
                    "reason": f"API class not recognized. Available: {known_str}"
                })
                print(f"[Planner] Skipped UNKNOWN: query='{query}'")
            elif api_class and api_class not in KNOWN_API_CLASSES:
                # LLM hallucinated a class not in our list - track as unavailable
                query_tracker.append({
                    "api_class": api_class,
                    "version": version,
                    "query": query,
                    "status": "unavailable",
                    "reason": f"{api_class} is not available in this system. Available: {known_str}"
                })
                print(f"[Planner] Skipped unavailable: {api_class}")
            else:
                # Valid - will be executed
                query_tracker.append({
                    "api_class": api_class,
                    "version": version,
                    "query": query,
                    "status": "pending",
                    "reason": None
                })
                valid_plan.append(item)
        
        # If ALL items were unavailable, inform the user
        if not valid_plan and query_tracker:
            unavailable_summary = "; ".join(
                f"{t['api_class']}: {t['reason']}" for t in query_tracker
            )
            print(f"[Planner] No valid API classes in plan. Informing user.")
            if trace:
                trace.end_node("planner", {
                    "result": "all_unavailable",
                    "intent_type": intent_type,
                    "query_tracker": query_tracker
                })
            return {
                "needs_clarification": True,
                "tool_plan": [],
                "query_tracker": query_tracker,
                "intent_type": intent_type,
                "messages": [AIMessage(content=f"Sorry, none of the requested APIs are available. {unavailable_summary}")]
            }
        
        print(f"[Planner] Plan produced ({len(valid_plan)} tool call(s), {len(query_tracker) - len(valid_plan)} unavailable):")
        for t in query_tracker:
            status_icon = "→" if t['status'] == 'pending' else "✗"
            print(f"  {status_icon} {t['api_class']} | version={t['version']} | query='{t['query']}' | status={t['status']}")
        
        if trace:
            trace.end_node("planner", {
                "result": "plan_ready",
                "intent_type": intent_type,
                "plan_size": len(valid_plan),
                "unavailable_count": len(query_tracker) - len(valid_plan),
                "plan": valid_plan,
                "query_tracker": query_tracker
            })

        return {
            "needs_clarification": False,
            "tool_plan": valid_plan,
            "query_tracker": query_tracker,
            "intent_type": intent_type
        }

    except (json.JSONDecodeError, KeyError) as e:
        print(f"[Planner] Failed to parse plan: {e}. Falling back to free-form agent.")
        print(f"[Planner] DEBUG: Response content was: {response.content if response.content else 'EMPTY'}")
        if trace:
            trace.end_node("planner", {"result": "parse_error", "error": str(e)})
        return {"needs_clarification": False, "tool_plan": [], "intent_type": "new_intent"}


# ---------------------------------------------------------------------------
# 5. Budget Checker Node
# ---------------------------------------------------------------------------
# Sits between planner and executor. Checks if the plan exceeds the tool call
# budget BEFORE execution begins. If it does, asks the user to break down
# their query into smaller parts rather than silently truncating.

def budget_checker_node(state: AgentState) -> dict:
    """
    Validates that the planned tool calls fit within the budget.
    """
    trace = get_trace()
    plan = state.get("tool_plan", []) or []
    current_budget = state.get("tool_call_budget", 0)
    calls_remaining = MAX_TOOL_CALLS - current_budget
    plan_size = len(plan)

    if trace:
        trace.start_node("budget_checker", {
            "plan_size": plan_size,
            "current_budget": current_budget,
            "calls_remaining": calls_remaining,
            "max_tool_calls": MAX_TOOL_CALLS
        })

    if plan_size <= calls_remaining:
        # Plan fits within budget — pass through
        print(f"[Budget Checker] Plan ({plan_size} calls) fits within budget ({calls_remaining} remaining). Proceeding.")
        if trace:
            trace.end_node("budget_checker", {"result": "within_budget", "plan_size": plan_size, "calls_remaining": calls_remaining})
        return {}

    # --- Plan exceeds budget ---

    # RETRY PATH: we already have partial results from prior tool calls.
    # Don't discard them by asking the user to start over — instead,
    # execute what still fits and mark the rest as budget_exceeded.
    if current_budget > 0:
        executable_plan = plan[:calls_remaining] if calls_remaining > 0 else []
        overflow_plan = plan[calls_remaining:] if calls_remaining > 0 else plan

        overflow_keys = {(p['api_class'].upper(), p.get('version')) for p in overflow_plan}
        tracker = state.get("query_tracker") or []
        updated_tracker = []
        for entry in tracker:
            key = (entry['api_class'].upper(), entry.get('version'))
            if key in overflow_keys and entry['status'] == 'pending':
                updated_entry = dict(entry)
                updated_entry['status'] = 'budget_exceeded'
                updated_entry['reason'] = (
                    f"Tool call budget ({MAX_TOOL_CALLS}) exhausted. "
                    f"Only {calls_remaining} call(s) remaining in this session. "
                    "Try asking about this API in a follow-up message."
                )
                updated_tracker.append(updated_entry)
                overflow_keys.discard(key)
            else:
                updated_tracker.append(entry)

        skipped_apis = [f"{p['api_class']} {p.get('version') or 'latest'}" for p in overflow_plan]
        print(f"[Budget Checker] Retry path: {plan_size} item(s) planned, {calls_remaining} remaining. "
              f"Executing {len(executable_plan)}, marking {len(overflow_plan)} as budget_exceeded: {', '.join(skipped_apis)}")

        if trace:
            trace.end_node("budget_checker", {
                "result": "retry_truncated",
                "executable": len(executable_plan),
                "overflow": len(overflow_plan),
                "skipped_apis": skipped_apis
            })

        return {
            "tool_plan": executable_plan,
            "query_tracker": updated_tracker,
        }

    # FRESH REQUEST: no prior results — ask user to break it down
    api_list = []
    for p in plan:
        cls = p.get('api_class', '')
        if cls not in api_list:
            api_list.append(cls)

    # Suggest logical batches
    batch_size = max(1, calls_remaining)  # Use current remaining as batch hint
    batches = [api_list[i:i + batch_size] for i in range(0, len(api_list), batch_size)]
    batch_suggestions = "\n".join(
        f"  - {', '.join(batch)}" for batch in batches
    )

    clarification_msg = (
        f"Your query requires **{plan_size} lookups** but the system can process "
        f"a maximum of **{MAX_TOOL_CALLS}** per request (with {calls_remaining} remaining in this session). "
        f"Could you break your question into smaller parts? For example:\n"
        f"{batch_suggestions}\n\n"
        f"You can ask about each group in a separate message and I'll cover them all."
    )

    print(f"[Budget Checker] Plan ({plan_size} calls) exceeds budget ({calls_remaining} remaining). Asking user to narrow query.")
    print(f"[Budget Checker] APIs in plan: {', '.join(api_list)}")

    if trace:
        trace.end_node("budget_checker", {
            "result": "over_budget_fresh",
            "plan_size": plan_size,
            "calls_remaining": calls_remaining,
            "apis": api_list
        })

    return {
        "needs_clarification": True,
        "messages": [AIMessage(content=clarification_msg)],
    }


def route_after_budget_checker(state: AgentState) -> Literal["executor", "restructurer", "__end__"]:
    """Routes after budget check:
    - Over budget on fresh request → __end__ (clarification)
    - Over budget on retry with nothing left to execute → restructurer (show partial results)
    - Within budget or truncated with items left → executor
    """
    if state.get("needs_clarification"):
        return "__end__"
    plan = state.get("tool_plan", []) or []
    if plan:
        return "executor"
    # No executable plan remaining — budget exhausted on retry path.
    # Go to restructurer so partial results are still presented.
    return "restructurer"


# ---------------------------------------------------------------------------
# 6. Executor (Agent) Node
# ---------------------------------------------------------------------------
# The executor is now "plan-aware". Instead of letting the LLM decide what to
# search for, it injects the plan as a hard constraint. The LLM's only job here
# is to translate the plan into the correct tool call arguments and fire them.

_EXECUTOR_SYSTEM = """You are a precise Stripe API documentation retrieval executor.

You have been given a retrieval plan. Execute it by calling the search_stripe_api_docs
tool for EACH item in the plan — no more, no fewer.

Rules:
- ONLY make tool calls listed in the plan below. Do NOT make any calls for APIs not in the plan.
- Use the exact api_class, version, and query from the plan. Do not improvise alternatives.
- Call all planned tool calls in parallel if there are multiple items.
- If the user's question mentions APIs not in the plan, IGNORE them — the planner already 
  filtered those out because they are unavailable.
- After all tool calls complete, do NOT call any more tools.
- If a tool returns "No documentation found," note it; do not retry."""

def executor_node(state: AgentState) -> dict:
    """
    Executes the retrieval plan. Enforces the tool call budget.
    Only makes tool calls that are in the plan — nothing extra.
    """
    trace = get_trace()
    current_budget = state.get("tool_call_budget", 0)
    plan = state.get("tool_plan", [])

    if trace:
        trace.start_node("executor", {
            "current_budget": current_budget,
            "plan_size": len(plan) if plan else 0,
            "max_tool_calls": MAX_TOOL_CALLS
        })

    # --- Budget Enforcement ---
    calls_remaining = MAX_TOOL_CALLS - current_budget
    if calls_remaining <= 0:
        print(f"\n[Executor] Tool call budget exhausted ({current_budget}/{MAX_TOOL_CALLS}). Proceeding to synthesis.")
        # Mark any remaining pending items as budget_exceeded
        tracker = state.get("query_tracker") or []
        updated_tracker = []
        for entry in tracker:
            if entry["status"] == "pending":
                updated_entry = dict(entry)
                updated_entry["status"] = "budget_exceeded"
                updated_entry["reason"] = (
                    f"Tool call budget ({MAX_TOOL_CALLS}) exhausted during execution. "
                    "Try asking about this API in a follow-up message."
                )
                updated_tracker.append(updated_entry)
                print(f"[Executor] Budget exceeded for: {entry['api_class']} {entry.get('version') or 'latest'}")
            else:
                updated_tracker.append(entry)
        return {
            "messages": [SystemMessage(content="SYSTEM: Tool call budget exhausted. Proceed with available data.")],
            "tool_plan": [],
            "query_tracker": updated_tracker if updated_tracker else None,
        }

    # --- Runtime budget overflow ---
    # The budget_checker_node validates the initial plan, but retries via
    # query_expander can consume extra budget slots. If the remaining plan
    # now exceeds what's left, truncate and mark overflow as budget_exceeded.
    _overflow_tracker = None
    if plan and len(plan) > calls_remaining:
        executable_plan = plan[:calls_remaining]
        overflow_plan = plan[calls_remaining:]
        overflow_classes = {(p['api_class'].upper(), p.get('version')) for p in overflow_plan}
        tracker = state.get("query_tracker") or []
        updated_tracker = []
        for entry in tracker:
            key = (entry['api_class'].upper(), entry.get('version'))
            if key in overflow_classes and entry['status'] == 'pending':
                updated_entry = dict(entry)
                updated_entry['status'] = 'budget_exceeded'
                updated_entry['reason'] = (
                    f"Tool call budget ({MAX_TOOL_CALLS}) exhausted during execution. "
                    f"Only {calls_remaining} call(s) remained when this item was reached. "
                    "Try asking about this API in a follow-up message."
                )
                updated_tracker.append(updated_entry)
                overflow_classes.discard(key)
            else:
                updated_tracker.append(entry)
        print(f"[Executor] Runtime overflow: plan has {len(plan)} items but only {calls_remaining} budget remaining. "
              f"Executing {len(executable_plan)}, marking {len(overflow_plan)} as budget_exceeded.")
        plan = executable_plan
        _overflow_tracker = updated_tracker

    # Build the executor prompt incorporating the plan
    if plan:
        plan_text = "\n".join(
            f"{i+1}. api_class={p['api_class']}, version={p.get('version') or 'latest'}, "
            f"query=\"{p['query']}\""
            for i, p in enumerate(plan)
        )
        plan_instructions = (
            f"Execute this retrieval plan exactly ({len(plan)} call(s)):\n{plan_text}\n\n"
            "CRITICAL: Make ONLY the tool calls listed above. If the user's query mentions other APIs "
            "(like checkout, invoices, etc.) that are NOT in this plan, DO NOT search for them. "
            "Those APIs have been filtered out because they are unavailable."
        )
    else:
        plan_instructions = (
            f"No plan was provided. Use your best judgment. "
            f"You have {calls_remaining} tool call(s) remaining in your budget."
        )

    system_msg = SystemMessage(content=f"{_EXECUTOR_SYSTEM}\n\n{plan_instructions}")
    messages_to_send = [system_msg] + list(state["messages"])

    response = get_llm_with_tools_bound().invoke(messages_to_send)

    # --- Post-validation: strip unauthorized tool calls ---
    if hasattr(response, "tool_calls") and response.tool_calls and plan:
        allowed_classes = {p['api_class'].upper() for p in plan}
        original_count = len(response.tool_calls)
        
        valid_tool_calls = []
        for tc in response.tool_calls:
            tc_class = tc.get('args', {}).get('api_class', '').upper()
            if not tc_class or tc_class in allowed_classes:
                valid_tool_calls.append(tc)
            else:
                print(f"[Executor] BLOCKED unauthorized tool call for: {tc_class}")
        
        if len(valid_tool_calls) < original_count:
            print(f"[Executor] Stripped {original_count - len(valid_tool_calls)} unauthorized call(s)")
            response.tool_calls = valid_tool_calls

    calls_made = len(response.tool_calls) if hasattr(response, "tool_calls") and response.tool_calls else 0
    print(f"\n[Executor] Made {calls_made} tool call(s). Budget: {current_budget + calls_made}/{MAX_TOOL_CALLS}")

    if trace:
        trace.end_node("executor", {
            "calls_made": calls_made,
            "budget_after": current_budget + calls_made,
            "budget_max": MAX_TOOL_CALLS,
            "tool_calls": [
                {"api_class": tc.get("args", {}).get("api_class", ""), "version": tc.get("args", {}).get("version", ""), "query": tc.get("args", {}).get("query", "")}
                for tc in (response.tool_calls if hasattr(response, "tool_calls") and response.tool_calls else [])
            ]
        })

    result = {
        "messages": [response],
        "tool_call_budget": current_budget + calls_made,
        # Clear the plan after execution so it doesn't re-fire on the next turn
        "tool_plan": [],
        "rephrase_count": state.get("rephrase_count", 0)
    }
    # If we had runtime overflow, persist the updated tracker
    if _overflow_tracker is not None:
        result["query_tracker"] = _overflow_tracker
    return result


# ---------------------------------------------------------------------------
# 6. Synthesizer Node
# ---------------------------------------------------------------------------
# The synthesizer is a dedicated "write the final answer" node. Using a plain
# LLM (no tools bound) here is critical — it physically cannot loop back into
# tool calls, so synthesis is guaranteed to terminate.

_SYNTHESIZER_SYSTEM = """You are a Stripe API documentation expert. 
Your task is to synthesize a final, comprehensive answer using ONLY the RESTRUCTURER ANALYSIS
provided below and the retrieved documentation chunks present in the conversation.

The RESTRUCTURER ANALYSIS contains a coverage report with each sub-query's status:
- COVERED: Documentation was successfully retrieved — include the answer.
- NOT_FOUND: Search ran but no matching docs — state this to the user.
- UNAVAILABLE: API class is not in this system — clearly inform the user.
- BUDGET_EXCEEDED: Tool call budget ran out before this query could execute — inform the user.

Rules:
- Address EVERY sub-query from the restructurer analysis, in order.
- For COVERED sub-queries, provide detailed answers based STRICTLY on the retrieved chunks.
- For UNAVAILABLE sub-queries:
  * State ONLY: "[API name] is not available in this documentation system."
  * Then list the available API classes the user can ask about.
  * Do NOT suggest workarounds, alternatives, code examples, or implementation approaches.
  * Do NOT speculate about what the unavailable API might contain or how it might work.
  * Do NOT mention or reference any other API as a substitute.
- For NOT_FOUND sub-queries:
  * State ONLY: "No matching documentation was found for [query]."
  * Suggest the user rephrase their question.
  * Do NOT guess or infer what the answer might be.
- For BUDGET_EXCEEDED sub-queries:
  * Inform the user that these APIs could not be searched because the tool call budget
    was exhausted during this request.
  * List which APIs were skipped and suggest the user ask about them in a follow-up message.
  * Do NOT fabricate information about these APIs.

STRICT GUARDRAILS — NEVER violate these:
1. NEVER fabricate, invent, or hallucinate any information not present in the retrieved chunks.
2. NEVER generate code examples, API calls, or implementation snippets unless they come directly from retrieved documentation.
3. NEVER provide information about APIs marked as UNAVAILABLE — only acknowledge unavailability.
4. NEVER fill knowledge gaps with general Stripe knowledge. If it's not in the chunks, don't say it.
5. If a version comparison was requested, structure with clear v1/v2 sections using ONLY retrieved data.
6. Use markdown tables for parameter comparisons when appropriate.
7. The RESTRUCTURER ANALYSIS uses a plain-text format for internal tracking.
   Do NOT reproduce its formatting (labels like "Sub-query 1", status lines, etc.) in your answer.
   Use your OWN markdown structure (headers, tables, bullet points) to present the answer clearly.
8. Do not call any tools. Write the answer now."""

def synthesizer_node(state: AgentState) -> dict:
    """
    Produces the final answer. Bound to a plain LLM — cannot call tools.
    This guarantees the graph terminates rather than looping.
    Reads restructurer_analysis from state (not from messages) to keep
    conversation history clean for future turns.
    Also builds a turn record for the conversation operation log.
    """
    trace = get_trace()
    if trace:
        trace.start_node("synthesizer", {"description": "Generating final synthesized answer"})

    print("\n[Synthesizer] Generating final answer...")
    analysis = state.get("restructurer_analysis", "")
    system_content = _SYNTHESIZER_SYSTEM
    if analysis:
        system_content += f"\n\nRESTRUCTURER ANALYSIS:\n\n{analysis}"
    messages_to_send = [SystemMessage(content=system_content)] + list(state["messages"])
    response = get_llm_plain().invoke(messages_to_send)

    # --- Build turn record for the conversation operation log ---
    tracker = state.get("query_tracker") or []
    user_msg = next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), None
    )
    turn_record = {
        "user_query": user_msg.content if user_msg else "",
        "operations": [
            {
                "api_class": t["api_class"],
                "version": t.get("version"),
                "query": t["query"],
                "status": t["status"]
            }
            for t in tracker
        ]
    }
    existing_context = list(state.get("conversation_context") or [])
    existing_context.append(turn_record)
    print(f"[Synthesizer] Operation log now has {len(existing_context)} turn(s)")

    # --- Derive active scope from covered tracker entries ---
    covered_entries = [t for t in tracker if t["status"] == "covered"]
    if covered_entries:
        # Deduplicate while preserving order
        seen_classes = []
        seen_versions = []
        for e in covered_entries:
            cls = e["api_class"]
            ver = e.get("version")
            if cls not in seen_classes:
                seen_classes.append(cls)
            if ver and ver not in seen_versions:
                seen_versions.append(ver)
        new_scope = {
            "api_classes": seen_classes,
            "versions": seen_versions if seen_versions else [None]
        }
        print(f"[Synthesizer] Active scope updated: {new_scope}")
    else:
        # No covered results — keep previous scope unchanged
        new_scope = state.get("active_scope")

    if trace:
        trace.end_node("synthesizer", {
            "answer_length": len(response.content) if response.content else 0,
            "operation_log_turns": len(existing_context),
            "active_scope": new_scope
        })

    return {
        "messages": [response],
        "conversation_context": existing_context,
        "active_scope": new_scope
    }


# ---------------------------------------------------------------------------
# 7. Query Expander Node
# ---------------------------------------------------------------------------
# Per-tool retry: fires when ANY tool call returns "No documentation found".
# Does lightweight correlation (similar to restructurer) to identify ALL
# failed entries, then builds a retry plan for every one of them.
# Routes through budget_checker, which truncates if retries exceed the
# remaining budget — no need to artificially free budget slots.

def query_expander(state: AgentState) -> dict:
    """
    Triggered when any tool result is empty. Performs lightweight correlation
    to identify ALL failed tracker entries, builds a retry plan for each,
    and routes through budget_checker for natural truncation.
    """
    trace = get_trace()
    if trace:
        trace.start_node("query_expander", {"description": "Retrying failed queries with broader terminology"})

    tracker = [dict(t) for t in (state.get("query_tracker", []) or [])]

    # --- Lightweight correlation to identify failed entries ---
    # Build tool_call_id → original args map from executor's AIMessages
    tool_call_args = {}
    for m in state["messages"]:
        if isinstance(m, AIMessage) and hasattr(m, "tool_calls") and m.tool_calls:
            for tc in m.tool_calls:
                tool_call_args[tc["id"]] = tc.get("args", {})

    def _norm_version(v):
        return None if v in (None, "latest", "") else v

    # Identify which (api_class, version) keys returned "No documentation found"
    failed_keys = set()
    for m in state["messages"]:
        if isinstance(m, ToolMessage):
            args = tool_call_args.get(m.tool_call_id, {})
            tc_class = args.get("api_class", "").upper()
            tc_version = _norm_version(args.get("version"))
            if tc_class and "No documentation found" in m.content:
                failed_keys.add((tc_class, tc_version))

    # Build retry plan from ALL pending tracker entries whose tool calls failed
    retry_plan = []
    for entry in tracker:
        if entry["status"] != "pending":
            continue  # Already resolved (unavailable, budget_exceeded, covered)
        key = (entry["api_class"].upper(), _norm_version(entry.get("version")))
        if key in failed_keys:
            retry_plan.append({
                "api_class": entry["api_class"],
                "version": entry.get("version"),
                "query": entry["query"]
            })
            # Entry stays "pending" for the retry

    rephrase_count = state.get("rephrase_count", 0) + 1
    print(f"\n[Query Expander] Retry round {rephrase_count}/{MAX_REPHRASE} — {len(retry_plan)} item(s) to retry")
    for p in retry_plan:
        print(f"  → {p['api_class']} {p.get('version') or 'latest'} — '{p['query']}'")

    if trace:
        trace.end_node("query_expander", {
            "rephrase_count": rephrase_count,
            "max_rephrase": MAX_REPHRASE,
            "retry_items": len(retry_plan),
            "retry_plan": retry_plan
        })

    return {
        "messages": [SystemMessage(content="SYSTEM: Some searches returned no results. Retrying failed queries with broader terminology.")],
        "rephrase_count": rephrase_count,
        # Budget is NOT freed — budget_checker handles truncation naturally
        "tool_plan": retry_plan,
        "query_tracker": tracker
    }


# ---------------------------------------------------------------------------
# 8. Routing Logic
# ---------------------------------------------------------------------------

def route_after_planner(state: AgentState) -> Literal["budget_checker", "__end__"]:
    """
    If the planner asked a clarification question, end the turn (the question
    is already in messages). Otherwise proceed to budget check.
    """
    trace = get_trace()
    if state.get("needs_clarification"):
        if trace:
            trace.add_routing("planner", "__end__", "Clarification needed")
        return "__end__"
    if trace:
        trace.add_routing("planner", "budget_checker", "Plan ready, checking budget")
    return "budget_checker"


def route_after_executor(state: AgentState) -> Literal["tools", "restructurer", "synthesizer"]:
    """Routes to tools if the executor made tool calls, to restructurer if
    returning from query_expander with no new calls, else to synthesizer."""
    trace = get_trace()
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        if trace:
            trace.add_routing("executor", "tools", f"Executing {len(last_message.tool_calls)} tool call(s)")
        return "tools"
    
    # If we have a query_tracker, we should always go through restructurer
    if state.get("query_tracker"):
        if trace:
            trace.add_routing("executor", "restructurer", "Has query tracker, analyzing coverage")
        return "restructurer"
    
    # No tracker = budget exhausted fallback or planner failure
    if trace:
        trace.add_routing("executor", "synthesizer", "No tracker, direct synthesis")
    return "synthesizer"


def route_after_tools(state: AgentState) -> Literal["query_expander", "restructurer"]:
    """
    Per-tool retry routing: if ANY tool call returned 'No documentation found'
    and retry attempts remain, route to query_expander.
    """
    trace = get_trace()
    current_rephrase = state.get("rephrase_count", 0)
    
    # Collect all recent ToolMessages
    tool_messages = []
    for m in reversed(state["messages"]):
        if isinstance(m, ToolMessage):
            tool_messages.append(m)
        elif tool_messages:  # Stop once we pass the ToolMessage block
            break
    
    if not tool_messages:
        if trace:
            trace.add_routing("tools", "restructurer", "No tool messages found")
        return "restructurer"
    
    # Check if ANY tool call failed
    any_failure = any(
        "No documentation found" in tm.content for tm in tool_messages
    )
    
    # Route to query_expander if there are failures and retries remain
    if any_failure and current_rephrase < MAX_REPHRASE:
        if trace:
            trace.add_routing("tools", "query_expander", f"Failures detected, retry {current_rephrase + 1}/{MAX_REPHRASE}")
        return "query_expander"
    
    if trace:
        reason = "All tools succeeded" if not any_failure else f"Retries exhausted ({current_rephrase}/{MAX_REPHRASE})"
        trace.add_routing("tools", "restructurer", reason)
    return "restructurer"


# ---------------------------------------------------------------------------
# 9. Restructurer Node
# ---------------------------------------------------------------------------
# The restructurer sits between tools and synthesizer. It reviews whether
# the retrieved data fully covers the user's original query, identifies
# gaps, and produces a structured analysis for the synthesizer.

def restructurer_node(state: AgentState) -> dict:
    """
    Reviews retrieved data against the original query using the query_tracker.
    Correlates tool results with tracked queries, updates statuses, and
    produces a structured coverage analysis for the synthesizer.
    """
    trace = get_trace()
    if trace:
        trace.start_node("restructurer", {"description": "Analyzing coverage of retrieved data"})

    print("\n[Restructurer] Analyzing coverage of user's query...")
    
    query_tracker = state.get("query_tracker", []) or []
    
    if not query_tracker:
        print("[Restructurer] No query tracker found, skipping.")
        if trace:
            trace.end_node("restructurer", {"result": "no_tracker"})
        return {}
    
    # --- Robust correlation via tool_call_id instead of string matching ---
    # Build tool_call_id → original args map from executor's AIMessages
    tool_call_args = {}
    for m in state["messages"]:
        if isinstance(m, AIMessage) and hasattr(m, "tool_calls") and m.tool_calls:
            for tc in m.tool_calls:
                tool_call_args[tc["id"]] = tc.get("args", {})

    tool_messages = [m for m in state["messages"] if isinstance(m, ToolMessage)]

    # Normalize versions: treat None, "latest", and "" as equivalent
    def _norm_version(v):
        return None if v in (None, "latest", "") else v

    # Map (api_class, normalized_version) → ToolMessage content
    result_map = {}
    for tm in tool_messages:
        args = tool_call_args.get(tm.tool_call_id, {})
        tc_class = args.get("api_class", "").upper()
        tc_version = _norm_version(args.get("version"))
        if tc_class:
            result_map[(tc_class, tc_version)] = tm.content

    # Correlate tracker entries with tool results using authoritative args
    for entry in query_tracker:
        if entry["status"] != "pending":
            continue  # Already resolved (unavailable)

        key = (entry["api_class"].upper(), _norm_version(entry.get("version")))
        content = result_map.get(key)

        if content is None:
            entry["status"] = "not_found"
            entry["reason"] = "No tool results matched this query"
        elif "No documentation found" in content:
            entry["status"] = "not_found"
            entry["reason"] = "No matching documentation in vector store"
        else:
            entry["status"] = "covered"
    
    # Build structured coverage analysis in plain text (no markdown) to avoid
    # formatting collisions when the synthesizer composes its own markdown answer.
    analysis_lines = ["QUERY COVERAGE ANALYSIS\n"]
    
    for i, entry in enumerate(query_tracker, 1):
        version_str = entry.get('version') or 'latest'
        analysis_lines.append(f"[Sub-query {i}] {entry['api_class']} {version_str} — \"{entry['query']}\"")
        analysis_lines.append(f"  Status: {entry['status'].upper()}")
        if entry.get('reason'):
            analysis_lines.append(f"  Reason: {entry['reason']}")
        analysis_lines.append("")
    
    # Summary counts
    covered = sum(1 for e in query_tracker if e['status'] == 'covered')
    not_found = sum(1 for e in query_tracker if e['status'] == 'not_found')
    unavailable = sum(1 for e in query_tracker if e['status'] == 'unavailable')
    budget_exceeded = sum(1 for e in query_tracker if e['status'] == 'budget_exceeded')
    total = len(query_tracker)
    
    summary_parts = [f"{covered}/{total} covered", f"{not_found} not found", f"{unavailable} unavailable"]
    if budget_exceeded > 0:
        summary_parts.append(f"{budget_exceeded} budget exceeded")
    analysis_lines.append(f"Summary: {', '.join(summary_parts)}")
    
    if unavailable > 0:
        unavailable_apis = [e['api_class'] for e in query_tracker if e['status'] == 'unavailable']
        analysis_lines.append(f"Unavailable APIs: {', '.join(unavailable_apis)}")
        analysis_lines.append(f"Available APIs: {', '.join(KNOWN_API_CLASSES)}")
    
    if budget_exceeded > 0:
        exceeded_apis = [f"{e['api_class']} {e.get('version') or 'latest'}" for e in query_tracker if e['status'] == 'budget_exceeded']
        analysis_lines.append(f"Budget exceeded APIs (ask in follow-up): {', '.join(exceeded_apis)}")
    
    analysis_text = "\n".join(analysis_lines)
    
    print(f"[Restructurer] Coverage: {covered}/{total} covered, {not_found} not found, {unavailable} unavailable, {budget_exceeded} budget exceeded")
    for entry in query_tracker:
        status_icon = {"covered": "✓", "not_found": "✗", "unavailable": "⊘", "budget_exceeded": "⏸"}.get(entry['status'], '?')
        print(f"  {status_icon} {entry['api_class']} {entry.get('version') or 'latest'} — {entry['status']}")
    
    if trace:
        trace.end_node("restructurer", {
            "covered": covered,
            "not_found": not_found,
            "unavailable": unavailable,
            "budget_exceeded": budget_exceeded,
            "total": total,
            "query_tracker": query_tracker
        })

    return {
        "restructurer_analysis": analysis_text,
        "query_tracker": query_tracker
    }


# ---------------------------------------------------------------------------
# 10. Graph Assembly
# ---------------------------------------------------------------------------

workflow = StateGraph(AgentState)

workflow.add_node("planner",         planner_node)
workflow.add_node("budget_checker",  budget_checker_node)
workflow.add_node("executor",        executor_node)
workflow.add_node("tools",           tool_node)
workflow.add_node("query_expander",  query_expander)
workflow.add_node("restructurer",    restructurer_node)
workflow.add_node("synthesizer",     synthesizer_node)

workflow.set_entry_point("planner")

workflow.add_conditional_edges("planner",        route_after_planner)
workflow.add_conditional_edges("budget_checker", route_after_budget_checker,
    {"executor": "executor", "restructurer": "restructurer", "__end__": END})
workflow.add_conditional_edges("executor",       route_after_executor,
    {"tools": "tools", "restructurer": "restructurer", "synthesizer": "synthesizer"})
workflow.add_conditional_edges("tools",          route_after_tools)
workflow.add_edge("query_expander", "budget_checker")  # retries also go through budget check
workflow.add_edge("restructurer",   "synthesizer")     # restructurer always leads to synthesis
workflow.add_edge("synthesizer",    END)

app_graph = workflow.compile()