# src/graph/nodes.py
"""
Graph node functions for the Stripe RAG Agent.

Each node function takes the agent state and returns state updates.
"""

import json
from typing import List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode

from src.graph.state import AgentState, ToolPlan, QueryTracker
from src.dependencies import get_current_llm
from src.tools import tools
from src.trace import get_trace
from src.constants import (
    MAX_TOOL_CALLS,
    MAX_REPHRASE,
    MAX_CONTEXT_TURNS,
    KNOWN_API_CLASSES,
    STATUS_PENDING,
    STATUS_COVERED,
    STATUS_NOT_FOUND,
    STATUS_UNAVAILABLE,
    STATUS_BUDGET_EXCEEDED,
    STATUS_ICONS,
    INTENT_NEW,
)
from src.prompts import (
    get_planner_system_prompt,
    EXECUTOR_SYSTEM_PROMPT,
    SYNTHESIZER_SYSTEM_PROMPT,
)


# ---------------------------------------------------------------------------
# LLM Access Functions
# ---------------------------------------------------------------------------

def get_llm_plain():
    """Get the current request's LLM without tools bound (for planning/synthesis)."""
    return get_current_llm()


def get_llm_with_tools_bound():
    """Get the current request's LLM with tools bound (for executor)."""
    return get_current_llm().bind_tools(tools)


# Pre-configured tool node for executing tool calls
tool_node = ToolNode(tools)


