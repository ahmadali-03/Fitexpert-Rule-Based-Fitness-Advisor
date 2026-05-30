from __future__ import annotations

from engine.conflict_resolver import ConflictResolver
from engine.explanation import ExplanationTrace
from engine.fact_base import FactBase
from engine.rule import Rule


class InferenceEngine:
    """
    Custom forward-chaining inference engine.

    Process:
    1. Match rules against current facts.
    2. Add matching rules to agenda.
    3. Resolve conflicts using salience/specificity/certainty.
    4. Fire selected rule.
    5. Add derived facts to working memory.
    6. Repeat until no more rules can fire.
    """

    def __init__(
        self,
        rules: list[Rule],
        conflict_resolver: ConflictResolver | None = None,
        max_cycles: int = 200,
    ) -> None:
        self.rules = rules
        self.conflict_resolver = conflict_resolver or ConflictResolver()
        self.max_cycles = max_cycles
        self.explanation_trace = ExplanationTrace()
        self.fired_rule_ids: set[str] = set()

    def reset(self) -> None:
        self.explanation_trace = ExplanationTrace()
        self.fired_rule_ids = set()

    def build_agenda(self, fact_base: FactBase) -> list[Rule]:
        agenda: list[Rule] = []

        for rule in self.rules:
            if rule.rule_id in self.fired_rule_ids:
                continue

            if rule.is_applicable(fact_base):
                agenda.append(rule)

        return agenda

    def run(self, fact_base: FactBase) -> tuple[FactBase, ExplanationTrace]:
        cycle = 0

        while cycle < self.max_cycles:
            cycle += 1

            agenda = self.build_agenda(fact_base)

            if not agenda:
                break

            selected_rule = self.conflict_resolver.select_next_rule(agenda)

            if selected_rule is None:
                break

            changed_facts = selected_rule.fire(fact_base)

            self.fired_rule_ids.add(selected_rule.rule_id)
            self.explanation_trace.record_rule_fire(selected_rule, changed_facts)

        return fact_base, self.explanation_trace