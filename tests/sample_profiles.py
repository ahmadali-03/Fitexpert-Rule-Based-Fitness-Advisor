from __future__ import annotations

from models.user_profile import UserProfile


def get_sample_profiles() -> list[tuple[str, UserProfile]]:
    """
    Multiple test profiles for validating FitExpert.

    Each scenario is designed to test different expert-system reasoning paths:
    - goal selection
    - injury overrides
    - medical caution
    - equipment limitations
    - schedule selection
    - age-based rules
    """

    return [
        (
            "T1: Beginner adult fat-loss user with mild knee issue and dumbbells",
            UserProfile(
                age=22,
                height_cm=170,
                weight_kg=78,
                goal="fat_loss",
                experience_level="beginner",
                available_days=4,
                equipment="home_dumbbells",
                injuries={"knee": "mild"},
                medical_conditions=[],
            ),
        ),
        (
            "T2: Senior flexibility user with no injuries",
            UserProfile(
                age=65,
                height_cm=165,
                weight_kg=68,
                goal="flexibility",
                experience_level="beginner",
                available_days=3,
                equipment="bodyweight_only",
                injuries={},
                medical_conditions=[],
            ),
        ),
        (
            "T3: Advanced adult strength user with full gym and no injuries",
            UserProfile(
                age=30,
                height_cm=180,
                weight_kg=82,
                goal="strength",
                experience_level="advanced",
                available_days=5,
                equipment="full_gym",
                injuries={},
                medical_conditions=[],
            ),
        ),
        (
            "T4: Beginner endurance user with asthma",
            UserProfile(
                age=26,
                height_cm=172,
                weight_kg=70,
                goal="endurance",
                experience_level="beginner",
                available_days=3,
                equipment="full_gym",
                injuries={},
                medical_conditions=["asthma"],
            ),
        ),
        (
            "T5: Intermediate muscle-gain user with shoulder limitation",
            UserProfile(
                age=28,
                height_cm=175,
                weight_kg=74,
                goal="muscle_gain",
                experience_level="intermediate",
                available_days=4,
                equipment="home_dumbbells",
                injuries={"shoulder": "moderate"},
                medical_conditions=[],
            ),
        ),
        (
            "T6: Obese beginner fat-loss user with bodyweight-only setup",
            UserProfile(
                age=35,
                height_cm=168,
                weight_kg=96,
                goal="fat_loss",
                experience_level="beginner",
                available_days=3,
                equipment="bodyweight_only",
                injuries={},
                medical_conditions=[],
            ),
        ),
        (
            "T7: Adult user with severe lower-back issue",
            UserProfile(
                age=40,
                height_cm=176,
                weight_kg=84,
                goal="strength",
                experience_level="intermediate",
                available_days=4,
                equipment="full_gym",
                injuries={"lower_back": "severe"},
                medical_conditions=[],
            ),
        ),
        (
            "T8: Youth beginner bodyweight fitness user",
            UserProfile(
                age=16,
                height_cm=168,
                weight_kg=58,
                goal="strength",
                experience_level="beginner",
                available_days=3,
                equipment="bodyweight_only",
                injuries={},
                medical_conditions=[],
            ),
        ),
    ]