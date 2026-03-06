"""
Prompt templates and few-shot examples for the CoT experiment.
Three conditions: standard (no reasoning), zero-shot CoT, few-shot CoT.
"""

# ─── STANDARD PROMPTS (no reasoning, direct answer) ───────────────────────────

STANDARD_TEMPLATES = {
    "gsm8k": (
        "Answer the following math problem with just the final number.\n\n"
        "Question: {question}\n"
        "Answer:"
    ),
    "svamp": (
        "Answer the following math problem with just the final number.\n\n"
        "Question: {question}\n"
        "Answer:"
    ),
    "commonsenseqa": (
        "Choose the correct answer (A, B, C, D, or E).\n\n"
        "Question: {question}\n"
        "Choices:\n{choices}\n"
        "Answer:"
    ),
    "triviaqa": (
        "Answer the following question briefly.\n\n"
        "Question: {question}\n"
        "Answer:"
    ),
}

# ─── ZERO-SHOT CoT PROMPTS ("Let's think step by step") ────────────────────────

ZERO_SHOT_COT_TEMPLATES = {
    "gsm8k": (
        "Answer the following math problem. Show your reasoning step by step, "
        "then give the final answer.\n\n"
        "Question: {question}\n"
        "Let's think step by step."
    ),
    "svamp": (
        "Answer the following math problem. Show your reasoning step by step, "
        "then give the final answer.\n\n"
        "Question: {question}\n"
        "Let's think step by step."
    ),
    "commonsenseqa": (
        "Choose the correct answer (A, B, C, D, or E). Think step by step.\n\n"
        "Question: {question}\n"
        "Choices:\n{choices}\n"
        "Let's think step by step."
    ),
    "triviaqa": (
        "Answer the following question. Think step by step before giving your answer.\n\n"
        "Question: {question}\n"
        "Let's think step by step."
    ),
}

# ─── FEW-SHOT CoT EXAMPLES ────────────────────────────────────────────────────

# GSM8K: 3 examples with multi-step arithmetic reasoning
GSM8K_FEW_SHOT_EXAMPLES = [
    {
        "question": "A farmer has 24 chickens. Each chicken lays 3 eggs per day. He sells eggs in cartons of 12. How many cartons can he fill each day?",
        "reasoning": "Step 1: Total eggs per day = 24 chickens × 3 eggs = 72 eggs.\nStep 2: Cartons = 72 eggs ÷ 12 eggs per carton = 6 cartons.",
        "answer": "6",
    },
    {
        "question": "Maria has $50. She buys 3 books at $8 each and 2 pens at $1.50 each. How much money does she have left?",
        "reasoning": "Step 1: Cost of books = 3 × $8 = $24.\nStep 2: Cost of pens = 2 × $1.50 = $3.\nStep 3: Total spent = $24 + $3 = $27.\nStep 4: Remaining = $50 - $27 = $23.",
        "answer": "23",
    },
    {
        "question": "A store has 120 apples. They sell 45 on Monday and receive a new shipment of 60 on Tuesday. On Wednesday, they sell half of the remaining apples. How many apples are left?",
        "reasoning": "Step 1: After Monday = 120 - 45 = 75 apples.\nStep 2: After Tuesday shipment = 75 + 60 = 135 apples.\nStep 3: Wednesday sales = 135 ÷ 2 = 67.5, so 67 apples sold.\nStep 4: Remaining = 135 - 67 = 68 apples.",
        "answer": "68",
    },
]

# SVAMP: 3 examples for arithmetic word problems
SVAMP_FEW_SHOT_EXAMPLES = [
    {
        "question": "There are 15 red balls and 23 blue balls in a bag. If you remove 8 red balls, how many more blue balls are there than red balls?",
        "reasoning": "Step 1: Red balls remaining = 15 - 8 = 7.\nStep 2: Difference = 23 - 7 = 16 more blue balls.",
        "answer": "16",
    },
    {
        "question": "A class has 32 students. 12 students play soccer and 10 play basketball. The rest play neither. How many students play neither sport?",
        "reasoning": "Step 1: Students playing a sport = 12 + 10 = 22.\nStep 2: Students playing neither = 32 - 22 = 10.",
        "answer": "10",
    },
    {
        "question": "Tom earns $15 per hour. He worked 6 hours on Saturday and 4 hours on Sunday. How much did he earn over the weekend?",
        "reasoning": "Step 1: Total hours = 6 + 4 = 10 hours.\nStep 2: Total earnings = 10 × $15 = $150.",
        "answer": "150",
    },
]

