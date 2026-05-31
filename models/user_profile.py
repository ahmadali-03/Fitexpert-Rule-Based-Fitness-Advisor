from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UserProfile:

    age: int
    height_cm: float
    weight_kg: float

    goal: str
    experience_level: str
    available_days: int
    equipment: str

    injuries: dict[str, str] = field(default_factory=dict)
    medical_conditions: list[str] = field(default_factory=list)

    def calculate_bmi(self) -> float:
        height_m = self.height_cm / 100

        if height_m <= 0:
            raise ValueError("Height must be greater than zero.")

        return round(self.weight_kg / (height_m ** 2), 2)

    def validate(self) -> None:

        valid_goals = {
            "strength",
            "muscle_gain",
            "fat_loss",
            "endurance",
            "flexibility",
        }

        valid_experience_levels = {
            "beginner",
            "intermediate",
            "advanced",
        }

        valid_equipment = {
            "full_gym",
            "home_dumbbells",
            "bodyweight_only",
        }

        if self.age <= 0:
            raise ValueError("Age must be greater than zero.")

        if self.height_cm <= 0:
            raise ValueError("Height must be greater than zero.")

        if self.weight_kg <= 0:
            raise ValueError("Weight must be greater than zero.")

        if self.goal not in valid_goals:
            raise ValueError(f"Invalid goal: {self.goal}")

        if self.experience_level not in valid_experience_levels:
            raise ValueError(f"Invalid experience level: {self.experience_level}")

        if self.available_days < 1 or self.available_days > 7:
            raise ValueError("Available training days must be between 1 and 7.")

        if self.equipment not in valid_equipment:
            raise ValueError(f"Invalid equipment option: {self.equipment}")