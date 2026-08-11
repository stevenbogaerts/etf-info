# ====================================================================
# Adjust _get_names_from_user as needed for your problem.


def _get_names_from_user() -> list:
    '''
    List each function or variable the student must define in user_code.py.
    - name: must match the identifier in question.html's pl-file-editor and in tests/.
    - description: a brief label shown to students in the variable table.
      This is a short identifier, not a copy of the Effects: docstring.
    - type: typically "python function" or "python variable".
    '''
    return [
        {
            "name": "my_function",
            "description": "BRIEF LABEL for the variable table",
            "type": "python function",
        }
    ]


# ====================================================================
# All other code is boilerplate and probably shouldn't be changed.


def generate(data: dict) -> None:
    data["params"]["names_for_user"] = []
    data["params"]["names_from_user"] = _get_names_from_user()
