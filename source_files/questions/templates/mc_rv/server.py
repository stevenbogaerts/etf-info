from pl_random import PLRandom
from pl_utils import PLUtils
import html


# ====================================================================
# Adjust behavior of the four functions below for your problem.


def _get_raw_parameters(plr: PLRandom) -> dict:
    '''
    Generate parameters of any type to define the problem.
    Return a dictionary mapping parameter key to parameter value.
    Values are available in question.html as {{ params.key }}.
    Use plr for any randomization.
    '''
    raw_params = {}
    raw_params["left"] = plr.integer(1, 9)
    raw_params["right"] = plr.integer(1, 9)
    return raw_params


def _get_correct_answer(raw_params: dict) -> str:
    '''
    Compute and return the correct answer as a string (plain text or HTML).
    raw_params contains the values from _get_raw_parameters.
    Can also be LaTeX: r"$x^2 + 1$"
    Or a code block: PLUtils.code_block("print('hello')")
    '''
    left = raw_params["left"]
    right = raw_params["right"]
    return str(left + right)


def _get_distractors(raw_params: dict, plr: PLRandom) -> list:
    '''
    Return a list of distractor dicts, each with:
      - "text": the distractor text
         (plain text, HTML-escaped, LaTeX, or code block)
      - "feedback": hint shown when this distractor is selected
        ("" for no hint)
    raw_params contains the values from _get_raw_parameters.
    plr is available for any additional randomization needed.

    Tip: generate extra candidates here if some may be duplicates -
    the boilerplate deduplicates automatically, keeping the first
    len(returned list) unique entries.
    '''
    left = raw_params["left"]
    right = raw_params["right"]

    return [
        {"text": str(left + right + 1),
         "feedback": "Off by one - check your arithmetic."},
        {"text": str(left + right - 1),
         "feedback": "Off by one - check your arithmetic."},
        {"text": str(left * right),
         "feedback": "That's multiplication, not addition."},
    ]


def _get_fallback_distractor(
    raw_params: dict, used_values: set, index: int
) -> dict:
    '''
    Return one fallback distractor dict when _get_distractors produced a
    duplicate or a match with the correct answer.

    - used_values:
      set of already-used PLUtils.normalize_for_comparison() strings
      (correct answer + accepted distractors).
      Use this to avoid further duplicates.
    - index: increments each time a new fallback is needed (0, 1, 2, …),
      so successive calls can produce different values.

    The returned dict must have "text" and "feedback" keys.
    It does NOT need to check used_values - the boilerplate handles that.
    Implement this so that varying index reliably produces distinct options.
    '''
    correct = int(_get_correct_answer(raw_params))
    candidates = [str(c) for c in [
        correct + index + 1,
        correct - (index + 1),
        correct + index + 2,
        correct - (index + 2)
    ]]

    # ------------------------------
    # Likely no changes needed below

    for candidate in candidates:
        if PLUtils.normalize_for_comparison(candidate) not in used_values:
            return {"text": candidate, "feedback": ""}

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
