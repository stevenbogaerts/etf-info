from pl_random import PLRandom
from pl_utils import PLUtils
import textwrap


# ====================================================================
# Adjust behavior of the four functions below for your problem.
#
# This template ("nv" = n variants) extends mc_rv_printed by adding
# MAJOR VARIATIONS - different code skeletons randomly selected each
# time - on top of the usual MINOR RANDOMNESS within each skeleton.
#
# The three major variants all show a for loop with print(..., end=sep):
#   range_n            →  for i in range(n):
#   range_start_stop   →  for i in range(start, stop):
#   range_start_stop_step → for i in range(start, stop, step):
#
# Each variant has its own parameter generation, correct answer, and
# distractors. All dispatch on raw_params["variant"].
#
# To add or remove major variants:
#   1. Add/remove a variant key in _get_raw_parameters
#   2. Add/remove the matching branch in each of the four functions


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
        n = plr.integer(2, 5)
        raw_params["n"] = n
        raw_params["code"] = textwrap.dedent(f"""
            for i in range({n}):
                print(i, end="{sep}")
        """).strip()

    elif variant == "range_start_stop":
        # range(start, stop): start >= 1 so it doesn't look like range(n)
        # count is number of iterations; stop = start + count
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
    Compute and return the correct answer, always wrapped in PLUtils.code_block().

    For single-line output (using end="", end="_", etc.):
        return PLUtils.code_block("0_1_2_3_")

    For multi-line output (default newline behavior):
        return PLUtils.code_block("line1\nline2\nline3")
    '''
    sep = raw_params["sep"]
    variant = raw_params["variant"]

    if variant == "range_n":
        n = raw_params["n"]
        return PLUtils.code_block(sep.join(str(i) for i in range(n)) + sep)

    elif variant == "range_start_stop":
        start, stop = raw_params["start"], raw_params["stop"]
        return PLUtils.code_block(sep.join(str(i) for i in range(start, stop)) + sep)

    else:  # range_start_stop_step
        start, stop, step = raw_params["start"], raw_params["stop"], raw_params["step"]
        return PLUtils.code_block(sep.join(str(i) for i in range(start, stop, step)) + sep)


def _get_distractors(raw_params: dict, plr: PLRandom) -> list:
    '''
    Return a list of distractor dicts, each with:
      - "text": the distractor text, always wrapped in PLUtils.code_block()
      - "feedback": hint shown when this distractor is selected ("" for none)

    Each distractor should target a specific misconception.

    Tip: generate extra candidates here if some may be duplicates -
    the boilerplate deduplicates automatically, keeping the first
    len(returned list) unique entries.
    '''
    sep = raw_params["sep"]
    variant = raw_params["variant"]

    if variant == "range_n":
        n = raw_params["n"]
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

            # Misconception: nothing is printed
            {"text": "<em>(nothing is printed)</em>",
             "feedback": "print() is called on each iteration of the loop, so output is produced."},
        ]

    elif variant == "range_start_stop":
        start, stop = raw_params["start"], raw_params["stop"]
        return [
            # Misconception: forgetting start, treating range(start, stop) like range(stop)
            {"text": PLUtils.code_block(sep.join(str(i) for i in range(stop)) + sep),
             "feedback": f"range({start}, {stop}) starts at {start}, not 0."},

            # Misconception: off-by-one - including stop in the output
            {"text": PLUtils.code_block(sep.join(str(i) for i in range(start, stop + 1)) + sep),
             "feedback": f"range({start}, {stop}) stops before {stop}, not at {stop}."},

            # Misconception: ignoring end=, assuming print() uses a newline
            {"text": PLUtils.code_block("\n".join(str(i) for i in range(start, stop))),
             "feedback": f'end="{sep}" replaces the default newline - output stays on one line.'},

            # Misconception: the last element doesn't get the end= separator
            {"text": PLUtils.code_block(sep.join(str(i) for i in range(start, stop))),
             "feedback": f'end="{sep}" is applied after every print(), including the last.'},
        ]

    else:  # range_start_stop_step
        start, stop, step = raw_params["start"], raw_params["stop"], raw_params["step"]
        direction = "negative" if step < 0 else "positive"
        movement = "down" if step < 0 else "up"

        # Distractor 1: wrong step direction - negate the step
        reversed_vals = list(range(start, stop, -step))
        if reversed_vals:
            wrong_dir_text = PLUtils.code_block(sep.join(str(i) for i in reversed_vals) + sep)
        else:
            wrong_dir_text = "<em>(nothing is printed)</em>"
        wrong_dir_feedback = (
            f"The step is {step}; a {direction} step counts {movement}, "
            f"so using {-step} would go the wrong direction."
        )

        return [
            # Misconception: wrong step sign / direction
            {"text": wrong_dir_text,
             "feedback": wrong_dir_feedback},

            # Misconception: off-by-one - including the stop value
            {"text": PLUtils.code_block(
                sep.join(str(i) for i in range(start, stop + step, step)) + sep),
             "feedback": f"range(..., {stop}, ...) stops before reaching {stop}."},

            # Misconception: ignoring end=, assuming print() uses a newline
            {"text": PLUtils.code_block(
                "\n".join(str(i) for i in range(start, stop, step))),
             "feedback": f'end="{sep}" replaces the default newline - output stays on one line.'},

            # Misconception: the last element doesn't get the end= separator
            {"text": PLUtils.code_block(
                sep.join(str(i) for i in range(start, stop, step))),
             "feedback": f'end="{sep}" is applied after every print(), including the last.'},
        ]


def _get_fallback_distractor(
    raw_params: dict, used_values: set, index: int
) -> dict:
    '''
    Return one fallback distractor dict when _get_distractors produced a
    duplicate or a match with the correct answer.

    Strategy: vary the effective loop count by ±offset to produce a
    different-length output.

    - used_values: set of already-used PLUtils.normalize_for_comparison() strings.
    - index: increments each time a new fallback is needed (0, 1, 2, …).
    '''
    sep = raw_params["sep"]
    variant = raw_params["variant"]

    offsets = [index + 1, -(index + 1), index + 2, -(index + 2)]

    if variant == "range_n":
        n = raw_params["n"]
        for offset in offsets:
            new_n = n + offset
            if new_n >= 1:
                candidate = sep.join(str(i) for i in range(new_n)) + sep
                if PLUtils.normalize_for_comparison(candidate) not in used_values:
                    return {"text": PLUtils.code_block(candidate), "feedback": ""}

    elif variant == "range_start_stop":
        start, stop = raw_params["start"], raw_params["stop"]
        for offset in offsets:
            new_stop = stop + offset
            if new_stop > start:
                candidate = sep.join(str(i) for i in range(start, new_stop)) + sep
                if PLUtils.normalize_for_comparison(candidate) not in used_values:
                    return {"text": PLUtils.code_block(candidate), "feedback": ""}

    else:  # range_start_stop_step
        start, stop, step = raw_params["start"], raw_params["stop"], raw_params["step"]
        # Adjust count by offset: new_stop = start + step * (count + offset)
        count = abs(stop - start) // abs(step)
        for offset in offsets:
            new_count = count + offset
            if new_count >= 1:
                new_stop = start + step * new_count
                vals = list(range(start, new_stop, step))
                if vals:
                    candidate = sep.join(str(i) for i in vals) + sep
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
