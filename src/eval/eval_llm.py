# src/eval/eval_llm.py
"""
Stripe RAG Agent Evaluation Framework

This framework evaluates the RAG agent on:
1. LLM Quality Metrics (via Ragas):
   - Faithfulness: Does the answer stay true to retrieved context?
   - Answer Relevancy: Does it actually answer the question?
   - Answer Correctness: How complete is it compared to ground truth?

2. Performance Metrics:
   - Latency: End-to-end response time
   - Token Usage: Total tokens consumed (input + output)
   - Tool Calls: Number of retrieval operations

HOW IT WORKS:
1. Each test case is run through the full agent graph
2. The agent retrieves context via tools (ToolMessages)
3. The agent generates a synthesized answer (final AIMessage)
4. Ragas evaluates answer quality using an LLM judge
5. Performance metrics are computed from execution stats

USAGE:
    # Run full evaluation
    python -m src.eval.eval_llm

    # Run quick test (2 cases)
    python -m src.eval.eval_llm --quick

    # Run specific category
    python -m src.eval.eval_llm --category customers
"""

import os
import sys
import time
import argparse
from typing import List, Dict, Any, Optional
from datetime import datetime

import pandas as pd
from datasets import Dataset
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Ragas metrics
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    answer_correctness,
)

# Import your agent graph and state types
from src.agent import app_graph, AgentState
from src.dependencies import get_llm, set_llm
from src.config import config

# Import test cases
from src.eval.test_cases import get_test_cases, ALL_TEST_CASES


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_OUTPUT_DIR = "data/eval"
RAGAS_LLM_MODEL = "gpt-4o-mini"  # LLM used by Ragas as the judge


# ---------------------------------------------------------------------------
# Evaluation Runner
# ---------------------------------------------------------------------------
class EvaluationRunner:
    """
    Runs evaluation test cases through the RAG agent and collects metrics.
    """
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = True):
        """
        Initialize the evaluation runner.
        
        Args:
            api_key: Groq API key. If None, uses environment variable or config.
            verbose: Print progress during evaluation.
        """
        self.verbose = verbose
        self._setup_llm(api_key)
        
    def _setup_llm(self, api_key: Optional[str] = None):
        """Configure the LLM for the agent."""
        try:
            llm = get_llm(api_key=api_key)
            set_llm(llm)
            if self.verbose:
                print("[Eval] LLM configured successfully")
        except ValueError as e:
            print(f"[Eval] ERROR: Failed to setup LLM: {e}")
            print("[Eval] Make sure GROQ_API_KEY is set in environment or config.yaml")
            sys.exit(1)
    
    def _build_initial_state(self, question: str) -> dict:
        """
        Build the initial agent state for a test question.
        
        This matches the state structure used by the actual API endpoint.
        """
        return {
            "messages": [HumanMessage(content=question)],
            "tool_call_budget": 0,
            "needs_clarification": False,
            "tool_plan": None,
            "rephrase_count": 0,
            "intent_type": None,
            "conversation_context": None,
            "active_scope": None,
            "query_tracker": None,
            "restructurer_analysis": None,
            "frontier_result": None,
            "is_rejected": False,
        }
    
    def _extract_contexts(self, messages: List) -> List[str]:
        """
        Extract retrieved contexts from ToolMessages.
        
        These are the chunks returned by the search_stripe_api_docs tool.
        Ragas uses these to evaluate faithfulness.
        """
        contexts = []
        for msg in messages:
            if isinstance(msg, ToolMessage):
                content = msg.content
                # Tool messages might be JSON or plain text
                if content and content.strip():
                    contexts.append(content)
        return contexts
    
    def _extract_token_usage(self, messages: List) -> Dict[str, int]:
        """
        Extract token usage from AIMessages.
        
        LangChain models attach usage_metadata to AIMessages with token counts.
        """
        total_tokens = 0
        input_tokens = 0
        output_tokens = 0
        
        for msg in messages:
            if isinstance(msg, AIMessage):
                usage = getattr(msg, "usage_metadata", None)
                if usage:
                    total_tokens += usage.get("total_tokens", 0)
                    input_tokens += usage.get("input_tokens", 0)
                    output_tokens += usage.get("output_tokens", 0)
        
        return {
            "total_tokens": total_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }
    
    def _count_tool_calls(self, messages: List) -> int:
        """Count the number of tool calls made during execution."""
        return sum(1 for msg in messages if isinstance(msg, ToolMessage))
    
    def run_single_test(self, test_case: dict) -> Dict[str, Any]:
        """
        Run a single test case through the agent.
        
        Args:
            test_case: Dict with 'question' and 'ground_truth' keys
            
        Returns:
            Dict with answer, contexts, and performance metrics
        """
        question = test_case["question"]
        
        # Build initial state
        initial_state = self._build_initial_state(question)
        
        # Time the execution
        start_time = time.time()
        
        # Invoke the agent graph
        try:
            output_state = app_graph.invoke(initial_state)
        except Exception as e:
            return {
                "question": question,
                "answer": f"[ERROR: {str(e)}]",
                "contexts": [],
                "ground_truth": test_case["ground_truth"],
                "latency_seconds": time.time() - start_time,
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "tool_calls": 0,
                "error": str(e),
                "is_rejected": False,
                "rejection_type": None,
            }
        
        latency = time.time() - start_time
        
        # Extract results
        messages = output_state.get("messages", [])
        final_message = messages[-1] if messages else None
        answer = final_message.content if final_message else "[No response]"
        
        # Extract contexts from tool messages
        contexts = self._extract_contexts(messages)
        
        # Extract token usage
        token_usage = self._extract_token_usage(messages)
        
        # Count tool calls
        tool_calls = self._count_tool_calls(messages)
        
        # Extract frontier rejection info
        is_rejected = output_state.get("is_rejected", False)
        frontier_result = output_state.get("frontier_result")
        rejection_type = frontier_result.get("rejection_type") if frontier_result else None
        
        return {
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": test_case["ground_truth"],
            "latency_seconds": round(latency, 2),
            "total_tokens": token_usage["total_tokens"],
            "input_tokens": token_usage["input_tokens"],
            "output_tokens": token_usage["output_tokens"],
            "tool_calls": tool_calls,
            "category": test_case.get("category", "unknown"),
            "is_rejected": is_rejected,
            "rejection_type": rejection_type,
        }
    
    def run_evaluation(self, test_cases: List[dict]) -> Dict[str, List]:
        """
        Run all test cases and collect results.
        
        Args:
            test_cases: List of test case dicts
            
        Returns:
            Dict with lists of results for each metric
        """
        results = {
            "question": [],
            "answer": [],
            "contexts": [],
            "ground_truth": [],
            "latency_seconds": [],
            "total_tokens": [],
            "input_tokens": [],
            "output_tokens": [],
            "tool_calls": [],
            "category": [],
            "is_rejected": [],
            "rejection_type": [],
        }
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Running Evaluation: {len(test_cases)} test cases")
            print(f"{'='*60}")
        
        for idx, test_case in enumerate(test_cases):
            if self.verbose:
                print(f"\n[{idx+1}/{len(test_cases)}] {test_case['question'][:60]}...")
            
            result = self.run_single_test(test_case)
            
            # Append to results
            for key in results:
                results[key].append(result.get(key))
            
            if self.verbose:
                rejected_str = " [REJECTED]" if result.get('is_rejected') else ""
                print(f"  ✓ Latency: {result['latency_seconds']}s | "
                      f"Tokens: {result['total_tokens']} | "
                      f"Tool calls: {result['tool_calls']}{rejected_str}")
        
        return results