# CommonsenseQA: 3 examples with multi-choice reasoning
CSQA_FEW_SHOT_EXAMPLES = [
    {
        "question": "What do people aim to do at a party?",
        "choices": "A) work\nB) have fun\nC) sleep\nD) study\nE) exercise",
        "reasoning": "Parties are social gatherings meant for celebration and enjoyment. The primary purpose is entertainment and socializing, not work, sleep, study, or exercise.",
        "answer": "B",
    },
    {
        "question": "Where would you find a large door that spins on a vertical axis?",
        "choices": "A) barn\nB) revolving door\nC) trapdoor\nD) sliding door\nE) screen door",
        "reasoning": "A door that spins on a vertical axis is the definition of a revolving door. Barns use large swinging doors, trapdoors open vertically, sliding doors move horizontally, and screen doors swing open.",
        "answer": "B",
    },
    {
        "question": "What might someone use to write on a whiteboard?",
        "choices": "A) pencil\nB) crayon\nC) dry-erase marker\nD) ballpoint pen\nE) chalk",
        "reasoning": "Whiteboards are designed specifically for dry-erase markers, which can be wiped off cleanly. Pencils, crayons, and ballpoint pens leave permanent marks. Chalk is for blackboards/chalkboards.",
        "answer": "C",
    },
]

# TriviaQA: 3 examples with step-by-step factual recall
TRIVIAQA_FEW_SHOT_EXAMPLES = [
    {
        "question": "Who painted the Mona Lisa?",
        "reasoning": "The Mona Lisa is one of the most famous paintings in history. It was created by the Italian Renaissance artist and polymath Leonardo da Vinci.",
        "answer": "Leonardo da Vinci",
    },
    {
        "question": "What is the capital city of Australia?",
        "reasoning": "Australia's capital is often confused with Sydney (the largest city) or Melbourne. However, Canberra was purpose-built as the capital to resolve the rivalry between Sydney and Melbourne.",
        "answer": "Canberra",
    },
    {
        "question": "In what year did World War II end?",
        "reasoning": "World War II ended with Germany's surrender in May 1945 (V-E Day) and Japan's surrender in September 1945 (V-J Day) after the atomic bombings of Hiroshima and Nagasaki.",
        "answer": "1945",
    },
]

# ─── Build few-shot prompt strings ────────────────────────────────────────────

def _format_gsm8k_few_shot():
    lines = []
    for ex in GSM8K_FEW_SHOT_EXAMPLES:
        lines.append(f"Question: {ex['question']}")
        lines.append(f"Let's think step by step.\n{ex['reasoning']}")
        lines.append(f"The answer is {ex['answer']}.")
        lines.append("")
    return "\n".join(lines)

def _format_svamp_few_shot():
    lines = []
    for ex in SVAMP_FEW_SHOT_EXAMPLES:
        lines.append(f"Question: {ex['question']}")
        lines.append(f"Let's think step by step.\n{ex['reasoning']}")
        lines.append(f"The answer is {ex['answer']}.")
        lines.append("")
    return "\n".join(lines)

def _format_csqa_few_shot():
    lines = []
    for ex in CSQA_FEW_SHOT_EXAMPLES:
        lines.append(f"Question: {ex['question']}")
        lines.append(f"Choices:\n{ex['choices']}")
        lines.append(f"Let's think step by step.\n{ex['reasoning']}")
        lines.append(f"The answer is {ex['answer']}.")
        lines.append("")
    return "\n".join(lines)

def _format_trivia_few_shot():
    lines = []
    for ex in TRIVIAQA_FEW_SHOT_EXAMPLES:
        lines.append(f"Question: {ex['question']}")
        lines.append(f"Let's think step by step.\n{ex['reasoning']}")
        lines.append(f"The answer is {ex['answer']}.")
        lines.append("")
    return "\n".join(lines)

FEW_SHOT_COT_TEMPLATES = {
    "gsm8k": (
        "Answer math problems step by step, then state the final answer.\n\n"
        + _format_gsm8k_few_shot()
        + "Question: {question}\n"
        "Let's think step by step."
    ),
    "svamp": (
        "Answer math problems step by step, then state the final answer.\n\n"
        + _format_svamp_few_shot()
        + "Question: {question}\n"
        "Let's think step by step."
    ),
    "commonsenseqa": (
        "Choose the correct answer by thinking step by step.\n\n"
        + _format_csqa_few_shot()
        + "Question: {question}\n"
        "Choices:\n{choices}\n"
        "Let's think step by step."
    ),
    "triviaqa": (
        "Answer questions by thinking step by step.\n\n"
        + _format_trivia_few_shot()
        + "Question: {question}\n"
        "Let's think step by step."
    ),
}


def format_prompt(task: str, condition: str, question: str, choices: str = "") -> str:
    """
    Format a prompt for the given task and condition.

    Args:
        task: One of 'gsm8k', 'svamp', 'commonsenseqa', 'triviaqa'
        condition: One of 'standard', 'zero_shot_cot', 'few_shot_cot'
        question: The question text
        choices: Formatted choices string (for commonsenseqa)

    Returns:
        Formatted prompt string
    """
    templates = {
        "standard": STANDARD_TEMPLATES,
        "zero_shot_cot": ZERO_SHOT_COT_TEMPLATES,
        "few_shot_cot": FEW_SHOT_COT_TEMPLATES,
    }
    template = templates[condition][task]
    if task == "commonsenseqa":
        return template.format(question=question, choices=choices)
    return template.format(question=question)
