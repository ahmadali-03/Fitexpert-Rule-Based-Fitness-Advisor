from __future__ import annotations

from engine.fact_base import FactBase
from models.user_profile import UserProfile


class ProfileAnalyzer:

    def create_initial_facts(self, profile: UserProfile) -> FactBase:
        profile.validate()

        facts = FactBase()

        bmi = profile.calculate_bmi()

        facts.add_fact(
            name="age",
            value=profile.age,
            certainty=1.0,
            source_rule="USER_INPUT",
            explanation="Age entered by the user.",
        )

        facts.add_fact(
            name="height_cm",
            value=profile.height_cm,
            certainty=1.0,
            source_rule="USER_INPUT",
            explanation="Height entered by the user.",
        )

        facts.add_fact(
            name="weight_kg",
            value=profile.weight_kg,
            certainty=1.0,
            source_rule="USER_INPUT",
            explanation="Weight entered by the user.",
        )

        facts.add_fact(
            name="bmi",
            value=bmi,
            certainty=1.0,
            source_rule="CALCULATED_INPUT",
            explanation="BMI calculated from user height and weight.",
        )

        facts.add_fact(
            name="goal",
            value=profile.goal,
            certainty=1.0,
            source_rule="USER_INPUT",
            explanation="Primary fitness goal selected by the user.",
        )

        facts.add_fact(
            name="experience_level",
            value=profile.experience_level,
            certainty=1.0,
            source_rule="USER_INPUT",
            explanation="Training experience level selected by the user.",
        )

        facts.add_fact(
            name="available_days",
            value=profile.available_days,
            certainty=1.0,
            source_rule="USER_INPUT",
            explanation="Number of days per week the user can train.",
        )

        facts.add_fact(
            name="equipment",
            value=profile.equipment,
            certainty=1.0,
            source_rule="USER_INPUT",
            explanation="Workout location/equipment selected by the user.",
        )

        for injury_name, severity in profile.injuries.items():
            facts.add_fact(
                name=f"injury_{injury_name}",
                value=severity,
                certainty=1.0,
                source_rule="USER_INPUT",
                explanation=f"User reported {severity} {injury_name} injury or limitation.",
            )

        for condition in profile.medical_conditions:
            facts.add_fact(
                name=f"condition_{condition}",
                value=True,
                certainty=1.0,
                source_rule="USER_INPUT",
                explanation=f"User reported medical condition: {condition}.",
            )

        if not profile.injuries:
            facts.add_fact(
                name="injury_none",
                value=True,
                certainty=1.0,
                source_rule="USER_INPUT",
                explanation="User reported no injuries.",
            )

        if not profile.medical_conditions:
            facts.add_fact(
                name="condition_none",
                value=True,
                certainty=1.0,
                source_rule="USER_INPUT",
                explanation="User reported no medical conditions.",
            )

        return facts