from __future__ import annotations


def clamp_cf(value: float) -> float:
    """Clamp certainty factor between -1 and +1."""
    return max(-1.0, min(1.0, value))


def combine_cf(existing_cf: float, new_cf: float) -> float:
    """
    Combine two certainty factors.

    Supports positive and negative evidence.
    Range:
    -1.0 = definitely false
     0.0 = unknown
    +1.0 = definitely true
    """

    existing_cf = clamp_cf(existing_cf)
    new_cf = clamp_cf(new_cf)

    if existing_cf >= 0 and new_cf >= 0:
        combined = existing_cf + new_cf * (1 - existing_cf)

    elif existing_cf <= 0 and new_cf <= 0:
        combined = existing_cf + new_cf * (1 + existing_cf)

    else:
        denominator = 1 - min(abs(existing_cf), abs(new_cf))

        if denominator == 0:
            combined = 0.0
        else:
            combined = (existing_cf + new_cf) / denominator

    return clamp_cf(combined)


def multiply_cf(*values: float) -> float:
    """
    Multiply certainty factors.

    Useful when rule confidence depends on both:
    - certainty of input facts
    - certainty of the rule itself
    """
    result = 1.0

    for value in values:
        result *= clamp_cf(value)

    return clamp_cf(result)