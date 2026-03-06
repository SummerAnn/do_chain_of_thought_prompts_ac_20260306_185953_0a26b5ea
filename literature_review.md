# Literature Review: Do Chain-of-Thought Prompts Actually Improve Accuracy or Just Verbosity?

**Research Hypothesis**: Chain-of-thought prompting improves accuracy primarily on multi-step arithmetic and logic tasks but shows no significant improvement on single-step factual recall, while consistently increasing output length.

---

## Research Area Overview

Chain-of-Thought (CoT) prompting is a paradigm in which large language models are prompted to generate intermediate reasoning steps before producing a final answer. Introduced by Wei et al. (2022), CoT prompting has become one of the most widely studied techniques in LLM research. The core questions in this research area have evolved from "does CoT work?" (yes, on some tasks) to "when does it work?" and "at what cost in verbosity?"

The literature reveals a nuanced picture: CoT consistently improves performance on multi-step reasoning tasks (arithmetic, symbolic, commonsense) but its benefits on single-step factual recall tasks are minimal or negative. Critically, CoT always increases output length significantly—by 5x-200x compared to direct answers—raising the question of whether accuracy gains are worth the verbosity cost.

---

## Key Papers

### Paper 1: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **Authors**: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou
- **Year**: 2022
- **Source**: NeurIPS 2022 (arXiv:2201.11903)
- **Key Contribution**: Demonstrated that providing a few "chain of thought" demonstrations in the prompt significantly improves LLM performance on reasoning tasks. Coined the term and established CoT as a research paradigm.
- **Methodology**: Few-shot prompting with 8 CoT examples; evaluated on three large LMs (GPT-3, PaLM, LaMDA) at various scales. Compared standard prompting vs. CoT prompting.
- **Datasets Used**: GSM8K, SVAMP, AQuA (arithmetic); CSQA, StrategyQA (commonsense); Coin Flip, Last Letter Concatenation (symbolic); Date Understanding, Sports Understanding (BIG-bench)
- **Results**: PaLM 540B with CoT achieves 57% on GSM8K vs. 18% with standard prompting (+39pp). Strong gains on symbolic reasoning, commonsense, and arithmetic. **Critical finding: CoT only helps models >= 100B parameters.** Small models show no benefit or degraded performance.
- **Verbosity**: Paper does not analyze output token counts, but qualitative examples show CoT generates 5-10x more text.
- **Code Available**: No official code; datasets available from original sources.
- **Relevance**: Foundational work establishing that CoT benefits multi-step reasoning. Does NOT test factual recall. The selective improvement pattern supports our hypothesis.

### Paper 2: Large Language Models are Zero-Shot Reasoners
- **Authors**: Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, Yusuke Iwasawa
- **Year**: 2022
- **Source**: NeurIPS 2022 (arXiv:2205.11916)
- **Key Contribution**: Showed that appending "Let's think step by step" (zero-shot CoT) elicits reasoning chains without any few-shot examples, achieving competitive performance with few-shot CoT.
- **Methodology**: Zero-shot prompting with a simple trigger phrase. Two-stage process: (1) generate reasoning, (2) extract answer.
- **Datasets Used**: MultiArith, GSM8K, AQUA-RAT, SingleEq (math); Letter, Coin Flip (symbolic); Last Letter (other); CommonsenseQA, Strategy QA (commonsense); Date, Tracking, Sports (BIG-bench)
- **Results**: Zero-shot CoT improves from 17.7% to 78.7% on MultiArith with InstructGPT. Competitive with few-shot CoT across most benchmarks. **Zero-shot CoT does NOT improve performance on single-step QA tasks.**
- **Code Available**: No
- **Relevance**: Confirms that CoT improvement is about task type, not just prompting format. Zero-shot CoT provides a useful baseline that's easy to implement in experiments.

