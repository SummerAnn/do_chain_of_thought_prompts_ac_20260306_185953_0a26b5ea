"""
Analysis and visualization script for CoT experiment results.
Run after experiment.py completes.

Produces:
- Statistical tests (McNemar, Wilcoxon) per task/condition pair
- Bar charts of accuracy by task and condition
- Token count distributions
- ΔAcc vs ΔTokens scatter plot
- Saves everything to results/plots/
"""
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

WORKSPACE = Path("/workspaces/do_chain_of_thought_prompts_ac_20260306_185953_0a26b5ea")
RESULTS_FILE = WORKSPACE / "results/raw_results.jsonl"
SUMMARY_FILE = WORKSPACE / "results/summary.json"
PLOTS_DIR = WORKSPACE / "results/plots"
STATS_FILE = WORKSPACE / "results/statistical_tests.json"

TASKS = ["gsm8k", "svamp", "commonsenseqa", "triviaqa"]
CONDITIONS = ["standard", "zero_shot_cot", "few_shot_cot"]
CONDITION_LABELS = {
    "standard": "Standard",
    "zero_shot_cot": "Zero-shot CoT",
    "few_shot_cot": "Few-shot CoT",
}
TASK_LABELS = {
    "gsm8k": "GSM8K\n(Arithmetic)",
    "svamp": "SVAMP\n(Arithmetic)",
    "commonsenseqa": "CommonsenseQA\n(Commonsense)",
    "triviaqa": "TriviaQA\n(Factual Recall)",
}
COLORS = {
    "standard": "#4C72B0",
    "zero_shot_cot": "#DD8452",
    "few_shot_cot": "#55A868",
}


def load_results() -> dict:
    """Load raw results, grouped by (task, condition)."""
    data = defaultdict(list)
    with open(RESULTS_FILE) as f:
        for line in f:
            rec = json.loads(line)
            data[(rec["task"], rec["condition"])].append(rec)
    return data


def mcnemar_test(correct_a: list[bool], correct_b: list[bool]) -> dict:
    """
    McNemar's test for paired binary outcomes.
    Tests H0: methods A and B have equal error rates.
    Returns dict with test statistic, p-value, and the contingency table.
    """
    assert len(correct_a) == len(correct_b), "Paired lists must be same length"
    # Contingency: b = A wrong, B right; c = A right, B wrong
    b = sum(1 for a, bb in zip(correct_a, correct_b) if not a and bb)
    c = sum(1 for a, bb in zip(correct_a, correct_b) if a and not bb)
    n = b + c
    if n == 0:
        return {"b": b, "c": c, "statistic": 0.0, "p_value": 1.0, "significant": False}
    # Use continuity-corrected McNemar
    statistic = (abs(b - c) - 1) ** 2 / n
    p_value = 1 - stats.chi2.cdf(statistic, df=1)
    return {
        "b": b,
        "c": c,
        "statistic": round(statistic, 4),
        "p_value": round(p_value, 6),
        "significant": p_value < 0.05,
    }


def cohens_d_tokens(tokens_a: list[float], tokens_b: list[float]) -> float:
    """Cohen's d for comparing two groups of token counts."""
    n_a, n_b = len(tokens_a), len(tokens_b)
    mean_a, mean_b = np.mean(tokens_a), np.mean(tokens_b)
    pooled_std = math.sqrt(
        ((n_a - 1) * np.var(tokens_a, ddof=1) + (n_b - 1) * np.var(tokens_b, ddof=1))
        / (n_a + n_b - 2)
    )
    if pooled_std == 0:
        return 0.0
    return round((mean_b - mean_a) / pooled_std, 3)


