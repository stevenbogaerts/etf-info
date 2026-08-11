from pl_utils import PLUtils
import html


# ====================================================================
# Edit these functions for your problem.


def generate(data):
    # Add or remove statements freely - question.html loops over all of them.
    # Each statement's "match" value must equal the "name" of one option below.
    # Option text can be plain text, html.escape(...), LaTeX, or PLUtils.code_block(...).
    data["params"]["statements"] = [
        {"text": "STATEMENT 1", "match": "option_1"},
        {"text": "STATEMENT 2", "match": "option_2"},
        {"text": "STATEMENT 3", "match": "option_3"},
        # add more {"text": ..., "match": ...} entries as needed
    ]

    plaintext_option = "Plain text option"
    plaintext_with_special_chars = html.escape(
        "Option with special chars: <, >, &"
    )
    latex_option = r"LaTeX option: $x^2 + 1$"
    one_line_code = PLUtils.code_block("print('Hello, world!')")
    multiline_code = PLUtils.code_block("""
        x = [1, 2, 3]
        print(x[0])
        1
    """)

    # Add or remove options freely. Extra options (no matching statement) are distractors.
    # Option names must be unique and match the "match" values used in statements above.
    data["params"]["options"] = [
        {"name": "option_1", "text": plaintext_option},
        {"name": "option_2", "text": plaintext_with_special_chars},
        {"name": "option_3", "text": latex_option},
        {"name": "option_4", "text": one_line_code},
        {"name": "distractor_1", "text": multiline_code},
        # add more {"name": ..., "text": ...} entries as needed
    ]


# No grade() needed - PL auto-grades pl-matching using the "match"
# values in each statement and the selected option names.
