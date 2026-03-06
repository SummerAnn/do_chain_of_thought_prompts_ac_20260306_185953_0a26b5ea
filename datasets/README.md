# Datasets for CoT Research

This directory contains datasets for evaluating Chain-of-Thought prompting accuracy vs. verbosity.
Data files are NOT committed to git due to size. Follow the download instructions below.

## Dataset Overview

| Name | Source | Size | Task Type | Purpose |
|------|--------|------|-----------|---------|
| GSM8K | openai/gsm8k | 7,473 train / 1,319 test | Multi-step arithmetic | Primary math reasoning benchmark |
| SVAMP | ChilleD/SVAMP | 700 train / 300 test | Arithmetic MWP | Tests shallow vs. deep reasoning |
| CommonsenseQA | tau/commonsense_qa | 9,741 train / 1,221 val | Commonsense MCQ | Multi-step commonsense reasoning |
| TriviaQA | mandarjoshi/trivia_qa | 5,000 (sample) | Factual recall | Single-step factual recall baseline |

---

## Dataset 1: GSM8K (Grade School Math 8K)

### Overview
- **Source**: HuggingFace `openai/gsm8k`
- **Size**: 8,792 total (7,473 train, 1,319 test)
- **Format**: HuggingFace Dataset (Parquet)
- **Task**: Multi-step arithmetic word problems (2-8 steps)
- **License**: MIT

### Purpose for Research
GSM8K is the PRIMARY benchmark for evaluating CoT on multi-step arithmetic tasks.
Wei et al. (2022) showed CoT doubles performance on GSM8K (18% -> 57% with PaLM 540B).
The hypothesis predicts significant CoT improvement here.

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("openai/gsm8k", "main")
dataset.save_to_disk("datasets/gsm8k")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/gsm8k")
# Fields: question (str), answer (str with #### final answer)
```

### Sample Data
See `gsm8k/samples.json` for 10 examples.

---

## Dataset 2: SVAMP (Simple Variations on Arithmetic Math word Problems)

### Overview
- **Source**: HuggingFace `ChilleD/SVAMP`
- **Size**: 1,000 total (700 train, 300 test)
- **Format**: HuggingFace Dataset
- **Task**: Arithmetic math word problems with structural variations
- **License**: MIT

### Purpose for Research
SVAMP tests whether models understand math problems or rely on shallow heuristics.
Useful for measuring whether CoT actually improves reasoning vs. surface pattern matching.
Chain-of-thought should help models avoid shallow reasoning shortcuts.

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("ChilleD/SVAMP")
dataset.save_to_disk("datasets/svamp")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/svamp")
# Fields: Body, Question, Answer, Equation, Type
```

### Sample Data
See `svamp/samples.json` for 10 examples.

---

## Dataset 3: CommonsenseQA

### Overview
- **Source**: HuggingFace `tau/commonsense_qa`
- **Size**: 12,102 total (9,741 train, 1,221 val, 1,140 test)
- **Format**: HuggingFace Dataset
- **Task**: Multiple-choice commonsense questions (5 choices)
- **License**: MIT

### Purpose for Research
CommonsenseQA tests multi-step commonsense reasoning (different from arithmetic).
The research hypothesis expects CoT to show moderate improvement on commonsense tasks.
Used in Wei et al. (2022) original CoT evaluation.

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("tau/commonsense_qa")
dataset.save_to_disk("datasets/commonsenseqa")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/commonsenseqa")
# Fields: id, question, question_concept, choices (label, text), answerKey
```

### Sample Data
See `commonsenseqa/samples.json` for 10 examples.

---

## Dataset 4: TriviaQA (Factual Recall)

### Overview
- **Source**: HuggingFace `mandarjoshi/trivia_qa` (rc.nocontext)
- **Size**: 5,000 (sample from 138,384 available)
- **Format**: HuggingFace Dataset
- **Task**: Trivia question answering (single-step factual recall)
- **License**: Apache 2.0

### Purpose for Research
TriviaQA is the KEY CONTROL dataset for testing the hypothesis that CoT does NOT improve
single-step factual recall. Questions are trivia-style, requiring only direct knowledge
retrieval without multi-step reasoning. The hypothesis predicts NO significant accuracy
improvement from CoT here (but DOES predict increased output length).

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("mandarjoshi/trivia_qa", "rc.nocontext", split="train[:5000]")
dataset.save_to_disk("datasets/triviaqa")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/triviaqa")
# Fields: question, answer (dict with aliases, value)
```

### Notes
- Use the `rc.nocontext` configuration for pure factual recall (no document context provided)
- The `answer` field contains multiple valid answer aliases
- For evaluation, check if model output contains any of the normalized_aliases

### Sample Data
See `triviaqa/samples.json` for 10 examples.

---

## Experiment Design Notes

For the research hypothesis comparison:
1. **Multi-step arithmetic tasks** (GSM8K, SVAMP): Expect significant CoT accuracy gain
2. **Commonsense reasoning** (CommonsenseQA): Expect moderate CoT accuracy gain
3. **Factual recall** (TriviaQA): Expect NO accuracy gain, but YES verbosity increase

Metrics to collect for EACH task:
- Accuracy (standard prompting vs. CoT prompting)
- Output token count / response length (verbosity measure)
- Task-specific metrics (exact match for factual, accuracy for MCQ)
