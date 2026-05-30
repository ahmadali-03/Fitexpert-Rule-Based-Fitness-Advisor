from __future__ import annotations

from engine.fact_base import FactBase
from knowledge_base.exercises import Exercise, get_exercises_by_category
from models.recommendation import (
    ExerciseRecommendation,
    FitnessRecommendation,
    WorkoutDay,
)


class WorkoutGenerator:
    """
    Converts inferred expert-system facts into a readable workout plan.

    Important:
    This class does not perform expert reasoning.
    It only formats conclusions already inferred by the rule engine.
    """

    def generate(self, fact_base: FactBase, reasoning_summary: str = "") -> FitnessRecommendation:
        program_title = self._get_program_title(fact_base)
        training_split = fact_base.get("training_split", "general_fitness")
        weekly_days = fact_base.get("available_days", 3)

        recommendation = FitnessRecommendation(
            program_title=program_title,
            training_split=training_split,
            weekly_days=weekly_days,
            reasoning_summary=reasoning_summary,
        )

        recommendation.workout_days = self._build_workout_days(fact_base)
        recommendation.safety_notes = self._build_safety_notes(fact_base)
        recommendation.progression_notes = self._build_progression_notes(fact_base)

        return recommendation

    def _get_program_title(self, fact_base: FactBase) -> str:
        final_program_type = fact_base.get("final_program_type", "general_fitness_plan")

        titles = {
            "beginner_4_day_low_impact_fat_loss": "Beginner 4-Day Low-Impact Fat-Loss Plan",
            "beginner_strength_foundation": "Beginner Strength Foundation Plan",
            "dumbbell_upper_lower_hypertrophy": "Dumbbell Upper/Lower Muscle-Gain Plan",
            "medical_clearance_required_before_plan": "Medical Clearance Required Before Training Plan",
            "general_fitness_plan": "General Fitness Plan",
        }

        return titles.get(final_program_type, "Personalized FitExpert Workout Plan")

    def _build_workout_days(self, fact_base: FactBase) -> list[WorkoutDay]:
        training_split = fact_base.get("training_split", "three_day_full_body")

        if fact_base.get("medical_clearance_required") is True:
            return [
                WorkoutDay(
                    day_name="Safety First",
                    focus="Medical clearance required before normal training",
                    exercises=[],
                )
            ]

        if training_split == "upper_lower":
            return self._build_upper_lower_plan(fact_base)

        if training_split in {"full_body", "three_day_full_body"}:
            return self._build_full_body_plan(fact_base)

        if training_split == "push_pull_legs":
            return self._build_push_pull_legs_plan(fact_base)

        return self._build_full_body_plan(fact_base)

    def _build_upper_lower_plan(self, fact_base: FactBase) -> list[WorkoutDay]:
        return [
            WorkoutDay(
                day_name="Day 1",
                focus="Upper Body A",
                exercises=self._select_exercises_for_focus(fact_base, "upper"),
            ),
            WorkoutDay(
                day_name="Day 2",
                focus="Lower Body A + Low-Impact Cardio",
                exercises=self._select_exercises_for_focus(fact_base, "lower"),
            ),
            WorkoutDay(
                day_name="Day 3",
                focus="Upper Body B",
                exercises=self._select_exercises_for_focus(fact_base, "upper"),
            ),
            WorkoutDay(
                day_name="Day 4",
                focus="Lower Body B + Core",
                exercises=self._select_exercises_for_focus(fact_base, "lower"),
            ),
        ]

    def _build_full_body_plan(self, fact_base: FactBase) -> list[WorkoutDay]:
        days = min(int(fact_base.get("available_days", 3)), 3)

        workout_days: list[WorkoutDay] = []

        for index in range(days):
            workout_days.append(
                WorkoutDay(
                    day_name=f"Day {index + 1}",
                    focus="Full Body",
                    exercises=self._select_exercises_for_focus(fact_base, "full_body"),
                )
            )

        return workout_days

    def _build_push_pull_legs_plan(self, fact_base: FactBase) -> list[WorkoutDay]:
        return [
            WorkoutDay(
                day_name="Day 1",
                focus="Push",
                exercises=self._select_exercises_for_focus(fact_base, "push"),
            ),
            WorkoutDay(
                day_name="Day 2",
                focus="Pull",
                exercises=self._select_exercises_for_focus(fact_base, "pull"),
            ),
            WorkoutDay(
                day_name="Day 3",
                focus="Legs",
                exercises=self._select_exercises_for_focus(fact_base, "lower"),
            ),
            WorkoutDay(
                day_name="Day 4",
                focus="Push",
                exercises=self._select_exercises_for_focus(fact_base, "push"),
            ),
            WorkoutDay(
                day_name="Day 5",
                focus="Pull",
                exercises=self._select_exercises_for_focus(fact_base, "pull"),
            ),
            WorkoutDay(
                day_name="Day 6",
                focus="Legs + Core",
                exercises=self._select_exercises_for_focus(fact_base, "lower"),
            ),
        ]

    def _select_exercises_for_focus(
        self,
        fact_base: FactBase,
        focus: str,
    ) -> list[ExerciseRecommendation]:
        equipment = fact_base.get("equipment", "bodyweight_only")
        forbidden_flags = self._get_forbidden_flags(fact_base)
        preferred_tags = self._get_preferred_tags(fact_base)

        selected: list[Exercise] = []

        if focus == "upper":
            selected.extend(
                get_exercises_by_category(
                    "upper_push",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=2,
                )
            )
            selected.extend(
                get_exercises_by_category(
                    "upper_pull",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=2,
                )
            )

        elif focus == "lower":
            selected.extend(
                get_exercises_by_category(
                    "lower_body",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=3,
                )
            )
            selected.extend(
                get_exercises_by_category(
                    "core",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=1,
                )
            )
            selected.extend(
                get_exercises_by_category(
                    "cardio",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=1,
                )
            )

        elif focus == "push":
            selected.extend(
                get_exercises_by_category(
                    "upper_push",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=4,
                )
            )

        elif focus == "pull":
            selected.extend(
                get_exercises_by_category(
                    "upper_pull",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=4,
                )
            )

        else:
            selected.extend(
                get_exercises_by_category(
                    "upper_push",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=1,
                )
            )
            selected.extend(
                get_exercises_by_category(
                    "upper_pull",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=1,
                )
            )
            selected.extend(
                get_exercises_by_category(
                    "lower_body",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=2,
                )
            )
            selected.extend(
                get_exercises_by_category(
                    "core",
                    equipment,
                    forbidden_flags,
                    preferred_tags,
                    limit=1,
                )
            )

        return [self._to_recommendation(exercise, fact_base) for exercise in selected]

    def _to_recommendation(
        self,
        exercise: Exercise,
        fact_base: FactBase,
    ) -> ExerciseRecommendation:
        sets = self._get_sets(fact_base)
        reps = self._get_reps(fact_base)

        if exercise.category == "cardio":
            sets = 1
            reps = fact_base.get("cardio_duration", "15_to_25_minutes")

            if fact_base.get("conditioning_style") == "low_impact_fat_loss":
                reps = "15_to_30_minutes"

        if exercise.category == "core":
            reps = "20_to_40_seconds_or_8_to_12_controlled_reps"

        return ExerciseRecommendation(
            name=exercise.name,
            category=exercise.category,
            sets=sets,
            reps=reps,
            notes=exercise.notes,
            certainty=self._estimate_exercise_certainty(exercise, fact_base),
        )

    def _get_sets(self, fact_base: FactBase) -> int:
        set_scheme = fact_base.get("set_scheme", "2_to_3_sets_per_exercise")

        if set_scheme == "4_to_5_sets_per_main_exercise":
            return 4

        if set_scheme == "3_to_4_sets_per_exercise":
            return 3

        return 2

    def _get_reps(self, fact_base: FactBase) -> str:
        rep_range = fact_base.get("rep_range", "8_to_12_reps")

        readable = {
            "3_to_6_reps": "3–6 reps",
            "8_to_12_reps": "8–12 reps",
            "10_to_15_reps": "10–15 reps",
        }

        return readable.get(rep_range, "8–12 reps")

    def _get_forbidden_flags(self, fact_base: FactBase) -> set[str]:
        flags: set[str] = set()

        possible_flags = {
            "avoid_high_impact",
            "avoid_deep_knee_flexion",
            "avoid_loaded_hinges",
            "avoid_heavy_spinal_loading",
            "avoid_overhead_pressing",
            "avoid_upright_rows",
        }

        for flag in possible_flags:
            if fact_base.get(flag) is True:
                flags.add(flag)

        return flags

    def _get_preferred_tags(self, fact_base: FactBase) -> set[str]:
        tags: set[str] = set()

        if fact_base.get("experience_level") == "beginner":
            tags.add("beginner_friendly")

        if fact_base.get("needs_knee_safe_training") is True:
            tags.add("knee_safe")
            tags.add("low_impact")

        if fact_base.get("back_risk_level") == "present":
            tags.add("back_friendly")
            tags.add("back_safe")

        if fact_base.get("shoulder_risk_level") == "present":
            tags.add("shoulder_friendly")
            tags.add("scapular_control")

        return tags

    def _estimate_exercise_certainty(
        self,
        exercise: Exercise,
        fact_base: FactBase,
    ) -> float:
        certainty = 0.75

        preferred_tags = self._get_preferred_tags(fact_base)

        if exercise.tags.intersection(preferred_tags):
            certainty += 0.15

        if fact_base.get("exercise_selection_style") == "dumbbell_based":
            if "home_dumbbells" in exercise.equipment_options:
                certainty += 0.1

        if exercise.category == "cardio" and fact_base.get("avoid_high_impact") is True:
            if "low_impact" in exercise.tags:
                certainty += 0.1

        return min(round(certainty, 2), 1.0)

    def _build_safety_notes(self, fact_base: FactBase) -> list[str]:
        notes: list[str] = []

        if fact_base.get("medical_clearance_required") is True:
            notes.append(
                "Medical clearance is required before following a normal training plan."
            )

        if fact_base.get("needs_knee_safe_training") is True:
            notes.append(
                "Knee-safe training selected: avoid jumping, sprinting, and painful deep knee bending."
            )

        if fact_base.get("avoid_heavy_spinal_loading") is True:
            notes.append(
                "Back-safe training selected: avoid heavy spinal loading and aggressive loaded hinges."
            )

        if fact_base.get("avoid_overhead_pressing") is True:
            notes.append(
                "Shoulder-safe training selected: avoid painful overhead pressing."
            )

        if fact_base.get("cardio_caution_required") is True:
            notes.append(
                "Cardio caution selected: use longer warm-up and controlled low-to-moderate intensity."
            )

        if not notes:
            notes.append("No major injury or medical restriction was inferred.")

        return notes

    def _build_progression_notes(self, fact_base: FactBase) -> list[str]:
        notes: list[str] = []

        if fact_base.get("experience_level") == "beginner":
            notes.append(
                "Start with easy-to-moderate effort and increase reps before increasing load."
            )

        if fact_base.get("training_volume") == "low":
            notes.append(
                "Use 2 sets initially; move to 3 sets when recovery and technique are consistent."
            )

        if fact_base.get("goal_direction") == "fat_loss_focused":
            notes.append(
                "Keep resistance training consistent and add low-impact cardio gradually."
            )

        if fact_base.get("goal_direction") == "strength_focused":
            notes.append(
                "Increase weight slowly only when form remains stable."
            )

        if fact_base.get("goal_direction") == "mobility_focused":
            notes.append(
                "Practice mobility frequently with gentle, pain-free range of motion."
            )

        return notes