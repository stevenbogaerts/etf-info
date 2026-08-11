import random
from code_feedback import Feedback
from pl_helpers import name, points
from pl_unit_test import PLTestCase


class Test(PLTestCase):

    # ------------------------------------------------------------------
    # Rubric (12 pts total):
    #   2 pts  - Provided examples (small fixed cases)
    #   2 pts  - Edge case: x = 0
    #   4 pts  - Positive inputs (fixed + random)
    #   4 pts  - Negative inputs (fixed + random)
    # ------------------------------------------------------------------

    @points(2)
    @name("Provided examples")
    def test_provided_example(self):
        cases = [(1, 2), (3, 5), (2, 10)]
        for x, n in cases:
            user_val = Feedback.call_user(self.st.my_function, x, n)
            ref_val = self.ref.my_function(x, n)
            if user_val != ref_val:
                Feedback.add_feedback(
                    f"my_function({x}, {n}) returned {user_val!r}, "
                    f"expected {ref_val!r}"
                )
                Feedback.set_score(0)
                return
        Feedback.set_score(1)

    @points(2)
    @name("Edge case: x = 0")
    def test_zero(self):
        for n in [1, 5, 9]:
            user_val = Feedback.call_user(self.st.my_function, 0, n)
            ref_val = self.ref.my_function(0, n)
            if user_val != ref_val:
                Feedback.add_feedback(
                    f"my_function(0, {n}) returned {user_val!r}, "
                    f"expected {ref_val!r}"
                )
                Feedback.set_score(0)
                return
        Feedback.set_score(1)

    @points(4)
    @name("Positive inputs")
    def test_positive(self):
        fixed = [(4, 3), (10, 7), (100, 2)]
        rand = [(random.randint(1, 50), random.randint(2, 9))
                for _ in range(4)]
        for x, n in fixed + rand:
            user_val = Feedback.call_user(self.st.my_function, x, n)
            ref_val = self.ref.my_function(x, n)
            if user_val != ref_val:
                Feedback.add_feedback(
                    f"my_function({x}, {n}) returned {user_val!r}, "
                    f"expected {ref_val!r}"
                )
                Feedback.set_score(0)
                return
        Feedback.set_score(1)

    @points(4)
    @name("Negative inputs")
    def test_negative(self):
        fixed = [(-1, 3), (-7, 5), (-10, 2)]
        rand = [(random.randint(-50, -1), random.randint(2, 9))
                for _ in range(4)]
        for x, n in fixed + rand:
            user_val = Feedback.call_user(self.st.my_function, x, n)
            ref_val = self.ref.my_function(x, n)
            if user_val != ref_val:
                Feedback.add_feedback(
                    f"my_function({x}, {n}) returned {user_val!r}, "
                    f"expected {ref_val!r}"
                )
                Feedback.set_score(0)
                return
        Feedback.set_score(1)