def run_statistical_tests(data: dict) -> dict:
    """
    Run McNemar's tests for accuracy and Wilcoxon tests for token counts.
    Returns nested dict of test results.
    """
    # Align examples by idx for paired tests
    def get_aligned(task, cond_a, cond_b):
        recs_a = {r["idx"]: r for r in data[(task, cond_a)]}
        recs_b = {r["idx"]: r for r in data[(task, cond_b)]}
        common_idx = sorted(set(recs_a) & set(recs_b))
        a_correct = [recs_a[i]["correct"] for i in common_idx]
        b_correct = [recs_b[i]["correct"] for i in common_idx]
        a_tokens = [recs_a[i]["output_tokens"] for i in common_idx]
        b_tokens = [recs_b[i]["output_tokens"] for i in common_idx]
        return a_correct, b_correct, a_tokens, b_tokens

    results = {}
    # Number of comparisons per task: 2 (standard vs zero_shot, standard vs few_shot)
    # Total accuracy comparisons: 4 tasks × 2 = 8 → Bonferroni α = 0.05/8 = 0.00625
    bonferroni_alpha = 0.05 / 8

    for task in TASKS:
        results[task] = {}
        for cot_cond in ["zero_shot_cot", "few_shot_cot"]:
            if (task, "standard") not in data or (task, cot_cond) not in data:
                continue
            a_correct, b_correct, a_tokens, b_tokens = get_aligned(task, "standard", cot_cond)

            # Accuracy test (McNemar's)
            acc_test = mcnemar_test(a_correct, b_correct)
            acc_test["bonferroni_significant"] = acc_test["p_value"] < bonferroni_alpha

            # Delta accuracy
            delta_acc = np.mean(b_correct) - np.mean(a_correct)

            # Token count test (Wilcoxon signed-rank)
            if len(a_tokens) > 1:
                diff = [bt - at for at, bt in zip(a_tokens, b_tokens)]
                if all(d == 0 for d in diff):
                    wil_stat, wil_p = 0.0, 1.0
                else:
                    wil_stat, wil_p = stats.wilcoxon(diff)
            else:
                wil_stat, wil_p = 0.0, 1.0

            delta_tokens = np.mean(b_tokens) - np.mean(a_tokens)
            d = cohens_d_tokens(a_tokens, b_tokens)

            results[task][cot_cond] = {
                "n_pairs": len(a_correct),
                "accuracy_standard": round(np.mean(a_correct), 4),
                "accuracy_cot": round(np.mean(b_correct), 4),
                "delta_accuracy": round(delta_acc, 4),
                "mcnemar": acc_test,
                "mean_tokens_standard": round(np.mean(a_tokens), 1),
                "mean_tokens_cot": round(np.mean(b_tokens), 1),
                "delta_tokens": round(delta_tokens, 1),
                "wilcoxon_stat": round(float(wil_stat), 3),
                "wilcoxon_p": round(float(wil_p), 6),
                "token_cohen_d": d,
            }

    return results