### Paper 3: Self-Consistency Improves Chain of Thought Reasoning in Language Models
- **Authors**: Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou
- **Year**: 2022/2023
- **Source**: ICLR 2023 (arXiv:2203.11171)
- **Key Contribution**: Self-consistency: sample multiple diverse reasoning paths via CoT, take majority vote. Substantial accuracy gains over standard CoT.
- **Methodology**: Sample k reasoning paths at temperature > 0, take majority vote on final answer. Evaluated on arithmetic, commonsense, and symbolic tasks.
- **Datasets Used**: GSM8K, SVAMP, AQuA, MultiArith, SingleEq; StrategyQA, ARC-c; Letter; BIG-bench; CommonSenseQA
- **Results**: GSM8K: +17.9% over CoT; SVAMP: +11.0%; AQuA: +12.2%; StrategyQA: +6.4%; ARC-c: +3.9%. Self-consistency provides consistent improvements on reasoning tasks.
- **Verbosity Impact**: Self-consistency generates k×(CoT tokens) since it samples multiple times, significantly increasing compute cost.
- **Code Available**: No official code
- **Relevance**: Important upper bound for reasoning accuracy. Demonstrates that multi-step reasoning tasks have significant headroom for improvement through better sampling.

### Paper 4: Least-to-Most Prompting Enables Complex Reasoning
- **Authors**: Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, Ed Chi
- **Year**: 2022/2023
- **Source**: ICLR 2023 (arXiv:2205.10625)
- **Key Contribution**: Decomposition-then-solve approach: first break problem into sub-problems, then solve sequentially. Solves tasks where CoT fails (long compositional generalization).
- **Methodology**: Two-stage prompting: (1) list sub-problems, (2) solve each sub-problem using prior answers.
- **Datasets Used**: SCAN (compositional generalization), DROP, MATH, GSM8K
- **Results**: 99.7% on SCAN where standard CoT fails. Demonstrates that problem complexity (not just multi-step nature) determines CoT's limits.
- **Code Available**: No
- **Relevance**: Shows that CoT is a specific approach to multi-step reasoning, not the only one. Helps understand *when* and *why* CoT helps.

### Paper 5: Chain of Draft: Thinking Faster by Writing Less
- **Authors**: Silei Xu, Wenhao Xie, Lingxiao Zhao, Pengcheng He
- **Year**: 2025
- **Source**: arXiv:2502.18600
- **Key Contribution**: Proposes Chain of Draft (CoD): prompts LLMs to generate minimal intermediate reasoning steps ("5 words per step"). Shows that verbosity and accuracy are separable—CoD achieves similar accuracy as CoT with 7.6-20% of the tokens.
- **Methodology**: Few-shot prompting with concise examples. Evaluated on GPT-4o and Claude 3.5 Sonnet. Compared Standard (baseline), CoT, and CoD prompting.
- **Datasets Used**: GSM8K (arithmetic), Date Understanding and Sports Understanding from BIG-bench (commonsense), Coin Flip (symbolic)
- **Results**:
  - GSM8K: Standard 53.3%, CoT 95.4% (205 tokens), CoD 91.1% (44 tokens) — 80% token reduction
  - Date Understanding: CoT 90.2% (76 tokens), CoD 88.1% (30 tokens) — 60% token reduction
  - Sports Understanding: CoT 87.0% (172 tokens), CoD 89.7% (31 tokens) — 82% token reduction
  - Coin Flip: Both CoT and CoD achieve 100%
- **Code Available**: Yes — https://github.com/sileix/chain-of-draft
- **Relevance**: DIRECTLY relevant. Provides evidence that CoT verbosity is not necessary for accuracy gains on reasoning tasks. This is the key paper for the verbosity-accuracy relationship.

### Paper 6: Evaluating Step-by-Step Reasoning Traces: A Survey (2025)
- **Authors**: Multiple (survey)
- **Year**: 2025
- **Source**: arXiv:2502.12289
- **Key Contribution**: Comprehensive survey of methods for evaluating CoT reasoning chains, beyond just final answer accuracy.
- **Methodology**: Survey of evaluation frameworks for reasoning traces.
- **Key Findings**: Points out that models can reach correct answers via incorrect reasoning (and vice versa). Evaluation of intermediate steps reveals qualitatively different behaviors than final accuracy.
- **Relevance**: Important for understanding what we're measuring when we evaluate CoT. Token count is one dimension; reasoning quality is another.

