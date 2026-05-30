from __future__ import annotations

import json
from pathlib import Path

from engine.rule import Rule
from knowledge_base.rules import get_rules


class RuleExporter:
    """
    Exports the Python knowledge base into human-readable documentation files.

    The system uses rules.py as the executable knowledge base.
    JSON and Markdown exports are for documentation, viva, and report purposes.
    """

    def __init__(
        self,
        json_path: str = "knowledge_base/rule_catalog.json",
        markdown_path: str = "docs/rule_table.md",
    ) -> None:
        self.json_path = Path(json_path)
        self.markdown_path = Path(markdown_path)

    def export_all(self) -> None:
        rules = get_rules()

        self._ensure_parent_directories()
        self.export_json(rules)
        self.export_markdown(rules)

        print("Rule export completed.")
        print(f"Total rules exported: {len(rules)}")
        print(f"JSON file: {self.json_path}")
        print(f"Markdown file: {self.markdown_path}")

    def _ensure_parent_directories(self) -> None:
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        self.markdown_path.parent.mkdir(parents=True, exist_ok=True)

    def export_json(self, rules: list[Rule]) -> None:
        data = []

        for rule in rules:
            data.append(
                {
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "category": rule.category,
                    "salience": rule.salience,
                    "certainty_factor": rule.certainty_factor,
                    "conditions": rule.condition_descriptions,
                    "actions": rule.action_descriptions,
                    "explanation": rule.explanation,
                }
            )

        with self.json_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def export_markdown(self, rules: list[Rule]) -> None:
        lines: list[str] = []

        lines.append("# FitExpert Rule Table")
        lines.append("")
        lines.append(f"Total Rules: **{len(rules)}**")
        lines.append("")
        lines.append(
            "This table documents the executable Python knowledge base used by FitExpert."
        )
        lines.append(
            "The JSON and Markdown versions are generated from `knowledge_base/rules.py` for documentation and viva explanation."
        )
        lines.append("")

        grouped_rules = self._group_rules_by_category(rules)

        for category, category_rules in grouped_rules.items():
            lines.append(f"## {category}")
            lines.append("")
            lines.append(
                "| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |"
            )
            lines.append(
                "|---|---|---:|---:|---|---|---|"
            )

            for rule in category_rules:
                conditions = "<br>".join(rule.condition_descriptions)
                actions = "<br>".join(rule.action_descriptions)
                explanation = rule.explanation.replace("\n", " ")

                lines.append(
                    f"| {rule.rule_id} "
                    f"| {rule.name} "
                    f"| {rule.salience} "
                    f"| {rule.certainty_factor} "
                    f"| {conditions} "
                    f"| {actions} "
                    f"| {explanation} |"
                )

            lines.append("")

        with self.markdown_path.open("w", encoding="utf-8") as file:
            file.write("\n".join(lines))

    def _group_rules_by_category(self, rules: list[Rule]) -> dict[str, list[Rule]]:
        grouped: dict[str, list[Rule]] = {}

        for rule in rules:
            grouped.setdefault(rule.category, []).append(rule)

        return grouped