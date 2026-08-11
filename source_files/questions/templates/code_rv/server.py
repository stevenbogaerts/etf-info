from pl_random import PLRandom


# ====================================================================
# Adjust _get_names_from_user and _get_raw_parameters for your problem.


def _get_names_from_user(raw: dict) -> list:
    '''
    List each function or variable the student must define in user_code.py.
    - name: must match the identifier in question.html's pl-file-editor and in tests/.
    - description: a brief label shown to students in the variable table.
      This is a short identifier, not a copy of the Effects: docstring.
    - type: typically "python function" or "python variable".
    raw contains the values from _get_raw_parameters, so names can be
    derived from variant parameters (e.g. f"multiply_by_{raw['n']}").
    '''
    return [
        {
            "name": f"multiply_by_{raw['n']}",
            "description": "BRIEF LABEL for the variable table",
            "type": "python function",
        }
    ]


def _get_raw_parameters(plr: PLRandom) -> dict:
    '''
    Generate and return the random variant parameters.
    Use plr for randomization. Return a dict mapping key to value.
    Values are stored in data["params"] and available in question.html
    as {{ params.key }}, and in the grader via self.data["params"]["key"].
    '''
    return {
        "n": plr.integer(2, 9),
    }


# ====================================================================
# All other code is boilerplate and probably shouldn't be changed.


def generate(data: dict) -> None:
    plr = PLRandom(data["variant_seed"])
    raw = _get_raw_parameters(plr)

    # Store variant parameters for use in question.html and the grader
    for key, value in raw.items():
        data["params"][key] = value

    # Pre-compute derived display values for the question text
    data["params"]["func_name"] = f"multiply_by_{raw['n']}"
    data["params"]["example_input"] = 3
    data["params"]["example_output"] = 3 * raw["n"]

    data["params"]["names_for_user"] = []
    data["params"]["names_from_user"] = _get_names_from_user(raw)