### Paper 7: SVAMP: Simple Variations on Arithmetic Math Word Problems
- **Authors**: Arkil Patel, Satwik Bhatt, Balaraman Ravindran
- **Year**: 2021
- **Source**: NAACL 2021 (arXiv:2103.07191)
- **Key Contribution**: Created SVAMP benchmark showing that models rely on shallow heuristics rather than true mathematical reasoning.
- **Methodology**: Created structurally varied versions of simple math problems. Models that solved original problems failed on variations.
- **Datasets Used**: SVAMP (challenge set of 1,000 problems)
- **Results**: Even state-of-the-art models in 2021 achieved only 57-63% accuracy on SVAMP despite high performance on simpler benchmarks. Models exploit surface patterns.
- **Code Available**: Yes — https://github.com/arkilpatel/SVAMP
- **Relevance**: Motivates why CoT may help on reasoning tasks specifically (it forces the model to work through logic rather than pattern match).

### Paper 8: The Decreasing Value of Chain of Thought in Prompting
- **Authors**: Lennart Meincke, Ethan Mollick, Lilach Mollick, Dan Shapiro
- **Year**: 2025
- **Source**: Wharton Generative AI Labs / SSRN:5285532
- **Key Contribution**: Systematic study showing that CoT's value is diminishing for modern LLMs, especially reasoning-capable models.
- **Methodology**: Compared CoT vs. direct prompting across multiple model types. Measured accuracy, token usage, and latency.
- **Key Findings**:
  - CoT requests take 35-600% longer (5-15 seconds) than direct requests
  - For non-reasoning models: CoT improves average performance by a small amount but introduces variability
  - For reasoning models (o3-mini, o4-mini): CoT adds only 2.9-3.1% improvement with 20-80% increase in time
  - Many models perform CoT-like reasoning by default, making explicit CoT prompting redundant
- **Relevance**: Confirms that CoT's accuracy benefits are limited and task-dependent, while verbosity costs are consistent. Supports our hypothesis from the cost perspective.

---

## Common Methodologies

### Evaluation Approaches
1. **Few-shot CoT**: Provide 3-8 demonstration examples with reasoning chains; evaluate on benchmark test set
2. **Zero-shot CoT**: Append "Let's think step by step" to prompt; no demonstrations needed
3. **Self-consistency CoT**: Sample multiple CoT paths, take majority vote
4. **Direct prompting (baseline)**: No reasoning, just answer

### Metrics
- **Exact match accuracy**: Percentage of correct final answers
- **Token count**: Total output tokens as verbosity measure
- **Latency**: Wall clock time for inference
- **Step validity**: Whether intermediate reasoning steps are correct (subset of papers)

---

## Standard Baselines

| Baseline | Description | Typical Performance Range |
|----------|-------------|--------------------------|
| Standard (direct) | No reasoning prompt | GSM8K: 15-65% (model-dependent) |
| Zero-shot CoT | "Let's think step by step" | GSM8K: 40-90% (model-dependent) |
| Few-shot CoT | 8 CoT demonstrations | GSM8K: 55-96% (model-dependent) |
| Self-consistency | Majority vote over k CoT samples | GSM8K: 74-97% (model-dependent) |

---

## Evaluation Metrics

| Task Type | Primary Metric | Notes |
|-----------|---------------|-------|
| Arithmetic (GSM8K, SVAMP) | Exact match on final number | Use pattern matching to extract #### answer |
| Commonsense MCQ (CommonsenseQA) | Multiple-choice accuracy | Compare to labeled answerKey |
| Factual recall (TriviaQA) | Exact match / contains answer | Check against normalized_aliases |
| Verbosity (ALL tasks) | Token count per response | Count output tokens for each prompt type |

---

## Datasets in the Literature

| Dataset | Papers Using It | Task Type | Why Relevant |
|---------|----------------|-----------|--------------|
| GSM8K | Wei 2022, Wang 2022, Zhou 2022, Xu 2025 | Multi-step arithmetic | Primary CoT benchmark; shows largest CoT gains |
| SVAMP | Wei 2022, Wang 2022 | Arithmetic with structural variations | Tests real reasoning vs. surface patterns |
| AQuA-RAT | Wei 2022, Wang 2022 | Algebraic MCQ | Multi-step algebraic reasoning |
| CommonsenseQA | Wei 2022, Kojima 2022 | Commonsense MCQ | Moderate CoT gains (commonsense) |
| StrategyQA | Wei 2022, Wang 2022 | Multi-hop commonsense | Multi-step commonsense |
| TriviaQA | Not in core CoT papers | Single-step factual recall | KEY CONTROL: expected NO CoT gain |
| BIG-bench (Date, Sports) | Wei 2022, Xu 2025 | Commonsense/symbolic | Varied reasoning types |
| Coin Flip | Wei 2022, Xu 2025 | Symbolic | Pure symbolic reasoning |

