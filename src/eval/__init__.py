# src/eval/__init__.py
"""
Evaluation Framework for Stripe RAG Agent

This module provides tools for evaluating the RAG agent's performance and quality.

Components:
    - eval_llm.py: Main evaluation runner
    - test_cases.py: Test case definitions

Usage:
    # Run from project root
    python -m src.eval.eval_llm
    
    # Or import programmatically
    from src.eval import EvaluationRunner, get_test_cases
"""

from src.eval.eval_llm import EvaluationRunner, run_ragas_evaluation, generate_report
from src.eval.test_cases import get_test_cases, ALL_TEST_CASES, QUICK_TEST_CASES

__all__ = [
    "EvaluationRunner",
    "run_ragas_evaluation",
    "generate_report",
    "get_test_cases",
    "ALL_TEST_CASES",
    "QUICK_TEST_CASES",
]
