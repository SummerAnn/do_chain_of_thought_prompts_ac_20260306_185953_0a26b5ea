# Resources Catalog

## Summary

This document catalogs all resources gathered for the research project:
**"Do Chain-of-Thought Prompts Actually Improve Accuracy or Just Verbosity?"**

All resources are locally available in this workspace.

---

## Papers

Total papers downloaded: **8**

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Chain-of-Thought Prompting Elicits Reasoning | Wei et al. | 2022 | `papers/2201.11903_wei2022_chain_of_thought.pdf` | Foundational CoT paper; GSM8K +39pp |
| Large Language Models are Zero-Shot Reasoners | Kojima et al. | 2022 | `papers/2205.11916_kojima2022_zero_shot_reasoners.pdf` | Zero-shot CoT ("Let's think step by step") |
| Self-Consistency Improves Chain of Thought | Wang et al. | 2022 | `papers/2203.11171_wang2022_self_consistency.pdf` | Majority vote CoT; GSM8K +17.9pp |
| Least-to-Most Prompting | Zhou et al. | 2022 | `papers/2205.10625_zhou2022_least_to_most.pdf` | Decomposition-based CoT extension |
| Chain of Draft: Thinking Faster by Writing Less | Xu et al. | 2025 | `papers/2502.18600_xu2025_chain_of_draft.pdf` | 80% token reduction with ~5% accuracy cost |
| Evaluating Step-by-Step Reasoning Traces | Survey | 2025 | `papers/2502.12289_survey_evaluating_reasoning_traces.pdf` | Survey of CoT evaluation methods |
| SVAMP Dataset Paper | Patel et al. | 2021 | `papers/2103.07191_patel2021_svamp.pdf` | Shallow heuristics in math models |
| Large Language Models Are Reasoning Teachers | Ho et al. | 2022 | `papers/2109.01652_ho2022_large_language_models_trained.pdf` | CoT distillation to small models |

See `papers/README.md` for detailed descriptions.

---

## Datasets

Total datasets downloaded: **4**

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| GSM8K | openai/gsm8k | 8,792 total | Multi-step arithmetic | `datasets/gsm8k/` | PRIMARY benchmark; 7473 train, 1319 test |
| SVAMP | ChilleD/SVAMP | 1,000 total | Arithmetic MWP | `datasets/svamp/` | Tests reasoning depth; 700 train, 300 test |
| CommonsenseQA | tau/commonsense_qa | 12,102 total | Commonsense MCQ | `datasets/commonsenseqa/` | Multi-step commonsense; 9741 train, 1221 val |
| TriviaQA | mandarjoshi/trivia_qa | 5,000 (sample) | Factual recall | `datasets/triviaqa/` | CONTROL: single-step factual recall |

See `datasets/README.md` for detailed descriptions and download instructions.

