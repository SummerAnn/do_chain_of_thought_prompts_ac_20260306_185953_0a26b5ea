"""
Answer extraction utilities for each task type.
Parses model responses to extract the final answer for accuracy evaluation.
"""
import re


def extract_gsm8k_answer(response: str) -> str | None:
    """
    Extract numeric answer from GSM8K/SVAMP model response.
    Looks for patterns like 'the answer is X', '#### X', or just a trailing number.
    Returns normalized string of the number (no commas, no $).
    """
    # Normalize: remove $ and commas
    response_clean = response.replace("$", "").replace(",", "")

    # Pattern: "#### 18" (GSM8K style)
    m = re.search(r"####\s*([\d.]+)", response_clean)
    if m:
        return m.group(1).strip()

    # Pattern: "The answer is X." or "The answer is X"
    m = re.search(r"[Tt]he answer is[:\s]+([\-\d.]+)", response_clean)
    if m:
        return m.group(1).strip()

    # Pattern: "answer: X" or "Answer: X"
    m = re.search(r"[Aa]nswer[:\s]+([\-\d.]+)", response_clean)
    if m:
        return m.group(1).strip()

    # Last number in response (fallback)
    numbers = re.findall(r"[\-]?\d+(?:\.\d+)?", response_clean)
    if numbers:
        return numbers[-1]

    return None


def check_gsm8k_correct(response: str, gold_answer: str) -> bool:
    """
    Check if response is correct for GSM8K.
    Gold answer format: "... #### 18"
    """
    # Extract gold answer from "#### N" format
    m = re.search(r"####\s*([\d.]+)", gold_answer.replace(",", ""))
    if not m:
        return False
    gold_num = m.group(1).strip()

    pred = extract_gsm8k_answer(response)
    if pred is None:
        return False

    # Compare as floats to handle e.g. "18" vs "18.0"
    try:
        return abs(float(pred) - float(gold_num)) < 0.01
    except ValueError:
        return pred == gold_num


def check_svamp_correct(response: str, gold_answer: str) -> bool:
    """
    Check if response is correct for SVAMP.
    Gold answer is a numeric string (already extracted).
    """
    pred = extract_gsm8k_answer(response)  # Same extraction logic
    if pred is None:
        return False
    try:
        return abs(float(pred) - float(str(gold_answer).replace(",", ""))) < 0.01
    except ValueError:
        return False


def extract_mcq_answer(response: str) -> str | None:
    """
    Extract MCQ answer (A-E) from CommonsenseQA model response.
    """
    # Pattern: "The answer is B." or "answer: B" or just "B)"
    m = re.search(r"[Tt]he answer is[:\s]*([A-E])\b", response)
    if m:
        return m.group(1).upper()

    m = re.search(r"[Aa]nswer[:\s]*([A-E])\b", response)
    if m:
        return m.group(1).upper()

    # Last standalone letter A-E
    matches = re.findall(r"\b([A-E])\b", response)
    if matches:
        return matches[-1].upper()

    return None


def check_csqa_correct(response: str, gold_key: str) -> bool:
    """Check if response is correct for CommonsenseQA."""
    pred = extract_mcq_answer(response)
    if pred is None:
        return False
    return pred.upper() == gold_key.upper()


def check_triviaqa_correct(response: str, gold_aliases: list[str]) -> bool:
    """
    Check if response is correct for TriviaQA.
    Checks if any normalized alias appears in the normalized response.
    """
    response_norm = response.lower().strip()
    for alias in gold_aliases:
        alias_norm = alias.lower().strip()
        if alias_norm in response_norm:
            return True
    return False
