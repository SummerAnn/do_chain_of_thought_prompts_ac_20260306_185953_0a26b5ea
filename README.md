# Do Chain-of-Thought Prompts Actually Improve Accuracy or Just Verbosity?

A systematic empirical study comparing Standard, Zero-shot CoT, and Few-shot CoT prompting across four task types, measuring both accuracy and token counts using real Claude API calls.

## Key Findings

- **CoT dramatically helps reasoning tasks**: +40.7pp on GSM8K arithmetic (54.0% → 94.7%), +51.3pp on CommonsenseQA (35.3% → 86.7%), both p < 0.0001
- **CoT does not help factual recall**: TriviaQA showed only +1.3-5.3pp with p > 0.05 (not significant)
- **CoT always inflates tokens**: 1.7× to 19× more output tokens regardless of whether accuracy improves
- **Verbosity cost is task-agnostic; accuracy gain is task-specific**: The key practical insight
- **Near-ceiling tasks show worst CoT ROI**: SVAMP (90% standard accuracy) used 19× more tokens for a non-significant 3.3pp gain

## Results Summary

| Task | Standard | ZS-CoT | FS-CoT | Std Tokens | FS-CoT Tokens | CoT Significant? |
|------|----------|--------|--------|------------|---------------|-----------------|
| GSM8K (arithmetic) | 54.0% | 94.7% | 94.7% | 17 | 146 | Yes (p<0.0001) |
| SVAMP (arithmetic) | 90.0% | 88.0% | 93.3% | 8 | 80 | No (p=0.18) |
| CommonsenseQA | 35.3% | 80.7% | 86.7% | 112 | 187 | Yes (p<0.0001) |
| TriviaQA (factual) | 72.7% | 78.0% | 74.0% | 50 | 140 | No (p=0.75) |

## How to Reproduce

```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Set API key
export ANTHROPIC_API_KEY=your_key_here

# 3. Run experiments (1800 API calls, ~45 min)
python src/experiment.py

# 4. Run analysis
python src/analyze.py
```

## File Structure

```
.
├── REPORT.md                    # Full research report
├── planning.md                  # Research plan and hypothesis
├── src/
│   ├── experiment.py           # Main experiment runner
│   ├── prompts.py              # Prompt templates
│   ├── extract_answers.py      # Answer extraction per task
│   └── analyze.py              # Statistical analysis + plots
├── results/
│   ├── raw_results.jsonl       # 1,800 individual API call results
│   ├── summary.json            # Aggregated metrics
│   ├── statistical_tests.json  # McNemar & Wilcoxon test results
│   └── plots/                  # Visualization PNG files
└── datasets/                   # Pre-downloaded datasets (not in git)
```

See [REPORT.md](REPORT.md) for the complete research report.
