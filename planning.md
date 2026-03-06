# Research Planning: Do Chain-of-Thought Prompts Actually Improve Accuracy or Just Verbosity?

## Motivation & Novelty Assessment

### Why This Research Matters
Chain-of-thought (CoT) prompting has become ubiquitous in LLM deployments, but practitioners face a real trade-off: CoT increases API costs (more output tokens = higher billing), latency, and response length. Understanding when CoT genuinely improves accuracy—versus when it merely adds verbose tokens—allows practitioners to deploy CoT selectively, reducing costs while preserving quality where it matters.

### Gap in Existing Work
Based on the literature review: (1) Foundational CoT papers (Wei 2022, Kojima 2022) test only reasoning tasks, never factual recall; (2) Verbosity is rarely measured as an outcome variable—only Chain of Draft (2025) and Meincke (2025) do this explicitly; (3) No single study compares CoT's accuracy AND verbosity effect across all four task types (arithmetic, commonsense, factual, symbolic) with a unified experiment. Our research fills this gap.

### Our Novel Contribution
A systematic, controlled comparison of Standard vs. Zero-shot CoT vs. Few-shot CoT across four task categories (arithmetic, commonsense, factual recall) measuring both accuracy improvement AND verbosity increase, with statistical tests for an interaction effect (task type × prompt style on accuracy) and a main effect (prompt style on verbosity). Results will provide a direct cost-benefit framework for CoT deployment decisions.

### Experiment Justification
- **Exp 1 (GSM8K)**: Multi-step arithmetic; hypothesis predicts large CoT accuracy gain. Primary test of H1.
- **Exp 2 (SVAMP)**: Arithmetic word problems with structural variations; tests whether CoT gain is robust or shallow.
- **Exp 3 (CommonsenseQA)**: Multi-choice commonsense; moderate CoT gain expected. Tests H1 at different task difficulty.
- **Exp 4 (TriviaQA)**: Single-step factual recall; hypothesis predicts NO accuracy gain. Primary test of H2 (the null).
- **Verbosity analysis (all tasks)**: Measures output token counts across all conditions to test H3 (consistent verbosity increase regardless of task type).

---

## Research Question
**Does chain-of-thought prompting improve accuracy primarily on multi-step reasoning tasks (arithmetic, logic) but not on single-step factual recall, while consistently increasing output length across all task types?**

## Background and Motivation
CoT prompting (Wei et al., 2022) generates intermediate reasoning steps before final answers. It has been shown to dramatically improve performance on multi-step arithmetic (+39pp on GSM8K for PaLM 540B). However, CoT always produces more tokens—5x-200x more than direct answers. In 2025, API costs are directly tied to token counts, and latency matters for user-facing applications. The critical question for practitioners: is the accuracy improvement from CoT worth the verbosity cost, and does it depend on task type?

## Hypothesis Decomposition

**H1 (Reasoning accuracy)**: CoT (zero-shot and few-shot) significantly improves accuracy on multi-step arithmetic (GSM8K, SVAMP) and commonsense (CommonsenseQA) tasks vs. standard prompting.

**H2 (Factual null)**: CoT does NOT significantly improve accuracy on single-step factual recall (TriviaQA). Any improvement is within noise (< 3pp).

**H3 (Verbosity main effect)**: CoT increases output token count significantly across ALL task types regardless of accuracy benefit. Effect is consistent across arithmetic, commonsense, and factual tasks.

**H4 (Interaction)**: There is a significant interaction between prompt type (CoT vs. Standard) and task type on accuracy, but NO such interaction on verbosity. Verbosity increase is task-agnostic; accuracy gain is task-specific.

---

## Proposed Methodology

