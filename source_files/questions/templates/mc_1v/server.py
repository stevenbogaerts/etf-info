from pl_utils import PLUtils
import html


# ====================================================================
# Edit these functions for your problem.


def generate(data):
    # Plain text answer. Can also be LaTeX: r"$x^2 + 1$"
    data["params"]["correct"] = "CORRECT ANSWER"

    plaintext_distractor = "This is a plain text distractor."
    plaintext_with_special_chars = html.escape(
        "Distractor with special chars: <, >, &"
    )
    latex_distractor = r"LaTeX distractor: $x^2 + 1$"
    one_line_code = PLUtils.code_block("print('Hello, world!')")
    multiline_code = PLUtils.code_block("""
        x = [1, 2, 3]
        print(x[0])
        1
    """)

    # Add "feedback" to any distractor to show a hint when it's selected.
    # Omit "feedback" (or use "") for no hint on that distractor.
    data["params"]["distractors"] = [
        {"text": plaintext_distractor, "feedback": "Plaintext distractor hint."},
        {"text": plaintext_with_special_chars, "feedback": "Distractor with special chars hint."},
        {"text": latex_distractor, "feedback": "LaTeX distractor hint."},
        {"text": one_line_code, "feedback": "One-line code hint."},
        {"text": multiline_code, "feedback": "Multiline code hint."},
    ]


# No grade() needed - PL auto-grades MC and renders per-answer feedback
# from the "feedback" key on each distractor dict.