---

## Gaps and Opportunities

### Gap 1: Verbosity as Outcome Variable
Most CoT papers focus exclusively on accuracy. Only Chain of Draft (2025) and the Decreasing Value paper (2025) explicitly measure token counts as a dependent variable. **Our research directly addresses this gap by measuring verbosity systematically across task types.**

### Gap 2: Factual Recall Comparison
The original CoT papers do not evaluate on pure factual recall tasks (TriviaQA, Natural Questions). They specifically focus on reasoning tasks. **Our research fills this gap by using TriviaQA as a controlled comparison dataset.**

### Gap 3: Task-Type Analysis
Most papers evaluate CoT on a fixed set of reasoning tasks. A systematic comparison across task types (arithmetic, commonsense, factual) within a single experiment design is underexplored. **Our research design directly addresses this.**

### Gap 4: Modern Models
Many baseline results are from 2022 (GPT-3, PaLM). The Decreasing Value paper (2025) shows that CoT's value is shrinking for modern models. **Our research can contribute updated findings for current models.**

---

## Recommendations for Our Experiment

### Recommended Datasets
1. **Primary (arithmetic)**: GSM8K test set (1,319 examples)
   - Justification: Gold standard for multi-step arithmetic CoT evaluation; largest CoT gains reported here
2. **Secondary (arithmetic)**: SVAMP test set (300 examples)
   - Justification: Tests whether CoT helps overcome shallow heuristics, not just harder problems
3. **Commonsense**: CommonsenseQA validation set (1,221 examples)
   - Justification: Moderate CoT gains expected; multi-step but not arithmetic
4. **Control (factual)**: TriviaQA sample (500-1,000 examples)
   - Justification: Single-step factual recall; hypothesis predicts NO accuracy gain but YES verbosity increase

### Recommended Baselines
1. **Standard prompting** (direct answer, no reasoning)
2. **Zero-shot CoT** ("Let's think step by step")
3. **Few-shot CoT** (3-5 demonstration examples with reasoning)
4. **Chain of Draft** (if testing verbosity reduction; requires few-shot examples)

### Recommended Metrics
1. **Accuracy**: Exact match on final answer for each task
2. **Output token count**: Measure verbosity for each prompt condition
3. **Accuracy improvement from CoT**: Δ accuracy = CoT accuracy - Standard accuracy
4. **Verbosity increase from CoT**: Δ tokens = CoT tokens - Standard tokens

### Methodological Considerations
- Use consistent model (e.g., Claude claude-haiku-4-5 or GPT-4o-mini) across all tasks to control for model effects
- Use temperature=0 for reproducibility (or fix seed)
- Match demonstration examples in few-shot CoT to task domain
- Use at least 100-200 examples per task for statistical reliability
- Report confidence intervals or error bars
- The hypothesis predicts an interaction effect: CoT × Task_Type on accuracy; a main effect of CoT on verbosity

### Key Prediction to Test
- **H1**: Significant accuracy gain for CoT on GSM8K, SVAMP, CommonsenseQA
- **H2**: No significant accuracy gain for CoT on TriviaQA
- **H3**: Consistent verbosity increase (higher token count) for CoT across ALL task types
- **H4** (secondary): Verbosity increase is similar across task types even when accuracy gain varies

---

## Summary Table of Evidence

| Evidence | Supports Hypothesis? | Source |
|----------|---------------------|--------|
| CoT boosts GSM8K by 39pp (PaLM 540B) | Yes (H1) | Wei 2022 |
| CoT doesn't help small models | Partial (scale matters) | Wei 2022 |
| Zero-shot CoT fails on single-step QA | Yes (H2) | Kojima 2022 |
| CoT requests take 35-600% longer | Yes (H3) | Meincke 2025 |
| CoD reduces tokens 80% with ~5% accuracy cost | Yes (H3, H4) | Xu 2025 |
| Self-consistency shows large gains on reasoning | Yes (H1) | Wang 2022 |
| SVAMP shows models use shallow heuristics | Context (why CoT helps) | Patel 2021 |