# ---------------------------------------------------------------------------
# Ragas Quality Evaluation
# ---------------------------------------------------------------------------
def run_ragas_evaluation(results: Dict[str, List], llm_model: str = RAGAS_LLM_MODEL) -> pd.DataFrame:
    """
    Run Ragas LLM quality evaluation on the collected results.
    
    Args:
        results: Dict with question, answer, contexts, ground_truth lists
        llm_model: OpenAI model to use as the Ragas judge
        
    Returns:
        DataFrame with quality scores
    """
    print("\n" + "="*60)
    print("Running Ragas Quality Evaluation (LLM-as-Judge)")
    print(f"Judge model: {llm_model}")
    print("="*60)
    
    # Ragas expects specific column names
    ragas_dataset = Dataset.from_dict({
        "question": results["question"],
        "answer": results["answer"],
        "contexts": results["contexts"],
        "ground_truth": results["ground_truth"],
    })
    
    # Run evaluation
    # Note: Ragas requires OPENAI_API_KEY in environment for the judge LLM
    try:
        evaluation_result = evaluate(
            dataset=ragas_dataset,
            metrics=[
                faithfulness,       # Is answer grounded in contexts?
                answer_relevancy,   # Does it answer the question?
                answer_correctness, # How complete vs ground truth?
            ],
        )
        return evaluation_result.to_pandas()
    except Exception as e:
        print(f"\n[WARNING] Ragas evaluation failed: {e}")
        print("Make sure OPENAI_API_KEY is set for the Ragas judge LLM")
        # Return empty DataFrame with expected columns
        return pd.DataFrame({
            "question": results["question"],
            "faithfulness": [None] * len(results["question"]),
            "answer_relevancy": [None] * len(results["question"]),
            "answer_correctness": [None] * len(results["question"]),
        })


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------
def generate_report(
    results: Dict[str, List],
    quality_df: pd.DataFrame,
    output_dir: str = DEFAULT_OUTPUT_DIR
) -> pd.DataFrame:
    """
    Combine performance and quality metrics into a final report.
    
    Args:
        results: Raw results from evaluation runner
        quality_df: DataFrame from Ragas evaluation
        output_dir: Directory to save reports
        
    Returns:
        Combined DataFrame with all metrics
    """
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    # Build performance DataFrame
    performance_df = pd.DataFrame({
        "question": results["question"],
        "answer": results["answer"],
        "category": results["category"],
        "latency_seconds": results["latency_seconds"],
        "total_tokens": results["total_tokens"],
        "input_tokens": results["input_tokens"],
        "output_tokens": results["output_tokens"],
        "tool_calls": results["tool_calls"],
    })
    
    # Merge with quality metrics (align on question)
    if "question" in quality_df.columns:
        final_df = performance_df.merge(
            quality_df[["question", "faithfulness", "answer_relevancy", "answer_correctness"]],
            on="question",
            how="left"
        )
    else:
        # Quality columns already match by index
        final_df = pd.concat([
            performance_df,
            quality_df[["faithfulness", "answer_relevancy", "answer_correctness"]]
        ], axis=1)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed report
    detailed_path = os.path.join(output_dir, f"eval_report_{timestamp}.csv")
    final_df.to_csv(detailed_path, index=False)
    
    # Save summary statistics
    summary = {
        "timestamp": timestamp,
        "total_cases": len(results["question"]),
        "avg_latency": round(sum(results["latency_seconds"]) / len(results["latency_seconds"]), 2),
        "avg_tokens": round(sum(results["total_tokens"]) / len(results["total_tokens"]), 0),
        "avg_tool_calls": round(sum(results["tool_calls"]) / len(results["tool_calls"]), 1),
        "avg_faithfulness": final_df["faithfulness"].mean() if final_df["faithfulness"].notna().any() else None,
        "avg_relevancy": final_df["answer_relevancy"].mean() if final_df["answer_relevancy"].notna().any() else None,
        "avg_correctness": final_df["answer_correctness"].mean() if final_df["answer_correctness"].notna().any() else None,
    }
    
    summary_df = pd.DataFrame([summary])
    summary_path = os.path.join(output_dir, f"eval_summary_{timestamp}.csv")
    summary_df.to_csv(summary_path, index=False)
    
    return final_df, summary, detailed_path, summary_path


