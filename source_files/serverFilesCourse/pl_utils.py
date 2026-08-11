from decimal import Decimal, InvalidOperation
import html
import re
import textwrap
import numpy as np
from typing import Any


class PLUtils:
    """
    Stateless utility methods for PrairieLearn question authoring.
    Complements PLRandom - no seed or instance state needed,
    so all methods are static.
    """

    # ------------------------------------------------------------------ #
    #  Number formatting                                                 #
    # ------------------------------------------------------------------ #

    @staticmethod
    def count_decimal_places(text: str) -> int:
        """Count decimal places in a numeric string like '3.14' -> 2"""
        if "." not in text:
            return 0
        return len(text.split(".", 1)[1])

    @staticmethod
    def format_number(
        value: float,
        digits_after: int | None = None,
        sig_figs: int | None = None
    ) -> str:
        """
        Smart number formatter.
        - digits_after: fixed decimal places,
          e.g. format_number(3.1, digits_after=2) -> '3.10'
        - sig_figs: significant figures,
          e.g. format_number(3.14159, sig_figs=3) -> '3.14'
        - neither: drops trailing zeros, integers show without decimal point
        """
        if digits_after is not None:
            return f"{value:.{digits_after}f}"
        if sig_figs is not None:
            from math import floor, log10
            if value == 0:
                return "0"
            magnitude = floor(log10(abs(value)))
            decimal_places = max(0, sig_figs - 1 - magnitude)
            return f"{value:.{decimal_places}f}"
        # Default: clean formatting
        if value == int(value):
            return str(int(value))
        return f"{value:g}"

    @staticmethod
    def latex_matrix(arr: np.ndarray, fmt: str = "g") -> str:
        """
        Format a 1D or 2D numpy array as a LaTeX bmatrix string.
        e.g. [[1,2],[3,4]] -> r'\begin{bmatrix}1 & 2\\3 & 4\end{bmatrix}'
        """
        arr = np.atleast_2d(arr)
        rows = r" \\ ".join(
            " & ".join(f"{v:{fmt}}" for v in row)
            for row in arr
        )
        return rf"\begin{{bmatrix}}{rows}\end{{bmatrix}}"

    # ------------------------------------------------------------------ #
    #  HTML / display helpers                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def code_block(code: str, language: str = "python") -> str:
        """
        Convert a (possibly indented) multi-line string into an HTML code block
        suitable for use as a <pl-answer> value via {{{text}}} in question.html.

        Usage in server.py:
            from pl_utils import PLUtils
            answer = PLUtils.code_block(\"\"\"
                x = [1, 2, 3]
                print(x[0])
                1
            \"\"\")

        Strips common leading whitespace (textwrap.dedent) and escapes
        HTML special characters so < > & in code render correctly.
        The language argument is included as a CSS class for syntax highlighting.

        Only leading/trailing blank lines are stripped (not spaces), so
        column-aligned output (e.g. a printed pandas DataFrame, whose header
        row is indented further than its data rows) keeps its alignment.
        """
        code = textwrap.dedent(code).strip('\n')
        escaped = html.escape(code)
        return f'<pre class="bg-light border rounded p-2"><code class="language-{language}">{escaped}</code></pre>'

    # ------------------------------------------------------------------ #
    #  Distractor / MC helpers                                           #
    # ------------------------------------------------------------------ #

    @staticmethod
    def normalize_for_comparison(text: str) -> str:
        """
        Normalize distractor/answer text for uniqueness checking.
        Strips HTML tags (e.g. from code_block output) and collapses whitespace.
        Case is preserved - code answers may be case-sensitive (True vs true).
        """
        no_tags = re.sub(r"<[^>]+>", "", text)
        return re.sub(r"\s+", " ", no_tags).strip()

    # ------------------------------------------------------------------ #
    #  Answer parsing & grading                                          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def parse_number_safe(text: str) -> Decimal | None:
        """
        Safely parse a student-submitted string to Decimal.
        Returns None if parsing fails, avoiding try/except in every grade().
        """
        try:
            return Decimal(text.strip())
        except InvalidOperation:
            return None

    @staticmethod
    def check_answer_in_range(
        submitted: float | Decimal,
        correct: float | Decimal,
        tolerance: float = 0.01,
        mode: str = "percent",
    ) -> bool:
        """
        Check if submitted is within tolerance of correct.
        mode='percent': tolerance is a fraction, e.g. 0.01 = 1%
        mode='absolute': tolerance is an absolute value
        """
        submitted = float(submitted)  # ensure submitted is a float for comparison
        correct = float(correct)  # ensure correct is a float for comparison

        if mode == "percent":
            if correct == 0:
                return abs(submitted - correct) <= tolerance
            return abs(submitted - correct) / abs(correct) <= tolerance
        elif mode == "absolute":
            return abs(submitted - correct) <= tolerance
        else:
            raise ValueError(
                f"Unknown mode '{mode}'. Use 'percent' or 'absolute'."
            )

    @staticmethod
    def sig_fig_check(text: str, expected_sig_figs: int) -> bool:
        """
        Check whether a submitted numeric string has the expected number
        of significant figures. e.g. '0.0340' -> 3 sig figs.
        """
        text = text.strip().lstrip("-")
        # Remove leading zeros and decimal point for counting
        digits = text.replace(".", "")
        digits = digits.lstrip("0")
        # Trailing zeros after decimal point are significant
        return len(digits) == expected_sig_figs

    @staticmethod
    def check_numeric_answer(
        submitted_str: str,
        correct: float,
        tolerance: float = 0.01,
        mode: str = "percent",
        required_decimal_places: int | None = None,
        required_sig_figs: int | None = None,
    ) -> tuple[float, str]:
        """
        One-stop grading helper. Returns (score, feedback).

        Checks in order:
          1. Can it be parsed?
          2. Is it numerically correct (within tolerance)?
          3. Does it have the right decimal places or sig figs?

        Partial credit (0.5) for correct value with wrong precision.
        """
        correct = float(correct)  # ensure correct is a float for comparison
        parsed = PLUtils.parse_number_safe(submitted_str)
        if parsed is None:
            return 0.0, "Your answer could not be interpreted as a number."

        numerically_correct = PLUtils.check_answer_in_range(parsed, correct, tolerance, mode)

        precision_correct = True
        precision_feedback = ""

        if required_decimal_places is not None:
            actual_dp = PLUtils.count_decimal_places(submitted_str.strip())
            if actual_dp != required_decimal_places:
                precision_correct = False
                precision_feedback = (
                    f"Write your answer with exactly {required_decimal_places} decimal place(s)."
                )

        if required_sig_figs is not None:
            if not PLUtils.sig_fig_check(submitted_str, required_sig_figs):
                precision_correct = False
                precision_feedback = (
                    f"Write your answer with exactly {required_sig_figs} significant figure(s)."
                )

        if numerically_correct and precision_correct:
            return 1.0, ""
        elif numerically_correct:
            return 0.5, "The value is correct, but check the precision. " + precision_feedback
        else:
            return 0.0, "The value is incorrect."

    # ------------------------------------------------------------------ #
    #  Feedback / scoring structure                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def apply_score(data: dict, key: str, score: float, feedback: str = "") -> None:
        """
        Write score and feedback into data in one call.
        Handles both data['score'] and data['partial_scores'][key].

        Feedback is written to data['partial_scores'][key]['feedback'],
        which PrairieLearn renders automatically next to the answer element.
        """
        data.setdefault("partial_scores", {})
        data["score"] = score
        data["partial_scores"][key] = {"score": score}
        if feedback:
            data["partial_scores"][key]["feedback"] = feedback
            data.setdefault("feedback", {})["general"] = feedback

    def __repr__(self):
        return "PLUtils()"
