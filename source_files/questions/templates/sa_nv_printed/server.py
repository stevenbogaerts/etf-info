from pl_random import PLRandom
from pl_utils import PLUtils
import textwrap


# ====================================================================
# Adjust behavior of the functions below for your problem.
#
# This template ("nv" = n variants) extends sa_rv_printed by adding
# MAJOR VARIATIONS - different code skeletons randomly selected each
# time - on top of the usual MINOR RANDOMNESS within each skeleton.
#
# The three major variants all show a for loop with print(..., end=sep):
#   range_n            →  for i in range(n):
#   range_start_stop   →  for i in range(start, stop):
#   range_start_stop_step → for i in range(start, stop, step):
#
# Each variant has its own minor-randomness rules (see _get_raw_parameters).
# raw_params["variant"] controls which major variation is shown.
#
# _get_correct_answer returns the output as a plain string (not a code block),
# since it is used for grading comparison.
#
# To add or remove major variants:
#   1. Add/remove a variant key in _get_raw_parameters
#   2. Add/remove the matching branch in _get_correct_answer

# Grading normalization: whitespace is handled here, not in question.html.
ignore_case = False
ignore_leading_trailing_whitespace = True
ignore_internal_whitespace = True


def _get_raw_parameters(plr: PLRandom) -> dict:
    '''
    Generate parameters to define the problem.
    Return a dictionary mapping parameter key to parameter value.
    Values are available in question.html as {{ params.key }}.
    Use plr for any randomization.

    IMPORTANT: Also build and store raw_params["code"] here - the Python
    code string that will be displayed to the student in the question.

    raw_params["variant"] controls which major variation is shown.
    '''
    raw_params = {}
    variant = plr.choice(["range_n", "range_start_stop", "range_start_stop_step"])
    raw_params["variant"] = variant

    sep = plr.choice(["_", "-", "|"])
    raw_params["sep"] = sep

    if variant == "range_n":
        # range(n): loop runs n times, i from 0 to n-1
        # Restriction: loop executes between 2 and 5 times inclusive
        n = plr.integer(2, 5)
        raw_params["n"] = n
        raw_params["code"] = textwrap.dedent(f"""
            for i in range({n}):
                print(i, end="{sep}")
        """).strip()

    elif variant == "range_start_stop":
        # range(start, stop): start >= 1 so it doesn't look like range(n)
        # count is number of iterations; stop = start + count
        # Restriction: loop executes between 2 and 5 times inclusive
        start = plr.integer(1, 4)
        count = plr.integer(2, 5)
        stop = start + count
        raw_params["start"] = start
        raw_params["stop"] = stop
        raw_params["code"] = textwrap.dedent(f"""
            for i in range({start}, {stop}):
                print(i, end="{sep}")
        """).strip()

    else:  # range_start_stop_step
        # Two sub-cases: positive step (2 or 3) or negative step (-1, -2, -3).
        # Positive step uses step != 1 so it's clearly different from range_start_stop.
        # Negative step forces stop < start, testing direction understanding.
        # Restriction: loop executes between 2 and 4 times inclusive in both sub-cases
        if plr.bool():
            # Positive step
            step = plr.choice([2, 3])
            start = plr.integer(0, 3)
            count = plr.integer(2, 4)
            stop = start + step * count
        else:
            # Negative step
            step = plr.choice([-1, -2, -3])
            count = plr.integer(2, 4)
            stop = plr.integer(0, 3)       # small positive-ish end value
            start = stop + abs(step) * count
        raw_params["start"] = start
        raw_params["stop"] = stop
        raw_params["step"] = step
        raw_params["code"] = textwrap.dedent(f"""
            for i in range({start}, {stop}, {step}):
                print(i, end="{sep}")
        """).strip()

    return raw_params


def _get_correct_answer(raw_params: dict) -> str:
    '''
    Compute and return the correct answer as a plain string.
    This is used directly for grading comparison.

    For single-line output (using end="", end="_", etc.):
        return the output string, e.g. "0_1_2_3_"
    '''
    sep = raw_params["sep"]
    variant = raw_params["variant"]

    if variant == "range_n":
        n = raw_params["n"]
        return sep.join(str(i) for i in range(n)) + sep

    elif variant == "range_start_stop":
        start, stop = raw_params["start"], raw_params["stop"]
        return sep.join(str(i) for i in range(start, stop)) + sep

    else:  # range_start_stop_step
        start, stop, step = raw_params["start"], raw_params["stop"], raw_params["step"]
        return sep.join(str(i) for i in range(start, stop, step)) + sep


def _get_feedback(is_correct: bool, submitted: str, correct: str,
                  params: dict) -> str:
    """
    Return a feedback string shown to the student, or "" for no feedback.
    - is_correct: True if the student's answer was accepted
    - submitted:  the normalized answer the student entered
    - correct:    the normalized correct answer string
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
# Boilerplate below - no changes needed for a standard printed-output question.


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