def print_report(final_df: pd.DataFrame, summary: dict):
    """Print a formatted evaluation report to console."""
    print("\n" + "="*80)
    print(" EVALUATION REPORT")
    print("="*80)
    
    # Summary stats
    print("\n📊 SUMMARY STATISTICS")
    print("-"*40)
    print(f"  Total test cases:      {summary['total_cases']}")
    print(f"  Avg latency:           {summary['avg_latency']}s")
    print(f"  Avg tokens:            {summary['avg_tokens']}")
    print(f"  Avg tool calls:        {summary['avg_tool_calls']}")
    
    if summary.get('avg_faithfulness') is not None:
        print(f"\n  📈 Quality Metrics (0-1 scale):")
        print(f"     Faithfulness:       {summary['avg_faithfulness']:.3f}")
        print(f"     Relevancy:          {summary['avg_relevancy']:.3f}")
        print(f"     Correctness:        {summary['avg_correctness']:.3f}")
    
    # Per-question breakdown
    print("\n📝 PER-QUESTION RESULTS")
    print("-"*80)
    
    display_cols = ["question", "latency_seconds", "total_tokens", "tool_calls"]
    if final_df["faithfulness"].notna().any():
        display_cols.extend(["faithfulness", "answer_relevancy", "answer_correctness"])
    
    # Truncate question for display
    display_df = final_df.copy()
    display_df["question"] = display_df["question"].str[:50] + "..."
    
    print(display_df[display_cols].to_string(index=False))
    print("="*80)


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Evaluate Stripe RAG Agent")
    parser.add_argument(
        "--quick", 
        action="store_true", 
        help="Run quick test (2 cases only)"
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Run only tests from specific category (e.g., 'customers', 'payment_intents')"
    )
    parser.add_argument(
        "--skip-ragas",
        action="store_true",
        help="Skip Ragas quality evaluation (only measure performance)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save evaluation reports"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Groq API key (or set GROQ_API_KEY environment variable)"
    )
    
    args = parser.parse_args()
    
    # Get test cases
    test_cases = get_test_cases(category=args.category, quick=args.quick)
    
    if not test_cases:
        print(f"[ERROR] No test cases found for category: {args.category}")
        sys.exit(1)
    
    print(f"\n🚀 Starting Stripe RAG Agent Evaluation")
    print(f"   Test cases: {len(test_cases)}")
    if args.category:
        print(f"   Category filter: {args.category}")
    
    # Run evaluation
    runner = EvaluationRunner(api_key=args.api_key)
    results = runner.run_evaluation(test_cases)
    
    # Run Ragas quality evaluation
    if args.skip_ragas:
        print("\n[INFO] Skipping Ragas evaluation (--skip-ragas flag)")
        quality_df = pd.DataFrame({
            "faithfulness": [None] * len(results["question"]),
            "answer_relevancy": [None] * len(results["question"]),
            "answer_correctness": [None] * len(results["question"]),
        })
    else:
        quality_df = run_ragas_evaluation(results)
    
    # Generate and print report
    final_df, summary, detailed_path, summary_path = generate_report(
        results, quality_df, args.output_dir
    )
    print_report(final_df, summary)
    
    print(f"\n📁 Reports saved:")
    print(f"   Detailed: {detailed_path}")
    print(f"   Summary:  {summary_path}")


if __name__ == "__main__":
    main()