from __future__ import annotations

from engine.rule import Rule


class ConflictResolver:
    """Strategy
    Higher salience fires first
    More specific rule fires first
    Higher certainty factor fires first
    Rule ID alphabetical order as final stable tie-breaker"""

    def sort_agenda(self, agenda: list[Rule]) -> list[Rule]:
        return sorted(
            agenda,
            key=lambda rule: (
                -rule.salience,
                -rule.specificity,
                -rule.certainty_factor,
                rule.rule_id,
            ),
        )

    def select_next_rule(self, agenda: list[Rule]) -> Rule | None:
        sorted_agenda = self.sort_agenda(agenda)
        return sorted_agenda[0] if sorted_agenda else None