# ---------------------------------------------------------------------------
# Planner Node
# ---------------------------------------------------------------------------

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
        return {"tool_plan": [], "needs_clarification": False, "intent_type": INTENT_NEW}

    print("\n[Planner] Analyzing query and building plan...")
    
    # Build context-aware prompt
    messages = state.get("messages", [])
    
    # Generate planner system prompt with current config
    planner_system_content = get_planner_system_prompt(KNOWN_API_CLASSES, MAX_TOOL_CALLS)
    
    # Inject active scope if available
    active_scope = state.get("active_scope")
    if active_scope:
        scope_json = json.dumps(active_scope)
        planner_system_content += f"\n\nACTIVE SCOPE:\n{scope_json}"
        print(f"[Planner] Active scope: {scope_json}")

    # Inject conversation operation log if available
    conv_context = state.get("conversation_context") or []
    if conv_context:
        trimmed = conv_context[-MAX_CONTEXT_TURNS:]
        context_json = json.dumps(trimmed, indent=2)
        planner_system_content += f"\n\nCONVERSATION OPERATION LOG (last {len(trimmed)} of {len(conv_context)} turns):\n{context_json}"
        print(f"[Planner] Injecting operation log ({len(trimmed)}/{len(conv_context)} turn(s), max={MAX_CONTEXT_TURNS})")
    
    # Build prompt messages with history for multi-turn context
    if len(messages) > 1:
        print(f"[Planner] Using conversation context ({len(messages)} total messages)")
        context_messages = messages[:-1][-10:]  # Last 10 messages for context
        prompt_messages = [SystemMessage(content=planner_system_content)]
        prompt_messages.extend(context_messages)
        prompt_messages.append(HumanMessage(content=user_message.content))
    else:
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
            return {"needs_clarification": False, "tool_plan": [], "intent_type": INTENT_NEW}
        
        # Strip markdown fences if the model added them
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw.rsplit("\n", 1)[0] if "\n" in raw else raw[:-3]
        raw = raw.strip()
        
        print(f"[Planner DEBUG] Cleaned JSON string: '{raw[:200]}'")
        
        plan_data = json.loads(raw)
        
        # Extract intent type
        intent_type = plan_data.get("intent_type", INTENT_NEW)
        print(f"[Planner] Intent classification: {intent_type}")

        # Handle clarification requests
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
                query_tracker.append({
                    "api_class": api_class,
                    "version": version,
                    "query": query,
                    "status": STATUS_UNAVAILABLE,
                    "reason": f"API class not recognized. Available: {known_str}"
                })
                print(f"[Planner] Skipped UNKNOWN: query='{query}'")
            elif api_class and api_class not in KNOWN_API_CLASSES:
                query_tracker.append({
                    "api_class": api_class,
                    "version": version,
                    "query": query,
                    "status": STATUS_UNAVAILABLE,
                    "reason": f"{api_class} is not available in this system. Available: {known_str}"
                })
                print(f"[Planner] Skipped unavailable: {api_class}")
            else:
                query_tracker.append({
                    "api_class": api_class,
                    "version": version,
                    "query": query,
                    "status": STATUS_PENDING,
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
            status_icon = "→" if t['status'] == STATUS_PENDING else "✗"
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
        return {"needs_clarification": False, "tool_plan": [], "intent_type": INTENT_NEW}


# ---------------------------------------------------------------------------
# Budget Checker Node
# ---------------------------------------------------------------------------

def budget_checker_node(state: AgentState) -> dict:
    """
    Validates that the planned tool calls fit within the budget.
    Sits between planner and executor.
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
        print(f"[Budget Checker] Plan ({plan_size} calls) fits within budget ({calls_remaining} remaining). Proceeding.")
        if trace:
            trace.end_node("budget_checker", {"result": "within_budget", "plan_size": plan_size, "calls_remaining": calls_remaining})
        return {}

    # --- Plan exceeds budget ---

    # RETRY PATH: we already have partial results from prior tool calls.
    if current_budget > 0:
        executable_plan = plan[:calls_remaining] if calls_remaining > 0 else []
        overflow_plan = plan[calls_remaining:] if calls_remaining > 0 else plan

        overflow_keys = {(p['api_class'].upper(), p.get('version')) for p in overflow_plan}
        tracker = state.get("query_tracker") or []
        updated_tracker = []
        for entry in tracker:
            key = (entry['api_class'].upper(), entry.get('version'))
            if key in overflow_keys and entry['status'] == STATUS_PENDING:
                updated_entry = dict(entry)
                updated_entry['status'] = STATUS_BUDGET_EXCEEDED
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

    batch_size = max(1, calls_remaining)
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


# ---------------------------------------------------------------------------
# Executor Node
# ---------------------------------------------------------------------------

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
        tracker = state.get("query_tracker") or []
        updated_tracker = []
        for entry in tracker:
            if entry["status"] == STATUS_PENDING:
                updated_entry = dict(entry)
                updated_entry["status"] = STATUS_BUDGET_EXCEEDED
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
    _overflow_tracker = None
    if plan and len(plan) > calls_remaining:
        executable_plan = plan[:calls_remaining]
        overflow_plan = plan[calls_remaining:]
        overflow_classes = {(p['api_class'].upper(), p.get('version')) for p in overflow_plan}
        tracker = state.get("query_tracker") or []
        updated_tracker = []
        for entry in tracker:
            key = (entry['api_class'].upper(), entry.get('version'))
            if key in overflow_classes and entry['status'] == STATUS_PENDING:
                updated_entry = dict(entry)
                updated_entry['status'] = STATUS_BUDGET_EXCEEDED
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

    system_msg = SystemMessage(content=f"{EXECUTOR_SYSTEM_PROMPT}\n\n{plan_instructions}")
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
        "tool_plan": [],
        "rephrase_count": state.get("rephrase_count", 0)
    }
    if _overflow_tracker is not None:
        result["query_tracker"] = _overflow_tracker
    return result


# ---------------------------------------------------------------------------
# Synthesizer Node
# ---------------------------------------------------------------------------

def synthesizer_node(state: AgentState) -> dict:
    """
    Produces the final answer. Bound to a plain LLM — cannot call tools.
    This guarantees the graph terminates rather than looping.
    """
    trace = get_trace()
    if trace:
        trace.start_node("synthesizer", {"description": "Generating final synthesized answer"})

    print("\n[Synthesizer] Generating final answer...")
    analysis = state.get("restructurer_analysis", "")
    system_content = SYNTHESIZER_SYSTEM_PROMPT
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
    covered_entries = [t for t in tracker if t["status"] == STATUS_COVERED]
    if covered_entries:
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
# Query Expander Node
# ---------------------------------------------------------------------------

def query_expander_node(state: AgentState) -> dict:
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
        if entry["status"] != STATUS_PENDING:
            continue
        key = (entry["api_class"].upper(), _norm_version(entry.get("version")))
        if key in failed_keys:
            retry_plan.append({
                "api_class": entry["api_class"],
                "version": entry.get("version"),
                "query": entry["query"]
            })

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
        "tool_plan": retry_plan,
        "query_tracker": tracker
    }


# ---------------------------------------------------------------------------
# Restructurer Node
# ---------------------------------------------------------------------------

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
    
    # --- Robust correlation via tool_call_id ---
    tool_call_args = {}
    for m in state["messages"]:
        if isinstance(m, AIMessage) and hasattr(m, "tool_calls") and m.tool_calls:
            for tc in m.tool_calls:
                tool_call_args[tc["id"]] = tc.get("args", {})

    tool_messages = [m for m in state["messages"] if isinstance(m, ToolMessage)]

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

    # Correlate tracker entries with tool results
    for entry in query_tracker:
        if entry["status"] != STATUS_PENDING:
            continue

        key = (entry["api_class"].upper(), _norm_version(entry.get("version")))
        content = result_map.get(key)

        if content is None:
            entry["status"] = STATUS_NOT_FOUND
            entry["reason"] = "No tool results matched this query"
        elif "No documentation found" in content:
            entry["status"] = STATUS_NOT_FOUND
            entry["reason"] = "No matching documentation in vector store"
        else:
            entry["status"] = STATUS_COVERED
    
    # Build structured coverage analysis in plain text
    analysis_lines = ["QUERY COVERAGE ANALYSIS\n"]
    
    for i, entry in enumerate(query_tracker, 1):
        version_str = entry.get('version') or 'latest'
        analysis_lines.append(f"[Sub-query {i}] {entry['api_class']} {version_str} — \"{entry['query']}\"")
        analysis_lines.append(f"  Status: {entry['status'].upper()}")
        if entry.get('reason'):
            analysis_lines.append(f"  Reason: {entry['reason']}")
        analysis_lines.append("")
    
    # Summary counts
    covered = sum(1 for e in query_tracker if e['status'] == STATUS_COVERED)
    not_found = sum(1 for e in query_tracker if e['status'] == STATUS_NOT_FOUND)
    unavailable = sum(1 for e in query_tracker if e['status'] == STATUS_UNAVAILABLE)
    budget_exceeded = sum(1 for e in query_tracker if e['status'] == STATUS_BUDGET_EXCEEDED)
    total = len(query_tracker)
    
    summary_parts = [f"{covered}/{total} covered", f"{not_found} not found", f"{unavailable} unavailable"]
    if budget_exceeded > 0:
        summary_parts.append(f"{budget_exceeded} budget exceeded")
    analysis_lines.append(f"Summary: {', '.join(summary_parts)}")
    
    if unavailable > 0:
        unavailable_apis = [e['api_class'] for e in query_tracker if e['status'] == STATUS_UNAVAILABLE]
        analysis_lines.append(f"Unavailable APIs: {', '.join(unavailable_apis)}")
        analysis_lines.append(f"Available APIs: {', '.join(KNOWN_API_CLASSES)}")
    
    if budget_exceeded > 0:
        exceeded_apis = [f"{e['api_class']} {e.get('version') or 'latest'}" for e in query_tracker if e['status'] == STATUS_BUDGET_EXCEEDED]
        analysis_lines.append(f"Budget exceeded APIs (ask in follow-up): {', '.join(exceeded_apis)}")
    
    analysis_text = "\n".join(analysis_lines)
    
    print(f"[Restructurer] Coverage: {covered}/{total} covered, {not_found} not found, {unavailable} unavailable, {budget_exceeded} budget exceeded")
    for entry in query_tracker:
        status_icon = STATUS_ICONS.get(entry['status'], '?')
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
