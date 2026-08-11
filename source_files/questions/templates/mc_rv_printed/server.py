from pl_random import PLRandom
from pl_utils import PLUtils
import textwrap


# ====================================================================
# Adjust behavior of the four functions below for your problem.
#
# Key difference from mc_rv: _get_raw_parameters must also build and
# store raw_params["code"] - the Python code string shown in the question.
#
# For the correct answer and distractors, always wrap the output string in
# PLUtils.code_block(), e.g. PLUtils.code_block("0_1_2_3_")
# For multi-line output, embed newlines: PLUtils.code_block("0\n1\n2\n3")
#
# Distractors should each target a specific student misconception
# about the topic being tested.


def _get_raw_parameters(plr: PLRandom) -> dict:
    '''
    Generate parameters to define the problem.
    Return a dictionary mapping parameter key to parameter value.
    Values are available in question.html as {{ params.key }}.
    Use plr for any randomization.

    IMPORTANT: Also build and store raw_params["code"] here - the Python
    code string that will be displayed to the student in the question.
    '''
    raw_params = {}
    raw_params["n"] = plr.integer(3, 6)
    raw_params["sep"] = plr.choice(["_", "-", "|"])

    n = raw_params["n"]
    sep = raw_params["sep"]
    raw_params["code"] = textwrap.dedent(f"""
        for i in range({n}):
            print(i, end="{sep}")
    """).strip()

    return raw_params


def _get_correct_answer(raw_params: dict) -> str:
    '''
    Compute and return the correct answer, always wrapped in PLUtils.code_block().

    For single-line output (using end="", end="_", etc.):
        return PLUtils.code_block("0_1_2_3_")

    For multi-line output (default newline behavior):
        return PLUtils.code_block("line1\nline2\nline3")
    '''
    n = raw_params["n"]
    sep = raw_params["sep"]
    return PLUtils.code_block(sep.join(str(i) for i in range(n)) + sep)


def _get_distractors(raw_params: dict, plr: PLRandom) -> list:
    '''
    Return a list of distractor dicts, each with:
      - "text": the distractor text, always wrapped in PLUtils.code_block()
      - "feedback": hint shown when this distractor is selected ("" for none)

    Each distractor should target a specific misconception.
    See the comments at the top of this file for common misconception types.

    Tip: generate extra candidates here if some may be duplicates -
    the boilerplate deduplicates automatically, keeping the first
    len(returned list) unique entries.
    '''
    n = raw_params["n"]
    sep = raw_params["sep"]

    return [
        # Misconception: range(n) starts at 1 instead of 0
        {"text": PLUtils.code_block(sep.join(str(i) for i in range(1, n + 1)) + sep),
         "feedback": f"range({n}) starts at 0, not 1."},

        # Misconception: the last element doesn't get the end= separator
        {"text": PLUtils.code_block(sep.join(str(i) for i in range(n))),
         "feedback": f'end="{sep}" is applied after every print(), including the last.'},

        # Misconception: ignoring end=, assuming print() uses a newline by default
        {"text": PLUtils.code_block("\n".join(str(i) for i in range(n))),
         "feedback": f'end="{sep}" replaces the default newline - output stays on one line.'},

        # Misconception: nothing is printed (wrong belief about control flow or range)
        {"text": "<em>(nothing is printed)</em>",
         "feedback": "print() is called on each iteration of the loop, so output is produced."},
    ]


def _get_fallback_distractor(
    raw_params: dict, used_values: set, index: int
) -> dict:
    '''
    Return one fallback distractor dict when _get_distractors produced a
    duplicate or a match with the correct answer.

    For print-output questions, fallbacks should look like plausible outputs.
    Strategy: vary the loop bound by ±offset to produce a different-length output.

    - used_values: set of already-used PLUtils.normalize_for_comparison() strings.
    - index: increments each time a new fallback is needed (0, 1, 2, …).
    '''
    n = raw_params["n"]
    sep = raw_params["sep"]

    # Try expanding then contracting the range by increasing offsets
    offsets = [index + 1, -(index + 1), index + 2, -(index + 2)]
    for offset in offsets:
        new_n = n + offset
        if new_n >= 1:
            candidate = sep.join(str(i) for i in range(new_n)) + sep
            if PLUtils.normalize_for_comparison(candidate) not in used_values:
                return {"text": PLUtils.code_block(candidate), "feedback": ""}

    # Last resort - should never be reached with reasonable index values
    return {"text": f"(option {index})", "feedback": ""}


# ====================================================================
# All other code is boilerplate and probably shouldn't be changed.


def _deduplicate_distractors(
    candidates: list, correct: str, raw_params: dict, n_needed: int
) -> list:
    norm_correct = PLUtils.normalize_for_comparison(correct)
    seen = {norm_correct}
    unique = []
    for d in candidates:
        norm = PLUtils.normalize_for_comparison(d["text"])
        if norm not in seen:
            seen.add(norm)
            unique.append(d)
    i = 0
    while len(unique) < n_needed:
        fb = _get_fallback_distractor(raw_params, seen, i)
        norm = PLUtils.normalize_for_comparison(fb["text"])
        if norm not in seen:
            seen.add(norm)
            unique.append(fb)
        i += 1
        if i > 100:  # hard safety cap
            break
    return unique[:n_needed]


def generate(data: dict) -> None:
    plr = PLRandom(data["variant_seed"])

    raw_params = _get_raw_parameters(plr)
    data["params"] = {k: str(v) for k, v in raw_params.items()}
    correct = _get_correct_answer(raw_params)
    data["params"]["correct"] = correct
    candidates = _get_distractors(raw_params, plr)
    data["params"]["distractors"] = _deduplicate_distractors(
        candidates, correct, raw_params, len(candidates)
    )


# No grade() needed - PL auto-grades MC and renders per-answer feedback
# from the "feedback" key on each distractor dict.
