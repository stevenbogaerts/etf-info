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
    raw_params["left"] = plr.integer(1, 9)
    raw_params["right"] = plr.integer(1, 9)
    return raw_params


def _get_correct_answer(raw_params: dict) -> int:
    '''
    Compute and return the correct answer int.
    raw_params contains the values from _get_raw_parameters.
    '''
    left = raw_params["left"]
    right = raw_params["right"]
    return left + right


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
    data["params"] = {k: str(v) for k, v in raw_params.items()}
    data["correct_answers"]["answer"] = _get_correct_answer(raw_params)


def grade(data: dict) -> None:
    submitted = data.get("submitted_answers", {}).get("answer", "").strip()
    correct = data.get("correct_answers", {}).get("answer", "")

    score, auto_feedback = PLUtils.check_numeric_answer(
        submitted,
        correct,
        tolerance=0.0,
        mode="absolute",
        required_decimal_places=0,
    )

    extra = _get_feedback(score == 1.0, submitted, str(correct), data["params"])
    feedback = " ".join(filter(None, [auto_feedback, extra]))
    PLUtils.apply_score(data, "answer", score, feedback)
