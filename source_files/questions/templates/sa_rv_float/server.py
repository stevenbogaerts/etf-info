from typing import Any
import numpy as np

from pl_random import PLRandom
from pl_utils import PLUtils

# ====================================================================
# Adjust behavior of _get_raw_parameters and _get_correct_answer as needed for your problem.


def _get_raw_parameters(plr: PLRandom) -> dict:
    '''
    Generate parameters of any type to define the problem.
    Return a dictionary mapping parameter key to parameter value.
    Values are available in question.html as {{ params.key }}.
    Use plr for any randomization.
    '''
    raw_params = {}
    raw_params["left"] = plr.num(0.1, 9.9, digits_after=1)
    raw_params["right"] = plr.num(0.1, 9.9, digits_after=1)
    return raw_params


def _get_correct_answer(raw_params: dict) -> tuple[float, int]:
    '''
    Compute and return the correct answer tuple (float, decimal_places).
    The float should already be rounded to those decimal places.
    The decimal_places int is used for grading
    and to tell the student how to format their answer.
    raw_params contains the values from _get_raw_parameters.
    '''
    left = raw_params["left"]
    right = raw_params["right"]
    total = left + right

    decimal_places = 1
    total = np.round(total, decimal_places)
    return total, decimal_places


def _get_feedback(is_correct: bool, submitted: str, correct: str,
                  params: dict) -> str:
    """
    Return an extra hint string, or "" for none.
    Appended to any automatic feedback (e.g. precision errors).
    - is_correct: True if the student's answer was fully correct
    - submitted:  the raw string the student entered
    - correct:    the correct answer value
    - params:     all params set in _get_raw_parameters()
    """
    if is_correct:
        return ""
    return "Hint/Feedback text here"


# ====================================================================
# All other code is boilerplate and probably shouldn't be changed.


def generate(data: dict) -> None:
    plr = PLRandom(data["variant_seed"])

    raw_params = _get_raw_parameters(plr)
    correct_answer, decimal_places = _get_correct_answer(raw_params)

    params: dict[str, Any] = {k: str(v) for k, v in raw_params.items()}
    params["decimal_places"] = decimal_places
    data["params"] = params

    if decimal_places == 0:
        data["params"]["answer_format_phrase"] = "Round your answer to the nearest integer."
    else:
        data["params"]["answer_format_phrase"] = (
            f"Round to {decimal_places} decimal place(s)."
        )
    data["correct_answers"]["answer"] = correct_answer


def grade(data: dict) -> None:
    submitted = data.get("submitted_answers", {}).get("answer", "").strip()
    correct = data.get("correct_answers", {}).get("answer", "")
    dp = data.get("params", {}).get("decimal_places", 0)

    score, auto_feedback = PLUtils.check_numeric_answer(
        submitted,
        correct,
        tolerance=0.0,
        mode="absolute",
        required_decimal_places=dp,
    )

    extra = _get_feedback(score == 1.0, submitted, str(correct), data["params"])
    feedback = " ".join(filter(None, [auto_feedback, extra]))
    PLUtils.apply_score(data, "answer", score, feedback)