### Data Format Notes
- **GSM8K**: `question` (str) + `answer` (str with #### final answer)
- **SVAMP**: `Body` + `Question` + `Answer` (numeric) + `Equation` + `Type`
- **CommonsenseQA**: `question` + `choices` (5-choice MCQ) + `answerKey`
- **TriviaQA**: `question` + `answer` (dict with aliases and normalized forms)

---

## Code Repositories

Total repositories cloned: **2**

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| chain-of-thought-hub | github.com/FranxYao/chain-of-thought-hub | LLM reasoning benchmarking | `code/chain-of-thought-hub/` | GSM8K, MATH, BBH, MMLU evaluation scripts |
| chain-of-draft | github.com/sileix/chain-of-draft | CoT vs CoD comparison framework | `code/chain-of-draft/` | Direct Standard vs CoT vs CoD comparison |

See `code/README.md` for detailed descriptions.

---

## Resource Gathering Notes

### Search Strategy
1. Used web search to identify foundational CoT papers (Wei 2022, Kojima 2022, Wang 2022)
2. Searched for verbosity-specific papers (Chain of Draft, Decreasing Value of CoT)
3. Searched for relevant evaluation benchmarks (GSM8K, SVAMP, CommonsenseQA, TriviaQA)
4. Identified GitHub repositories for evaluation code

### Selection Criteria
- **Papers**: Focus on foundational CoT papers + recent verbosity analysis papers
- **Datasets**: Selected to cover 3 task types: (1) multi-step arithmetic, (2) commonsense reasoning, (3) single-step factual recall
- **Code**: Prioritized repositories with direct comparison of Standard vs. CoT prompting

### Challenges Encountered
- Paper-finder service was not available; used web search manually instead
- TriviaQA download required streaming due to large size; downloaded 5,000 sample subset
- SSRN paper (Meincke 2025 "Decreasing Value of CoT") could not be downloaded as PDF; summarized from abstract

### Gaps and Workarounds
- Meincke et al. (2025) SSRN paper not freely available as PDF; sufficient info from abstract and blog post
- No pre-existing code for comparing CoT vs. no-CoT specifically on TriviaQA; will need to extend chain-of-draft code

---

## Recommendations for Experiment Design

### 1. Primary Dataset(s)
- **GSM8K** (test set, 1,319 examples): Main benchmark for multi-step arithmetic. Expected large CoT accuracy gain.
- **TriviaQA** (500-1,000 examples): Control dataset for single-step factual recall. Expected NO accuracy gain.

### 2. Secondary Datasets
- **SVAMP** (test set, 300 examples): Tests robustness of arithmetic reasoning.
- **CommonsenseQA** (validation set, 1,221 examples): Bridges arithmetic and factual tasks.

### 3. Baseline Methods
1. **Standard prompting** (baseline): Direct answer, no reasoning
2. **Zero-shot CoT**: Append "Let's think step by step"
3. **Few-shot CoT**: 3-5 task-specific demonstrations with reasoning chains

### 4. Evaluation Metrics
- **Accuracy**: Exact match on final answer (or contains-answer for TriviaQA)
- **Output token count**: Verbosity measurement for each prompt condition
- **Accuracy delta (ΔAcc)**: CoT accuracy - Standard accuracy (tests H1/H2)
- **Verbosity delta (ΔTokens)**: CoT tokens - Standard tokens (tests H3)

### 5. Code to Adapt/Reuse
- **Primary**: `code/chain-of-draft/` — Already implements Standard vs. CoT vs. CoD comparison with token counting. Supports GPT and Claude APIs.
  - Extend `tasks/` to include TriviaQA and CommonsenseQA
  - Use `llm_client.py` for API calls
  - Adapt `evaluate.py` for new tasks
- **Reference**: `code/chain-of-thought-hub/gsm8k/` — Reference implementations for GSM8K evaluation

### 6. Experimental Configuration
```python
# Recommended configuration
TASKS = ["gsm8k", "svamp", "commonsenseqa", "triviaqa"]
PROMPTS = ["standard", "zero_shot_cot", "few_shot_cot"]
MODELS = ["claude-haiku-4-5-20251001"]  # or gpt-4o-mini
SAMPLE_SIZE = {
    "gsm8k": 500,          # from 1319 test
    "svamp": 300,           # all test
    "commonsenseqa": 500,   # from 1221 val
    "triviaqa": 500,        # from 5000 sample
}
METRICS = ["accuracy", "output_token_count"]
```

### 7. Expected Results
Based on literature:

| Task | Expected ΔAcc (CoT vs. Standard) | Expected ΔTokens |
|------|----------------------------------|------------------|
| GSM8K | Large (+20 to +40pp) | Large (+150-200 tokens) |
| SVAMP | Moderate (+10 to +20pp) | Large (+100-150 tokens) |
| CommonsenseQA | Small-Moderate (+3 to +10pp) | Large (+50-100 tokens) |
| TriviaQA | Negligible (0 to -2pp) | Large (+50-100 tokens) |

**Key prediction**: Verbosity increase should be large and consistent across ALL tasks, while accuracy improvement should be significant only for reasoning-heavy tasks.

---

## Environment Setup

To reproduce this research:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install pypdf requests httpx datasets

# Download datasets (if not already present)
python -c "
from datasets import load_dataset
load_dataset('openai/gsm8k', 'main').save_to_disk('datasets/gsm8k')
load_dataset('ChilleD/SVAMP').save_to_disk('datasets/svamp')
load_dataset('tau/commonsense_qa').save_to_disk('datasets/commonsenseqa')
load_dataset('mandarjoshi/trivia_qa', 'rc.nocontext', split='train[:5000]').save_to_disk('datasets/triviaqa')
"
```