def plot_accuracy_bars(data: dict, out_path: Path):
    """Bar chart of accuracy by task and condition."""
    fig, ax = plt.subplots(figsize=(12, 6))

    n_tasks = len(TASKS)
    n_conds = len(CONDITIONS)
    bar_width = 0.25
    x = np.arange(n_tasks)

    for ci, cond in enumerate(CONDITIONS):
        accuracies = []
        for task in TASKS:
            recs = data.get((task, cond), [])
            if recs:
                acc = sum(r["correct"] for r in recs) / len(recs)
            else:
                acc = 0.0
            accuracies.append(acc * 100)  # Convert to %

        offset = (ci - 1) * bar_width
        bars = ax.bar(
            x + offset, accuracies,
            width=bar_width,
            label=CONDITION_LABELS[cond],
            color=COLORS[cond],
            alpha=0.85,
            edgecolor="white",
            linewidth=0.5,
        )
        # Add value labels on bars
        for bar, val in zip(bars, accuracies):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{val:.1f}%",
                ha="center", va="bottom",
                fontsize=8, color="black",
            )

    ax.set_xticks(x)
    ax.set_xticklabels([TASK_LABELS[t] for t in TASKS], fontsize=10)
    ax.set_ylabel("Accuracy (%)", fontsize=12)
    ax.set_title("Accuracy by Task Type and Prompting Condition", fontsize=13, fontweight="bold")
    ax.legend(loc="upper right", fontsize=10)
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def plot_token_counts(data: dict, out_path: Path):
    """Bar chart of mean output token counts by task and condition."""
    fig, ax = plt.subplots(figsize=(12, 6))

    n_tasks = len(TASKS)
    bar_width = 0.25
    x = np.arange(n_tasks)

    for ci, cond in enumerate(CONDITIONS):
        token_means = []
        token_sems = []
        for task in TASKS:
            recs = data.get((task, cond), [])
            if recs:
                tokens = [r["output_tokens"] for r in recs]
                token_means.append(np.mean(tokens))
                token_sems.append(np.std(tokens, ddof=1) / math.sqrt(len(tokens)))
            else:
                token_means.append(0)
                token_sems.append(0)

        offset = (ci - 1) * bar_width
        ax.bar(
            x + offset, token_means,
            width=bar_width,
            label=CONDITION_LABELS[cond],
            color=COLORS[cond],
            alpha=0.85,
            edgecolor="white",
            yerr=token_sems,
            capsize=3,
        )

    ax.set_xticks(x)
    ax.set_xticklabels([TASK_LABELS[t] for t in TASKS], fontsize=10)
    ax.set_ylabel("Mean Output Tokens", fontsize=12)
    ax.set_title("Mean Output Token Count by Task Type and Prompting Condition", fontsize=13, fontweight="bold")
    ax.legend(loc="upper right", fontsize=10)
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def plot_delta_acc_vs_delta_tokens(stats_results: dict, out_path: Path):
    """Scatter plot: ΔAcc (pp) vs ΔTokens for each (task, condition) pair."""
    fig, ax = plt.subplots(figsize=(9, 7))

    task_markers = {"gsm8k": "o", "svamp": "s", "commonsenseqa": "^", "triviaqa": "D"}
    cond_colors = {"zero_shot_cot": COLORS["zero_shot_cot"], "few_shot_cot": COLORS["few_shot_cot"]}

    for task in TASKS:
        for cond in ["zero_shot_cot", "few_shot_cot"]:
            if task not in stats_results or cond not in stats_results[task]:
                continue
            res = stats_results[task][cond]
            delta_acc = res["delta_accuracy"] * 100  # pp
            delta_tokens = res["delta_tokens"]

            ax.scatter(
                delta_tokens, delta_acc,
                s=120,
                marker=task_markers[task],
                color=cond_colors[cond],
                edgecolors="black",
                linewidths=0.7,
                zorder=5,
                label=f"{task} / {CONDITION_LABELS[cond]}",
            )
            # Annotate
            ax.annotate(
                f"{task[:4]}/{cond[:4]}",
                xy=(delta_tokens, delta_acc),
                xytext=(6, 3),
                textcoords="offset points",
                fontsize=7.5,
            )

    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--", alpha=0.7)
    ax.axvline(0, color="gray", linewidth=0.8, linestyle="--", alpha=0.7)
    ax.set_xlabel("ΔTokens (CoT − Standard, output tokens)", fontsize=12)
    ax.set_ylabel("ΔAccuracy (CoT − Standard, percentage points)", fontsize=12)
    ax.set_title("Accuracy Gain vs. Verbosity Cost of Chain-of-Thought Prompting", fontsize=12, fontweight="bold")

    # Build legend without duplicates
    handles_seen = {}
    for task in TASKS:
        label = TASK_LABELS[task].replace("\n", " ")
        handles_seen[label] = mpatches.Patch(
            facecolor="white", edgecolor="black",
            label=label, linewidth=0.7,
        )
    for cond in ["zero_shot_cot", "few_shot_cot"]:
        label = CONDITION_LABELS[cond]
        handles_seen[label] = mpatches.Patch(color=cond_colors[cond], label=label, alpha=0.85)

    ax.legend(handles=list(handles_seen.values()), fontsize=8, loc="upper left")
    ax.yaxis.grid(True, alpha=0.3)
    ax.xaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def plot_token_multiplier(data: dict, out_path: Path):
    """
    Bar chart showing token multiplier: CoT tokens / Standard tokens.
    This visualizes verbosity inflation.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(len(TASKS))
    bar_width = 0.35

    for ci, cond in enumerate(["zero_shot_cot", "few_shot_cot"]):
        multipliers = []
        for task in TASKS:
            std_recs = data.get((task, "standard"), [])
            cot_recs = data.get((task, cond), [])
            if std_recs and cot_recs:
                std_mean = np.mean([r["output_tokens"] for r in std_recs])
                cot_mean = np.mean([r["output_tokens"] for r in cot_recs])
                multipliers.append(cot_mean / std_mean if std_mean > 0 else 1.0)
            else:
                multipliers.append(1.0)

        offset = (ci - 0.5) * bar_width
        bars = ax.bar(
            x + offset, multipliers,
            width=bar_width,
            label=CONDITION_LABELS[cond],
            color=COLORS[cond],
            alpha=0.85,
            edgecolor="white",
        )
        for bar, val in zip(bars, multipliers):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.02,
                f"{val:.1f}×",
                ha="center", va="bottom",
                fontsize=9,
            )

    ax.axhline(1.0, color="black", linewidth=1, linestyle="-", alpha=0.5, label="1× (no increase)")
    ax.set_xticks(x)
    ax.set_xticklabels([TASK_LABELS[t] for t in TASKS], fontsize=10)
    ax.set_ylabel("Token Multiplier (CoT / Standard)", fontsize=12)
    ax.set_title("Verbosity Inflation: How Many Times More Tokens Does CoT Use?", fontsize=12, fontweight="bold")
    ax.legend(fontsize=10)
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def print_results_table(data: dict, stats_results: dict):
    """Print formatted results table to stdout."""
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)

    header = f"{'Task':<20} {'Condition':<18} {'Acc %':>7} {'Tokens':>8} {'ΔAcc':>7} {'ΔTok':>7} {'p(McNemar)':>12}"
    print(header)
    print("-"*80)

    for task in TASKS:
        for cond in CONDITIONS:
            recs = data.get((task, cond), [])
            if not recs:
                continue
            acc = sum(r["correct"] for r in recs) / len(recs) * 100
            mean_tok = np.mean([r["output_tokens"] for r in recs])

            delta_acc_str = "—"
            delta_tok_str = "—"
            p_val_str = "—"

            if cond != "standard" and task in stats_results and cond in stats_results[task]:
                res = stats_results[task][cond]
                delta_acc_str = f"{res['delta_accuracy']*100:+.1f}pp"
                delta_tok_str = f"{res['delta_tokens']:+.0f}"
                p = res["mcnemar"]["p_value"]
                p_val_str = f"{p:.4f}{'*' if res['mcnemar']['significant'] else ' '}"

            print(f"{task:<20} {cond:<18} {acc:>7.1f} {mean_tok:>8.1f} {delta_acc_str:>7} {delta_tok_str:>7} {p_val_str:>12}")
        print()


def main():
    PLOTS_DIR.mkdir(exist_ok=True)

    print("Loading results...")
    data = load_results()

    print("Running statistical tests...")
    stats_results = run_statistical_tests(data)

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (bool, np.bool_)):
                return bool(obj)
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            return super().default(obj)

    with open(STATS_FILE, "w") as f:
        json.dump(stats_results, f, indent=2, cls=NumpyEncoder)
    print(f"Statistical tests saved to {STATS_FILE}")

    print_results_table(data, stats_results)

    print("\nGenerating plots...")
    plot_accuracy_bars(data, PLOTS_DIR / "accuracy_by_task.png")
    plot_token_counts(data, PLOTS_DIR / "token_counts.png")
    plot_delta_acc_vs_delta_tokens(stats_results, PLOTS_DIR / "delta_acc_vs_delta_tokens.png")
    plot_token_multiplier(data, PLOTS_DIR / "token_multiplier.png")

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
