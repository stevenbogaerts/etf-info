import re

from pl_random import PLRandom
from pl_utils import PLUtils

# ====================================================================
# Edit these flags and functions for your problem.
#
# Use this template when the expected answer is a short, single-line Python
# expression or statement and the number of valid forms is small enough that
# regex can capture all of them. If there are too many valid forms, use a
# code_* template with external grading instead.
#
# Grading: the answer is accepted if ALL patterns in ANY ONE group match.
# Each group is a list of patterns (AND within a group).
# The groups themselves are OR-ed: any fully matching group → correct.

# Grading normalization: whitespace is handled here, not in question.html.
ignore_leading_trailing_whitespace = True
ignore_internal_whitespace = False  # False: spacing usually matters in code


def _get_raw_parameters(plr: PLRandom) -> dict:
    '''
    Generate parameters of any type to define the problem.
    Return a dictionary mapping parameter key to parameter value.
    Values are available in question.html as {{ params.key }}.
    Use plr for any randomization.
    '''
    raw_params = {}
    raw_params["n"] = plr.integer(2, 8)
    return raw_params


def _get_correct_pattern_groups(params: dict) -> list:
    '''
    Return a list of pattern groups. The answer is correct when ALL patterns
    in ANY ONE group match the submitted answer via re.search.

        [                          # outer list: OR across groups
            [p1, p2],              # group 1: correct if p1 AND p2 both match
            [p3],                  # group 2: correct if p3 matches
        ]

    params values are strings (e.g. params["n"] == "5"), which is fine since
    patterns are built with f-strings that stringify values anyway.

    Tips:
    - Use r"..." raw strings to avoid double-escaping backslashes.
    - \\s* matches optional whitespace (e.g. around operators).
    - \\b marks a word boundary (avoids matching partial words).
    - Patterns are case-sensitive.
    - A group with a single pattern is fine when one regex covers a valid form.
    '''
    n1 = int(params["n"]) + 1
    return [
        [rf"range\s*\(\s*{n1}\s*\)"],                    # range(n+1)
        [rf"range\s*\(\s*0\s*,\s*{n1}\s*\)"],            # range(0, n+1)
        [rf"range\s*\(\s*0\s*,\s*{n1}\s*,\s*1\s*\)"],   # range(0, n+1, 1)
    ]


def _get_feedback(is_correct: bool, submitted: str, groups: list,
                  params: dict) -> str:
    """
    Return a feedback string shown to the student, or "" for no feedback.
    - is_correct: True if the student's answer was accepted
    - submitted:  the normalized answer the student entered
    - groups:     the list returned by _get_correct_pattern_groups()
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

    return normalized


# ====================================================================
# Boilerplate below - no changes needed for a standard code answer question.


def generate(data: dict) -> None:
    plr = PLRandom(data["variant_seed"])

    raw_params = _get_raw_parameters(plr)
    data["params"] = {k: str(v) for k, v in raw_params.items()}


def grade(data: dict) -> None:
    submitted_raw = str(data.get("submitted_answers", {}).get("answer", ""))
    submitted = _normalize_for_grading(submitted_raw)

    # Treat whitespace-only submissions as blank when normalization is on.
    if (
        ignore_leading_trailing_whitespace or ignore_internal_whitespace
    ) and submitted == "":
        PLUtils.apply_score(data, "answer", 0.0, "")
        return

    # Groups are recomputed from params rather than stored in data["params"],
    # so they are never exposed as template variables.
    groups = _get_correct_pattern_groups(data["params"])
    is_correct = any(
        all(re.search(p, submitted) for p in group)
        for group in groups
    )

    score = 1.0 if is_correct else 0.0
    PLUtils.apply_score(data, "answer", score,
                        _get_feedback(is_correct, submitted, groups,
                                      data["params"]))
