# Downloaded Papers

Papers downloaded for research on: "Do Chain-of-Thought Prompts Actually Improve Accuracy or Just Verbosity?"

## 1. Wei et al. (2022) - Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **File**: `2201.11903_wei2022_chain_of_thought.pdf`
- **Authors**: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou
- **Year**: 2022
- **Venue**: NeurIPS 2022
- **arXiv**: https://arxiv.org/abs/2201.11903
- **Why relevant**: The foundational paper proposing CoT prompting. Shows CoT improves performance on arithmetic (GSM8K), commonsense, and symbolic reasoning tasks. Key finding: CoT is an emergent ability only for models >=100B parameters. Benchmarks used: GSM8K, SVAMP, AQuA, CSQA, StrategyQA, BIG-bench tasks.

## 2. Kojima et al. (2022) - Large Language Models are Zero-Shot Reasoners
- **File**: `2205.11916_kojima2022_zero_shot_reasoners.pdf`
- **Authors**: Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, Yusuke Iwasawa
- **Year**: 2022
- **Venue**: NeurIPS 2022
- **arXiv**: https://arxiv.org/abs/2205.11916
- **Why relevant**: Introduces zero-shot CoT ("Let's think step by step"), showing CoT can work without few-shot examples. Important for understanding CoT's behavior on different task types.

## 3. Wang et al. (2022) - Self-Consistency Improves Chain of Thought Reasoning
- **File**: `2203.11171_wang2022_self_consistency.pdf`
- **Authors**: Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou
- **Year**: 2022
- **Venue**: ICLR 2023
- **arXiv**: https://arxiv.org/abs/2203.11171
- **Why relevant**: Self-consistency extends CoT by sampling multiple reasoning paths. Demonstrates substantial accuracy gains on GSM8K (+17.9%), SVAMP (+11%), AQuA (+12.2%), and StrategyQA (+6.4%). Important baseline for comparison.

## 4. Zhou et al. (2022) - Least-to-Most Prompting Enables Complex Reasoning
- **File**: `2205.10625_zhou2022_least_to_most.pdf`
- **Authors**: Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, Ed Chi
- **Year**: 2022/2023
- **Venue**: ICLR 2023
- **arXiv**: https://arxiv.org/abs/2205.10625
- **Why relevant**: Extension of CoT that decomposes problems into sub-problems. Shows CoT limitations on complex tasks and how progressive problem-solving improves generalization.

## 5. Xu et al. (2025) - Chain of Draft: Thinking Faster by Writing Less
- **File**: `2502.18600_xu2025_chain_of_draft.pdf`
- **Authors**: Silei Xu, Wenhao Xie, Lingxiao Zhao, Pengcheng He
- **Year**: 2025
- **Venue**: arXiv preprint
- **arXiv**: https://arxiv.org/abs/2502.18600
- **Why relevant**: Directly addresses verbosity question. Shows CoT uses 200 tokens vs CoD's 40 tokens on GSM8K, with comparable accuracy (95% CoT vs 91% CoD). Demonstrates CoT verbosity is separable from accuracy gains.

## 6. Survey on Evaluating Reasoning Traces (2025)
- **File**: `2502.12289_survey_evaluating_reasoning_traces.pdf`
- **Authors**: Multiple (survey paper)
- **Year**: 2025
- **arXiv**: https://arxiv.org/abs/2502.12289
- **Why relevant**: Comprehensive survey of methods for evaluating CoT reasoning chains, covering metrics beyond just final answer accuracy.

## 7. Patel et al. (2021) - SVAMP: Simple Variations on Arithmetic Math Word Problems
- **File**: `2103.07191_patel2021_svamp.pdf`
- **Authors**: Arkil Patel, Satwik Bhatt, Balaraman Ravindran
- **Year**: 2021
- **Venue**: NAACL 2021
- **arXiv**: https://arxiv.org/abs/2103.07191
- **Why relevant**: Introduces the SVAMP benchmark showing that NLP models rely on shallow heuristics for math word problems. Important context for understanding what CoT actually improves.

## 8. Ho et al. (2022) - Large Language Models Are Reasoning Teachers
- **File**: `2109.01652_ho2022_large_language_models_trained.pdf`
- **Authors**: Namgyu Ho, Laura Schmid, Se-Young Yun
- **Year**: 2022
- **arXiv**: https://arxiv.org/abs/2212.08410
- **Why relevant**: Studies fine-tuning on CoT rationales to transfer reasoning ability to smaller models. Shows CoT benefits are real and transferable, not just verbosity artifacts.
