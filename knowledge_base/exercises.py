from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Exercise:
    """
    Represents one exercise option in the exercise knowledge base.
    """

    name: str
    category: str
    equipment_options: set[str]
    tags: set[str] = field(default_factory=set)
    contraindications: set[str] = field(default_factory=set)
    notes: str = ""


EXERCISE_DATABASE: list[Exercise] = [
    # ============================================================
    # UPPER BODY PUSH
    # ============================================================

    Exercise(
        name="Dumbbell Floor Press",
        category="upper_push",
        equipment_options={"home_dumbbells", "full_gym"},
        tags={"beginner_friendly", "shoulder_friendly"},
        notes="Good pressing option with limited shoulder range.",
    ),
    Exercise(
        name="Incline Push-up",
        category="upper_push",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"beginner_friendly", "bodyweight"},
        notes="Use a bench, table, or wall to reduce difficulty.",
    ),
    Exercise(
        name="Push-up",
        category="upper_push",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"bodyweight"},
        notes="Keep body straight and control the lowering phase.",
    ),
    Exercise(
        name="Dumbbell Shoulder Press",
        category="upper_push",
        equipment_options={"home_dumbbells", "full_gym"},
        tags={"overhead"},
        contraindications={"avoid_overhead_pressing"},
        notes="Avoid if shoulder pain is present.",
    ),
    Exercise(
        name="Machine Chest Press",
        category="upper_push",
        equipment_options={"full_gym"},
        tags={"machine", "beginner_friendly"},
        notes="Stable pressing option for gym users.",
    ),

    # ============================================================
    # UPPER BODY PULL
    # ============================================================

    Exercise(
        name="One-arm Dumbbell Row",
        category="upper_pull",
        equipment_options={"home_dumbbells", "full_gym"},
        tags={"beginner_friendly", "back"},
        notes="Support one hand on a bench or chair.",
    ),
    Exercise(
        name="Chest-supported Dumbbell Row",
        category="upper_pull",
        equipment_options={"home_dumbbells", "full_gym"},
        tags={"back_safe", "beginner_friendly"},
        notes="Reduces lower-back stress compared with unsupported rows.",
    ),
    Exercise(
        name="Lat Pulldown",
        category="upper_pull",
        equipment_options={"full_gym"},
        tags={"machine", "back"},
        notes="Use controlled motion and avoid leaning too far back.",
    ),
    Exercise(
        name="Seated Cable Row",
        category="upper_pull",
        equipment_options={"full_gym"},
        tags={"machine", "back"},
        notes="Keep torso stable and pull elbows back.",
    ),
    Exercise(
        name="Prone Y-T-W Raises",
        category="upper_pull",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"shoulder_friendly", "scapular_control"},
        notes="Use light/no weight and focus on control.",
    ),

    # ============================================================
    # LOWER BODY
    # ============================================================

    Exercise(
        name="Glute Bridge",
        category="lower_body",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"knee_safe", "back_friendly", "beginner_friendly"},
        notes="Squeeze glutes at the top and avoid arching the lower back.",
    ),
    Exercise(
        name="Box Squat to Chair",
        category="lower_body",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"knee_safe", "beginner_friendly"},
        notes="Sit back to a chair/box and keep range pain-free.",
    ),
    Exercise(
        name="Supported Step-up",
        category="lower_body",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"knee_safe"},
        notes="Use a low step and hold support if needed.",
    ),
    Exercise(
        name="Dumbbell Romanian Deadlift",
        category="lower_body",
        equipment_options={"home_dumbbells", "full_gym"},
        tags={"hinge", "posterior_chain"},
        contraindications={"avoid_loaded_hinges", "avoid_heavy_spinal_loading"},
        notes="Keep back neutral and use light/moderate dumbbells.",
    ),
    Exercise(
        name="Goblet Squat",
        category="lower_body",
        equipment_options={"home_dumbbells", "full_gym"},
        tags={"squat"},
        contraindications={"avoid_deep_knee_flexion"},
        notes="Use comfortable depth only.",
    ),
    Exercise(
        name="Leg Press",
        category="lower_body",
        equipment_options={"full_gym"},
        tags={"machine"},
        contraindications={"avoid_deep_knee_flexion"},
        notes="Keep range controlled and avoid locking knees.",
    ),

    # ============================================================
    # CORE
    # ============================================================

    Exercise(
        name="Dead Bug",
        category="core",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"back_friendly", "beginner_friendly"},
        notes="Keep lower back gently pressed toward the floor.",
    ),
    Exercise(
        name="Bird Dog",
        category="core",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"back_friendly", "beginner_friendly"},
        notes="Move slowly and avoid rotating the hips.",
    ),
    Exercise(
        name="Front Plank",
        category="core",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"anti_extension"},
        notes="Stop if lower-back discomfort appears.",
    ),
    Exercise(
        name="Side Plank",
        category="core",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"anti_rotation"},
        notes="Keep hips stacked and body straight.",
    ),

    # ============================================================
    # CARDIO
    # ============================================================

    Exercise(
        name="Brisk Walking",
        category="cardio",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"low_impact", "knee_safe", "beginner_friendly"},
        notes="Use a pace where conversation is possible but slightly challenging.",
    ),
    Exercise(
        name="Stationary Cycling",
        category="cardio",
        equipment_options={"full_gym"},
        tags={"low_impact", "knee_safe"},
        notes="Use low-to-moderate resistance and smooth cadence.",
    ),
    Exercise(
        name="Elliptical",
        category="cardio",
        equipment_options={"full_gym"},
        tags={"low_impact", "knee_safe"},
        notes="Good low-impact cardio option if available.",
    ),
    Exercise(
        name="Jump Rope",
        category="cardio",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"high_impact"},
        contraindications={"avoid_high_impact"},
        notes="Avoid if knee pain or high-impact restriction exists.",
    ),
    Exercise(
        name="Low-impact Marching Intervals",
        category="cardio",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"low_impact", "beginner_friendly"},
        notes="March in place with controlled effort.",
    ),

    # ============================================================
    # MOBILITY
    # ============================================================

    Exercise(
        name="Cat-Cow Mobility",
        category="mobility",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"spine_mobility", "beginner_friendly"},
        notes="Move gently through comfortable range.",
    ),
    Exercise(
        name="Hip Flexor Stretch",
        category="mobility",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"lower_body_mobility"},
        notes="Keep torso tall and avoid forcing range.",
    ),
    Exercise(
        name="Wall Slides",
        category="mobility",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"shoulder_mobility"},
        notes="Move slowly and stay pain-free.",
    ),
    Exercise(
        name="Hamstring Stretch",
        category="mobility",
        equipment_options={"bodyweight_only", "home_dumbbells", "full_gym"},
        tags={"lower_body_mobility"},
        notes="Use a mild stretch, not pain.",
    ),
]


def get_exercises_by_category(
    category: str,
    equipment: str,
    forbidden_flags: set[str] | None = None,
    preferred_tags: set[str] | None = None,
    limit: int = 4,
) -> list[Exercise]:
    """
    Select exercises by category, equipment, and safety restrictions.
    """

    forbidden_flags = forbidden_flags or set()
    preferred_tags = preferred_tags or set()

    candidates: list[Exercise] = []

    for exercise in EXERCISE_DATABASE:
        if exercise.category != category:
            continue

        if equipment not in exercise.equipment_options:
            continue

        if exercise.contraindications.intersection(forbidden_flags):
            continue

        candidates.append(exercise)

    # Prefer exercises with matching tags.
    candidates.sort(
        key=lambda exercise: len(exercise.tags.intersection(preferred_tags)),
        reverse=True,
    )

    return candidates[:limit]