### Approach
Use real LLM API calls (Claude Haiku claude-haiku-4-5, a capable but cost-effective model) to compare three prompting strategies across four task types. Measure both accuracy and token counts for every prediction. Use statistical tests (McNemar's test for accuracy differences, paired t-tests for token counts, interaction tests for H4).

### Experimental Steps

1. **Load datasets** from pre-downloaded Arrow files using HuggingFace `datasets` library
2. **Sample** 200 examples per task (800 total) for balanced, statistically reliable estimates with manageable API cost (~$5-15 total)
3. **Define prompts**:
   - Standard: "Question: {q}\nAnswer:"
   - Zero-shot CoT: "Question: {q}\nLet's think step by step.\nAnswer:"
   - Few-shot CoT: 3 task-specific examples with reasoning chains + "Question: {q}\nLet's think step by step."
4. **Call Claude API** for each (task, prompt_type, example) combination; log raw response and token counts
5. **Parse answers** using task-specific extractors (regex for numbers in GSM8K/SVAMP, letter for CommonsenseQA, string match for TriviaQA)
6. **Compute metrics**: accuracy per (task, prompt), mean token counts per (task, prompt)
7. **Statistical tests**: McNemar's test for pairwise accuracy comparisons, paired t-tests for token counts, two-way ANOVA or regression for interaction H4
8. **Visualize**: Bar charts of accuracy by task/prompt, token count distributions, ΔAcc vs. ΔTokens scatter

### Baselines
| Baseline | Description | Rationale |
|----------|-------------|-----------|
| Standard prompting | No reasoning, direct answer | Simplest baseline; measures CoT's incremental value |
| Zero-shot CoT | "Let's think step by step" | Easy to deploy; no examples needed; canonical CoT baseline |
| Few-shot CoT | 3 examples with reasoning | Strongest CoT variant; shows upper bound of CoT benefit |

### Evaluation Metrics
| Metric | Definition | Why |
|--------|-----------|-----|
| Accuracy | % correct answers (exact match) | Primary outcome; task-specific extraction |
| Output token count | Tokens in model's response | Verbosity measure; correlates with cost |
| ΔAcc = CoT_acc - Standard_acc | Accuracy improvement from CoT | Tests H1, H2 |
| ΔTokens = CoT_tokens - Standard_tokens | Token increase from CoT | Tests H3 |
| Token efficiency = ΔAcc / ΔTokens | Accuracy gain per additional token | Practical cost-benefit metric |

### Statistical Analysis Plan
- **Accuracy comparisons**: McNemar's test (paired, binary outcomes) between Standard vs. Zero-shot CoT and Standard vs. Few-shot CoT per task; p < 0.05 with Bonferroni correction (8 comparisons → α = 0.00625)
- **Token count comparisons**: Paired Wilcoxon signed-rank test (token counts are non-normal) between Standard vs. CoT per task
- **Interaction test**: Two-way mixed ANOVA with task type and prompt type as factors; test for Task × Prompt interaction on accuracy
- **Effect size**: Cohen's d for token differences; ΔAcc (percentage points) as practical effect

---

## Expected Outcomes

| Task | Expected ΔAcc (Few-shot CoT) | Expected ΔTokens |
|------|------------------------------|------------------|
| GSM8K | +20 to +40pp | +150-250 tokens |
| SVAMP | +10 to +20pp | +100-200 tokens |
| CommonsenseQA | +3 to +10pp | +50-150 tokens |
| TriviaQA | 0 to -2pp (null result) | +50-150 tokens |

Results supporting hypothesis: significant positive ΔAcc for arithmetic tasks, non-significant ΔAcc for TriviaQA, significant ΔTokens for ALL tasks.

---

## Timeline and Milestones
1. **Environment + dataset loading** (30 min)
2. **Implement prompt templates and evaluation harness** (45 min)
3. **Run API experiments** (60-90 min, ~3200 API calls total: 800 × 4 conditions)
4. **Analyze results + visualizations** (45 min)
5. **Write REPORT.md** (30 min)

---

## Potential Challenges
- **Rate limits**: Claude API may throttle; handle with exponential backoff + batching
- **Answer extraction**: CoT responses embed the answer in verbose reasoning; need robust regex
- **API cost**: ~3200 calls × avg 200 tokens output ≈ 640K tokens; at Haiku prices ~$1-3 total
- **Accuracy ceiling**: Modern Claude models may already be near-perfect on easier tasks, reducing observable CoT gain

## Success Criteria
- All 4 hypothesis tests run with p-values reported
- At least H1 and H3 confirmed (strong prior from literature)
- H2 (TriviaQA null) evaluated with sufficient power (200 examples)
- ΔAcc vs. ΔTokens tradeoff visualized and interpretable
- REPORT.md documents actual experimental results
