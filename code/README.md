# Cloned Code Repositories

## Repo 1: chain-of-thought-hub
- **URL**: https://github.com/FranxYao/chain-of-thought-hub
- **Purpose**: Comprehensive benchmarking of LLMs on complex reasoning tasks using CoT prompting
- **Location**: `code/chain-of-thought-hub/`
- **Key files**:
  - `gsm8k/` - GSM8K evaluation scripts
  - `BBH/` - BIG-bench Hard evaluation
  - `MMLU/` - MMLU knowledge benchmark
  - `notebooks/` - Jupyter notebooks for analysis
- **What it provides**: Ready-to-use evaluation scripts for GSM8K and other benchmarks; leaderboard of model performance with CoT prompting; baseline comparison scores
- **Notes**: Primarily designed for comparing different LLMs, not comparing prompting strategies. Useful as a reference for expected performance levels.

## Repo 2: chain-of-draft
- **URL**: https://github.com/sileix/chain-of-draft
- **Purpose**: Official implementation of Chain of Draft (CoD) - a verbosity-reducing alternative to CoT
- **Location**: `code/chain-of-draft/`
- **Key files**:
  - `evaluate.py` - Main evaluation script
  - `llm_client.py` - LLM API client (supports OpenAI, Claude, OpenAI-compatible)
  - `configs/` - Prompts and few-shot examples for each task (gsm8k, date, sports, coin_flip)
  - `tasks/` - Task-specific evaluation logic
  - `utils.py` - Utility functions
- **What it provides**: Direct comparison of Standard, CoT, and CoD prompting strategies; token counting and latency measurement; evaluation on GSM8K and BIG-bench tasks
- **Key usage**:
  ```bash
  python evaluate.py \
      --task gsm8k \
      --model gpt-4o \
      --prompt cod \   # options: baseline, cod, cot
      --shot 5
  ```
- **Notes**:
  - Requires OpenAI API key (for GPT models) or Anthropic API key (for Claude models)
  - Results stored in `./results/` directory
  - This codebase directly supports the verbosity measurement aspect of our research
  - Can be adapted to measure token counts for standard vs. CoT prompting on our datasets

## Key Utility

The `chain-of-draft` repository is the most directly relevant to our research because:
1. It already implements the comparison framework (Standard vs. CoT vs. CoD)
2. It measures both accuracy AND token count (verbosity)
3. It evaluates on GSM8K which is our primary arithmetic benchmark
4. The code can be extended to include TriviaQA (factual recall) evaluation
