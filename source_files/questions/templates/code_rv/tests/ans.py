# n is defined in setup_code.py, which runs before this file.
# The reference answer has unrestricted access to all setup_code variables.

def _impl(x: int) -> int:
    return x * n  # noqa: F821


globals()[f'multiply_by_{n}'] = _impl  # noqa: F821
