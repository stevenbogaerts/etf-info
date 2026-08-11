from pl_random import PLRandom
from pl_utils import PLUtils

# ====================================================================
# Edit these flags and functions for your problem.

# Grading normalization: whitespace is handled here, not in question.html.
ignore_case = False
ignore_leading_trailing_whitespace = True
# collapses internal spaces: "a b" → "ab"
ignore_internal_whitespace = True


def _get_raw_parameters(plr: PLRandom) -> dict:
    '''
    Generate parameters of any type to define the problem.
    Return a dictionary mapping parameter key to parameter value.
    Values are available in question.html as {{ params.key }}.
    Use plr for any randomization.
    '''
    raw_params = {}
    raw_params["animal"] = plr.choice(["cat", "dog", "fish"])
    raw_params["color"] = plr.choice(["red", "blue", "green"])
    return raw_params


def _get_correct_answer(raw_params: dict) -> str:
    '''
    Compute and return the correct answer string.
    raw_params contains the values from _get_raw_parameters.
    '''
    if raw_params["animal"] == "cat":
        answer = "yes"
    elif raw_params["color"] == "blue":
        answer = "no"
    else:
        answer = "maybe"
    return answer


def _get_feedback(is_correct: bool, submitted: str, correct: str,
                  params: dict) -> str:
    """
    Return a feedback string shown to the student, or "" for no feedback.
    - is_correct: True if the student's answer was accepted
    - submitted:  the normalized answer the student entered
    - correct:    the correct answer string
    - params:     all params set in _get_raw_parameters()
    """
    if is_correct:
        return ""
    return "Hint/Feedback text here"


def _normalize_for_grading(value: str) -> str:
    normalized = value

    if ignore_leading_trailing_whitespace:
        normalized = normalized.strip()

    if ignore_internal_whitespace:
        normalized = "".join(normalized.split())

    if ignore_case:
        normalized = normalized.lower()

    return normalized


# ====================================================================
# Boilerplate below - no changes needed for a standard string answer question.


def generate(data: dict) -> None:
    plr = PLRandom(data["variant_seed"])

    raw_params = _get_raw_parameters(plr)
    data["params"] = {k: str(v) for k, v in raw_params.items()}
    data["correct_answers"]["answer"] = _get_correct_answer(raw_params)


def grade(data: dict) -> None:
    submitted_raw = str(data.get("submitted_answers", {}).get("answer", ""))
    correct_raw = str(data.get("correct_answers", {}).get("answer", ""))

    submitted_normalized = _normalize_for_grading(submitted_raw)
    correct_normalized = _normalize_for_grading(correct_raw)

    # Treat whitespace-only submissions as blank when whitespace normalization is enabled.
    if (
        ignore_leading_trailing_whitespace or ignore_internal_whitespace
    ) and submitted_normalized == "":
        PLUtils.apply_score(data, "answer", 0.0, "")
        return

    score = 1.0 if submitted_normalized == correct_normalized else 0.0
    PLUtils.apply_score(data, "answer", score,
                        _get_feedback(score == 1.0, submitted_normalized,
                                  correct_normalized, data["params"]))
