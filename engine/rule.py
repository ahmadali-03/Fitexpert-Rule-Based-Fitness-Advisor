from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


Condition = Callable[[Any], bool]
Action = Callable[[Any, Any], Iterable[str] | str | None]


@dataclass
class Rule:
    """rule has
    IF part: conditions
    THEN part: actions
    salience: priority for conflict resolution
    certainty factor: confidence strength of the rule
    explanation: human-readable reason for the rule"""

    rule_id: str
    name: str
    category: str
    salience: int
    conditions: list[Condition]
    actions: list[Action]
    condition_descriptions: list[str]
    action_descriptions: list[str]
    certainty_factor: float = 1.0
    explanation: str = ""

    def is_applicable(self, fact_base: Any) -> bool:

        return all(condition(fact_base) for condition in self.conditions)

    def fire(self, fact_base: Any) -> list[str]:

        changed_facts: list[str] = []

        for action in self.actions:
            result = action(fact_base, self)

            if result is None:
                continue

            if isinstance(result, str):
                changed_facts.append(result)

            else:
                changed_facts.extend(list(result))

        return changed_facts

    @property
    def specificity(self) -> int:

        #More conditions means more specific rule

        return len(self.conditions)