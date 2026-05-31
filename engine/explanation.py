from __future__ import annotations

from dataclasses import dataclass

from engine.rule import Rule


@dataclass
class RuleTrace:

    rule_id: str
    rule_name: str
    category: str
    salience: int
    certainty_factor: float
    conditions: list[str]
    actions: list[str]
    created_facts: list[str]
    explanation: str


class ExplanationTrace:

    def __init__(self) -> None:
        self.fired_rules: list[RuleTrace] = []

    def record_rule_fire(self, rule: Rule, created_facts: list[str]) -> None:
        trace = RuleTrace(
            rule_id=rule.rule_id,
            rule_name=rule.name,
            category=rule.category,
            salience=rule.salience,
            certainty_factor=rule.certainty_factor,
            conditions=rule.condition_descriptions,
            actions=rule.action_descriptions,
            created_facts=created_facts,
            explanation=rule.explanation,
        )

        self.fired_rules.append(trace)

    def get_fired_rule_ids(self) -> list[str]:
        return [trace.rule_id for trace in self.fired_rules]

    def format_reasoning_chain(self) -> str:
        if not self.fired_rules:
            return "No rules fired."

        lines: list[str] = []

        for index, trace in enumerate(self.fired_rules, start=1):
            lines.append(f"{index}. Rule {trace.rule_id}: {trace.rule_name}")
            lines.append(f"   Category: {trace.category}")
            lines.append(f"   Priority/Salience: {trace.salience}")
            lines.append(f"   Certainty Factor: {trace.certainty_factor}")
            lines.append("   IF:")
            for condition in trace.conditions:
                lines.append(f"      - {condition}")

            lines.append("   THEN:")
            for action in trace.actions:
                lines.append(f"      - {action}")

            if trace.created_facts:
                lines.append(f"   Created/Updated Facts: {', '.join(trace.created_facts)}")

            lines.append(f"   Explanation: {trace.explanation}")
            lines.append("")

        return "\n".join(lines)