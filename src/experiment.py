"""
Main experiment runner for CoT vs Standard prompting comparison.

Loads datasets, calls Claude API for each (task, condition, example),
records accuracy and token counts, saves results to JSON.

Usage:
    source .venv/bin/activate
    python src/experiment.py

Environment variables required:
    ANTHROPIC_API_KEY
"""
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

import anthropic
from datasets import load_from_disk, Dataset
import pyarrow as pa
import pyarrow.ipc as ipc

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))
from prompts import format_prompt
from extract_answers import (
    check_gsm8k_correct,
    check_svamp_correct,
    check_csqa_correct,
    check_triviaqa_correct,
)

# ─── Configuration ─────────────────────────────────────────────────────────────

WORKSPACE = Path("/workspaces/do_chain_of_thought_prompts_ac_20260306_185953_0a26b5ea")
RESULTS_DIR = WORKSPACE / "results"
RESULTS_FILE = RESULTS_DIR / "raw_results.jsonl"
SUMMARY_FILE = RESULTS_DIR / "summary.json"

MODEL = "claude-haiku-4-5-20251001"  # Fast, cost-effective Claude model
TEMPERATURE = 0  # Deterministic for reproducibility
MAX_TOKENS = 512  # Allow full CoT reasoning chains

SAMPLE_SIZE = 150  # Per task; 4 tasks × 3 conditions = 1800 API calls total
RANDOM_SEED = 42

TASKS = ["gsm8k", "svamp", "commonsenseqa", "triviaqa"]
CONDITIONS = ["standard", "zero_shot_cot", "few_shot_cot"]

# Rate limiting
CALLS_PER_MINUTE = 45  # Stay under Haiku rate limits
SLEEP_BETWEEN_CALLS = 60.0 / CALLS_PER_MINUTE  # ~1.33s between calls

# ─── Data Loading ──────────────────────────────────────────────────────────────

def load_gsm8k(n: int, seed: int) -> list[dict]:
    """Load n examples from GSM8K test split."""
    ds = load_from_disk(str(WORKSPACE / "datasets/gsm8k"))
    test = ds["test"]
    rng = random.Random(seed)
    indices = rng.sample(range(len(test)), min(n, len(test)))
    return [{"task": "gsm8k", "question": test[i]["question"], "gold": test[i]["answer"]} for i in indices]


def load_svamp(n: int, seed: int) -> list[dict]:
    """Load n examples from SVAMP test split."""
    ds = load_from_disk(str(WORKSPACE / "datasets/svamp"))
    test = ds["test"]
    rng = random.Random(seed)
    indices = rng.sample(range(len(test)), min(n, len(test)))
    return [
        {
            "task": "svamp",
            "question": test[i]["question_concat"],
            "gold": str(test[i]["Answer"]),
        }
        for i in indices
    ]


def load_commonsenseqa(n: int, seed: int) -> list[dict]:
    """Load n examples from CommonsenseQA validation split."""
    ds = load_from_disk(str(WORKSPACE / "datasets/commonsenseqa"))
    val = ds["validation"]
    rng = random.Random(seed)
    indices = rng.sample(range(len(val)), min(n, len(val)))
    examples = []
    for i in indices:
        row = val[i]
        labels = row["choices"]["label"]
        texts = row["choices"]["text"]
        choices_str = "\n".join(f"{l}) {t}" for l, t in zip(labels, texts))
        examples.append({
            "task": "commonsenseqa",
            "question": row["question"],
            "choices": choices_str,
            "gold": row["answerKey"],
        })
    return examples


def load_triviaqa(n: int, seed: int) -> list[dict]:
    """Load n examples from TriviaQA (Arrow file)."""
    arrow_path = WORKSPACE / "datasets/triviaqa/data-00000-of-00001.arrow"
    with pa.memory_map(str(arrow_path), "r") as f:
        reader = ipc.open_stream(f)
        table = reader.read_all()

    rng = random.Random(seed)
    all_idx = list(range(len(table)))
    indices = rng.sample(all_idx, min(n, len(all_idx)))

    examples = []
    for i in indices:
        row = {k: table[k][i].as_py() for k in table.schema.names}
        answer = row["answer"]
        aliases = answer.get("normalized_aliases", [answer.get("normalized_value", "")])
        if not aliases:
            aliases = [answer.get("normalized_value", "")]
        examples.append({
            "task": "triviaqa",
            "question": row["question"],
            "gold": answer.get("value", ""),
            "gold_aliases": aliases,
        })
    return examples


