from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Fact:
    """
    Represents one fact in working memory.
    """

    name: str
    value: Any
    certainty: float = 1.0
    source_rule: str = "USER_INPUT"
    explanation: str = ""


class FactBase:
    """
    Working memory of the expert system.

    Stores:
    - initial user facts
    - derived facts created by fired rules
    """

    def __init__(self) -> None:
        self._facts: dict[str, Fact] = {}
        self.history: list[str] = []

    def add_fact(
        self,
        name: str,
        value: Any,
        certainty: float = 1.0,
        source_rule: str = "UNKNOWN",
        explanation: str = "",
    ) -> bool:
        """
        Add or update a fact.

        Returns True if the fact was newly added or meaningfully updated.
        """
        certainty = max(-1.0, min(1.0, certainty))

        existing_fact = self._facts.get(name)

        if existing_fact is None:
            self._facts[name] = Fact(
                name=name,
                value=value,
                certainty=certainty,
                source_rule=source_rule,
                explanation=explanation,
            )
            self.history.append(f"ADDED: {name} = {value} CF={certainty}")
            return True

        # If same value exists but new certainty is stronger, update it.
        if existing_fact.value == value and certainty > existing_fact.certainty:
            existing_fact.certainty = certainty
            existing_fact.source_rule = source_rule
            existing_fact.explanation = explanation
            self.history.append(f"UPDATED CF: {name} = {value} CF={certainty}")
            return True

        # If different value appears with stronger certainty, replace it.
        if existing_fact.value != value and certainty > existing_fact.certainty:
            old_value = existing_fact.value
            existing_fact.value = value
            existing_fact.certainty = certainty
            existing_fact.source_rule = source_rule
            existing_fact.explanation = explanation
            self.history.append(
                f"REPLACED: {name}: {old_value} -> {value} CF={certainty}"
            )
            return True

        return False

    def get(self, name: str, default: Any = None) -> Any:
        fact = self._facts.get(name)
        return fact.value if fact else default

    def get_certainty(self, name: str) -> float:
        fact = self._facts.get(name)
        return fact.certainty if fact else 0.0

    def has(self, name: str) -> bool:
        return name in self._facts

    def matches(self, name: str, value: Any) -> bool:
        return self.get(name) == value

    def all_facts(self) -> list[Fact]:
        return list(self._facts.values())

    def to_dict(self) -> dict[str, Any]:
        return {name: fact.value for name, fact in self._facts.items()}

    def explain_fact(self, name: str) -> str:
        fact = self._facts.get(name)

        if fact is None:
            return f"No fact named '{name}' exists in working memory."

        return (
            f"{fact.name} = {fact.value} "
            f"(CF={fact.certainty}, source={fact.source_rule})\n"
            f"Explanation: {fact.explanation}"
        )