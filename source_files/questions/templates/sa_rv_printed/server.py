from pl_random import PLRandom
from pl_utils import PLUtils
import textwrap


# ====================================================================
# Adjust behavior of the functions below for your problem.
#
# Key difference from sa_rv_str: _get_raw_parameters must also build and
# store raw_params["code"] - the Python code string shown in the question.
#
# _get_correct_answer returns the output as a plain string (not a code block),
# since it is used for grading comparison.
# For multi-line output, embed newlines: "line1\nline2\nline3"

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
    Compute and return the correct answer as a plain string.
    This is used directly for grading comparison.

    For single-line output (using end="", end="_", etc.):
        return the output string, e.g. "0_1_2_3_"

    For multi-line output (default newline behavior):
        return lines joined with newlines, e.g. "line1\nline2\nline3"
        (The student is expected to enter only the first line, or all lines
        separated by newlines, depending on how you phrase the question.)
    '''
    n = raw_params["n"]
    sep = raw_params["sep"]
    return sep.join(str(i) for i in range(n)) + sep


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