def load_all_examples() -> dict[str, list[dict]]:
    """Load samples from all tasks."""
    print(f"Loading {SAMPLE_SIZE} examples per task (seed={RANDOM_SEED})...")
    return {
        "gsm8k": load_gsm8k(SAMPLE_SIZE, RANDOM_SEED),
        "svamp": load_svamp(SAMPLE_SIZE, RANDOM_SEED),
        "commonsenseqa": load_commonsenseqa(SAMPLE_SIZE, RANDOM_SEED),
        "triviaqa": load_triviaqa(SAMPLE_SIZE, RANDOM_SEED),
    }

# ─── API Calling ───────────────────────────────────────────────────────────────

def call_claude(client: anthropic.Anthropic, prompt: str, max_retries: int = 5) -> dict:
    """
    Call Claude API with retry logic.
    Returns dict with 'content' (text) and 'output_tokens' (int).
    """
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                messages=[{"role": "user", "content": prompt}],
            )
            return {
                "content": response.content[0].text,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
        except anthropic.RateLimitError:
            wait_time = (2 ** attempt) * 10
            print(f"  Rate limit hit, waiting {wait_time}s...")
            time.sleep(wait_time)
        except anthropic.APIError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) * 5
            print(f"  API error ({e}), retrying in {wait_time}s...")
            time.sleep(wait_time)
    raise RuntimeError("Max retries exceeded")


# ─── Answer Checking ───────────────────────────────────────────────────────────

def check_correct(task: str, response: str, example: dict) -> bool:
    """Check if model response is correct for the given task."""
    if task == "gsm8k":
        return check_gsm8k_correct(response, example["gold"])
    elif task == "svamp":
        return check_svamp_correct(response, example["gold"])
    elif task == "commonsenseqa":
        return check_csqa_correct(response, example["gold"])
    elif task == "triviaqa":
        return check_triviaqa_correct(response, example.get("gold_aliases", [example["gold"]]))
    return False

# ─── Main Experiment Loop ──────────────────────────────────────────────────────

def run_experiments():
    """Run all experiments and save results."""
    random.seed(RANDOM_SEED)
    RESULTS_DIR.mkdir(exist_ok=True)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    client = anthropic.Anthropic(api_key=api_key)

    examples_by_task = load_all_examples()

    # Count already-done results to allow resumption
    done_keys = set()
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            for line in f:
                rec = json.loads(line)
                done_keys.add((rec["task"], rec["condition"], rec["idx"]))
        print(f"Resuming: {len(done_keys)} results already completed")

    total_calls = sum(len(v) for v in examples_by_task.values()) * len(CONDITIONS)
    completed = len(done_keys)
    print(f"Total API calls needed: {total_calls}  (already done: {completed})\n")

    with open(RESULTS_FILE, "a") as out_f:
        for task in TASKS:
            examples = examples_by_task[task]
            for condition in CONDITIONS:
                pending = [(idx, ex) for idx, ex in enumerate(examples)
                           if (task, condition, idx) not in done_keys]
                if not pending:
                    continue

                print(f"[{task.upper()} / {condition}] {len(pending)} remaining...")
                for idx, ex in pending:
                    # Format prompt
                    choices = ex.get("choices", "")
                    prompt = format_prompt(task, condition, ex["question"], choices)

                    # Call API
                    result = call_claude(client, prompt)
                    response_text = result["content"]

                    # Evaluate accuracy
                    correct = check_correct(task, response_text, ex)

                    # Save result
                    record = {
                        "task": task,
                        "condition": condition,
                        "idx": idx,
                        "question": ex["question"],
                        "gold": ex.get("gold", ""),
                        "response": response_text,
                        "correct": correct,
                        "input_tokens": result["input_tokens"],
                        "output_tokens": result["output_tokens"],
                    }
                    out_f.write(json.dumps(record) + "\n")
                    out_f.flush()

                    completed += 1
                    print(
                        f"  [{completed}/{total_calls}] task={task}, cond={condition}, "
                        f"idx={idx}, correct={correct}, out_tokens={result['output_tokens']}"
                    )

                    time.sleep(SLEEP_BETWEEN_CALLS)

    print(f"\nAll experiments complete! Results saved to {RESULTS_FILE}")
    compute_summary()


def compute_summary():
    """Aggregate results into summary statistics."""
    from collections import defaultdict

    records_by_key = defaultdict(list)
    with open(RESULTS_FILE) as f:
        for line in f:
            rec = json.loads(line)
            key = (rec["task"], rec["condition"])
            records_by_key[key].append(rec)

    summary = {}
    for (task, condition), records in records_by_key.items():
        n = len(records)
        correct_count = sum(r["correct"] for r in records)
        avg_output_tokens = sum(r["output_tokens"] for r in records) / n
        accuracy = correct_count / n

        if task not in summary:
            summary[task] = {}
        summary[task][condition] = {
            "n": n,
            "accuracy": round(accuracy, 4),
            "correct": correct_count,
            "avg_output_tokens": round(avg_output_tokens, 1),
        }

    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to {SUMMARY_FILE}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run_experiments()
