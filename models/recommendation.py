from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ExerciseRecommendation:
    """
    Represents one recommended exercise.
    """

    name: str
    category: str
    sets: int
    reps: str
    notes: str = ""
    certainty: float = 1.0


@dataclass
class WorkoutDay:
    """
    Represents one day in the workout plan.
    """

    day_name: str
    focus: str
    exercises: list[ExerciseRecommendation] = field(default_factory=list)


@dataclass
class FitnessRecommendation:
    """
    Final output object produced after inference.
    """

    program_title: str
    training_split: str
    weekly_days: int
    workout_days: list[WorkoutDay] = field(default_factory=list)
    safety_notes: list[str] = field(default_factory=list)
    progression_notes: list[str] = field(default_factory=list)
    reasoning_summary: str = ""