import numpy as np
from faker import Faker


class PLRandom:
    """
    A utility class for generating random values in PrairieLearn questions.
    Wraps numpy's random generator and Faker for rich random content.
    """

    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)
        self.fake = Faker()
        Faker.seed(seed)

    # ------------------------------------------------------------------ #
    #  Core numeric                                                        #
    # ------------------------------------------------------------------ #

    def num(
        self, low=0.0, high=1.0, digits_after=None
    ) -> float | int:
        """
        Random float in [low, high).
        - digits_after:  round to this many decimal places
        Returns a float unless digits_after=0, in which case returns int.
        """
        value = self.rng.uniform(low, high)
        if digits_after is not None:
            value = round(value, digits_after)
            if digits_after == 0:
                return int(value)
        return float(value)

    def integer(self, low=0, high=100) -> int:
        """Random integer in [low, high] (inclusive)."""
        return int(self.rng.integers(low, high + 1))

    # ------------------------------------------------------------------ #
    #  Choices & lists                                                     #
    # ------------------------------------------------------------------ #

    def choice(self, items, exclude=None) -> object:
        """Pick one item from a list, optionally excluding certain values."""
        pool = [x for x in items if exclude is None or x not in exclude]
        if not pool:
            raise ValueError("No items left after exclusions.")
        return pool[int(self.rng.integers(0, len(pool)))]

    def choices(self, items, k=2, replace=False, exclude=None) -> list:
        """Pick k items from a list."""
        pool = [x for x in items if exclude is None or x not in exclude]
        if not replace and k > len(pool):
            raise ValueError("Not enough items to sample without replacement.")
        idx = self.rng.choice(len(pool), size=k, replace=replace)
        return [pool[i] for i in idx]

    def shuffle(self, items) -> list:
        """Return a shuffled copy of items"""
        arr = list(items)
        perm = self.rng.permutation(len(arr))
        shuffled = [arr[i] for i in perm]
        return shuffled

    # ------------------------------------------------------------------ #
    #  Misc                                                                #
    # ------------------------------------------------------------------ #

    def percent(self, low=0.0, high=100.0, digits_after=1):
        """Random percentage value."""
        return round(self.rng.uniform(low, high), digits_after)

    def bool(self, p_true=0.5):
        """Random boolean with given probability of True."""
        return bool(self.rng.random() < p_true)

    def __repr__(self):
        return f"PLRandom(rng={self.rng}, fake={self.fake})"

    '''
    By accessing the Faker attribute, other random data can be generated, 
    such as:

    fake.name()

    fake.user_name()
    fake.password()
    fake.email()
    fake.address()
    fake.city()
    fake.state()
    fake.country()
    fake.postcode()
    fake.date_of_birth()

    fake.credit_card_number()
    fake.credit_card_expire()

    fake.company()
    fake.job()

    fake.date_this_year()
    fake.date_between(start_date='-1y', end_date='today')
    fake.time()

    fake.word()
    fake.sentence()
    fake.paragraph()

    fake.latitude()
    fake.longitude()
    fake.uuid4()
    '''
