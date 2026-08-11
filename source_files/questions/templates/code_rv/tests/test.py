import random
from code_feedback import Feedback
from pl_helpers import name, points
from pl_unit_test import PLTestCase


class Test(PLTestCase):

    # ------------------------------------------------------------------
    # Rubric (12 pts total):
    #   2 pts  - Provided example (matches question text)
    #   2 pts  - Edge case: x = 0
    #   4 pts  - Positive inputs (fixed + random)
    #   4 pts  - Negative inputs (fixed + random)
    # ------------------------------------------------------------------

    def _get_fns(self):
        func_name = self.data['params']['func_name']
        return getattr(self.st, func_name), getattr(self.ref, func_name), func_name

    @points(2)
    @name("Provided example")
    def test_provided_example(self):
        user_fn, ref_fn, func_name = self._get_fns()
        example_input = self.data['params']['example_input']
        user_val = Feedback.call_user(user_fn, example_input)
        ref_val = ref_fn(example_input)
        if user_val != ref_val:
            Feedback.add_feedback(
                f"{func_name}({example_input}) returned {user_val!r}, "
                f"expected {ref_val!r}"
            )
            Feedback.set_score(0)
            return
        Feedback.set_score(1)

    @points(2)
    @name("Edge case: x = 0")
    def test_zero(self):
        user_fn, ref_fn, func_name = self._get_fns()
        user_val = Feedback.call_user(user_fn, 0)
        ref_val = ref_fn(0)
        if user_val != ref_val:
            Feedback.add_feedback(
                f"{func_name}(0) returned {user_val!r}, "
                f"expected {ref_val!r}"
            )
            Feedback.set_score(0)
            return
        Feedback.set_score(1)

    @points(4)
    @name("Positive inputs")
    def test_positive(self):
        user_fn, ref_fn, func_name = self._get_fns()
        fixed = [4, 10, 100]
        rand = [random.randint(1, 50) for _ in range(4)]
        for x in fixed + rand:
            user_val = Feedback.call_user(user_fn, x)
            ref_val = ref_fn(x)
            if user_val != ref_val:
                Feedback.add_feedback(
                    f"{func_name}({x}) returned {user_val!r}, "
                    f"expected {ref_val!r}"
                )
                Feedback.set_score(0)
                return
        Feedback.set_score(1)

    @points(4)
    @name("Negative inputs")
    def test_negative(self):
        user_fn, ref_fn, func_name = self._get_fns()
        fixed = [-1, -7, -10]
        rand = [random.randint(-50, -1) for _ in range(4)]
        for x in fixed + rand:
            user_val = Feedback.call_user(user_fn, x)
            ref_val = ref_fn(x)
            if user_val != ref_val:
                Feedback.add_feedback(
                    f"{func_name}({x}) returned {user_val!r}, "
                    f"expected {ref_val!r}"
                )
                Feedback.set_score(0)
                return
        Feedback.set_score(1)
