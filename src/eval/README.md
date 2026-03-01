# Stripe RAG Agent Evaluation Framework

This evaluation framework measures both **quality** and **performance** of the RAG agent.

## Quick Start

```bash
# Run full evaluation
python -m src.eval.eval_llm

# Run quick test (2 cases)
python -m src.eval.eval_llm --quick

# Run specific category
python -m src.eval.eval_llm --category customers

# Skip Ragas (performance only)
python -m src.eval.eval_llm --skip-ragas
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EVALUATION PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐     ┌──────────────────┐     ┌─────────────────────┐     │
│   │  Test Cases  │────▶│   Agent Graph    │────▶│  Results Collector  │     │
│   │  (questions  │     │   (your RAG)     │     │  (answers, context, │     │
│   │   + ground   │     │                  │     │   latency, tokens)  │     │
│   │   truth)     │     │                  │     │                     │     │
│   └──────────────┘     └──────────────────┘     └──────────┬──────────┘     │
│                                                            │                 │
│                                                            ▼                 │
│                               ┌────────────────────────────────────────┐     │
│                               │         METRICS COMPUTATION            │     │
│                               ├────────────────────────────────────────┤     │
│                               │                                        │     │
│   ┌───────────────────┐       │   ┌─────────────────────────────────┐  │     │
│   │  Performance      │◀──────│───│  Latency, Tokens, Tool Calls    │  │     │
│   │  (measured)       │       │   └─────────────────────────────────┘  │     │
│   └───────────────────┘       │                                        │     │
│                               │   ┌─────────────────────────────────┐  │     │
│   ┌───────────────────┐       │   │  Ragas LLM-as-Judge             │  │     │
│   │  Quality (Ragas)  │◀──────│───│  - Faithfulness                 │  │     │
│   │  (LLM-judged)     │       │   │  - Answer Relevancy             │  │     │
│   └───────────────────┘       │   │  - Answer Correctness           │  │     │
│                               │   └─────────────────────────────────┘  │     │
│                               └────────────────────────────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## How Model Answers Feed Into Evaluation

The evaluation process works in 3 stages:

### Stage 1: Run Agent

```python
# For each test question, we invoke the full agent graph
initial_state = {
    "messages": [HumanMessage(content="What parameters to create a customer?")],
    "tool_call_budget": 0,
    ...
}
output_state = app_graph.invoke(initial_state)
```

### Stage 2: Extract Results

```python
# From the output state, we extract:

# 1. ANSWER: Final AIMessage content
answer = output_state["messages"][-1].content

# 2. CONTEXTS: Content from ToolMessages (retrieved chunks)
contexts = [m.content for m in messages if isinstance(m, ToolMessage)]

# 3. TOKENS: From AIMessage usage_metadata
for m in messages:
    if isinstance(m, AIMessage) and m.usage_metadata:
        total_tokens += m.usage_metadata.get("total_tokens", 0)
```

### Stage 3: Quality Evaluation (Ragas)

```python
# Ragas uses GPT-4 as a "judge" to evaluate:

# FAITHFULNESS: Is the answer grounded in the retrieved contexts?
# - Compares answer statements to context chunks
# - Score: 0 (hallucinated) to 1 (fully grounded)

# ANSWER RELEVANCY: Does it actually answer the question?
# - Evaluates if answer addresses the user's query
# - Score: 0 (off-topic) to 1 (directly relevant)

# ANSWER CORRECTNESS: How complete is it vs ground truth?
# - Compares answer to your expected ground_truth
# - Score: 0 (incorrect) to 1 (fully correct)
```

## Metrics Explained

### Performance Metrics (Measured Directly)

| Metric            | Description               | How Measured                                   |
| ----------------- | ------------------------- | ---------------------------------------------- |
| `latency_seconds` | End-to-end response time  | `time.time()` around `app_graph.invoke()`      |
| `total_tokens`    | Total LLM tokens used     | Sum of `AIMessage.usage_metadata.total_tokens` |
| `input_tokens`    | Prompt tokens             | From `usage_metadata.input_tokens`             |
| `output_tokens`   | Completion tokens         | From `usage_metadata.output_tokens`            |
| `tool_calls`      | Number of retrieval calls | Count of `ToolMessage` in output               |

### Quality Metrics (LLM-Judged via Ragas)

| Metric               | Question Answered           | Score Range                 |
| -------------------- | --------------------------- | --------------------------- |
| `faithfulness`       | Did it hallucinate?         | 0-1 (1 = no hallucination)  |
| `answer_relevancy`   | Did it answer the question? | 0-1 (1 = directly relevant) |
| `answer_correctness` | How complete vs expected?   | 0-1 (1 = fully correct)     |

## Adding Test Cases

Edit `src/eval/test_cases.py`:

```python
MY_TEST_CASES = [
    {
        "question": "Your test question",
        "ground_truth": "The expected correct answer...",
        "category": "my_category",
        "expected_api_classes": ["CUSTOMERS"]  # Optional
    },
]
```

### Writing Good Ground Truth

1. **Be specific**: Include key facts, parameters, endpoints
2. **Be comprehensive**: Cover what a complete answer should include
3. **Be accurate**: Base on your actual documentation
4. **Not too long**: Focus on key information, not every detail

## Environment Setup

### Required API Keys

```bash
# For your RAG agent (Groq)
export GROQ_API_KEY="your-groq-key"

# For Ragas judge LLM (OpenAI)
export OPENAI_API_KEY="your-openai-key"
```

### Install Dependencies

```bash
pip install ragas datasets pandas
```

## Output Files

Reports are saved to `data/eval/`:

- `eval_report_YYYYMMDD_HHMMSS.csv`: Detailed per-question results
- `eval_summary_YYYYMMDD_HHMMSS.csv`: Aggregate statistics

## Example Output

```
================================================================================
 EVALUATION REPORT
================================================================================

📊 SUMMARY STATISTICS
----------------------------------------
  Total test cases:      8
  Avg latency:           3.45s
  Avg tokens:            2150
  Avg tool calls:        2.3

  📈 Quality Metrics (0-1 scale):
     Faithfulness:       0.923
     Relevancy:          0.891
     Correctness:        0.856

📝 PER-QUESTION RESULTS
--------------------------------------------------------------------------------
question                                       latency_seconds  total_tokens  tool_calls  faithfulness  answer_relevancy  answer_correctness
What are the required parameters to create...  2.34             1850          2           0.95          0.92              0.88
How do I retrieve a customer by ID?...         1.89             1420          1           0.98          0.95              0.91
...
```

## Interpreting Results

### Good Scores

- Faithfulness > 0.9: Minimal hallucination
- Relevancy > 0.85: Answers are on-topic
- Correctness > 0.8: Answers are comprehensive

### Warning Signs

- Faithfulness < 0.7: Agent may be hallucinating
- High latency + low tool_calls: Possibly stuck in loops
- Low correctness with high faithfulness: Context retrieval may be poor

## Programmatic Usage

```python
from src.eval import EvaluationRunner, get_test_cases, run_ragas_evaluation

# Get test cases
test_cases = get_test_cases(category="customers")

# Run evaluation
runner = EvaluationRunner()
results = runner.run_evaluation(test_cases)

# Get quality scores
quality_df = run_ragas_evaluation(results)

# Access individual results
for i, question in enumerate(results["question"]):
    print(f"Q: {question}")
    print(f"A: {results['answer'][i]}")
    print(f"Latency: {results['latency_seconds'][i]}s")
```
