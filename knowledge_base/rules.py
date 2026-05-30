from __future__ import annotations

from typing import Any, Callable

from engine.fact_base import FactBase
from engine.rule import Rule
from knowledge_base.rule_categories import (
    CATEGORY_AGE_CLASSIFICATION,
    CATEGORY_BMI_CLASSIFICATION,
    CATEGORY_EQUIPMENT_ANALYSIS,
    CATEGORY_EXPERIENCE_ANALYSIS,
    CATEGORY_GOAL_ANALYSIS,
    CATEGORY_INJURY_SAFETY,
    CATEGORY_MEDICAL_SAFETY,
    CATEGORY_PROGRAM_DIRECTION,
    CATEGORY_SCHEDULE_ANALYSIS,
    SALIENCE,
)


def has_fact(name: str) -> Callable[[FactBase], bool]:
    return lambda facts: facts.has(name)


def fact_equals(name: str, value: Any) -> Callable[[FactBase], bool]:
    return lambda facts: facts.matches(name, value)


def fact_in(name: str, values: set[Any]) -> Callable[[FactBase], bool]:
    return lambda facts: facts.get(name) in values


def fact_less_than(name: str, value: float) -> Callable[[FactBase], bool]:
    return lambda facts: facts.has(name) and facts.get(name) < value


def fact_between(name: str, low: float, high: float) -> Callable[[FactBase], bool]:
    return lambda facts: facts.has(name) and low <= facts.get(name) < high


def fact_greater_equal(name: str, value: float) -> Callable[[FactBase], bool]:
    return lambda facts: facts.has(name) and facts.get(name) >= value


def add_fact_action(
    name: str,
    value: Any,
    certainty: float = 1.0,
    explanation: str = "",
):
    """
    Creates a rule action that adds a derived fact to working memory.
    """

    def action(fact_base: FactBase, rule: Rule):
        was_changed = fact_base.add_fact(
            name=name,
            value=value,
            certainty=certainty * rule.certainty_factor,
            source_rule=rule.rule_id,
            explanation=explanation or rule.explanation,
        )

        return [name] if was_changed else []

    return action


def get_rules() -> list[Rule]:
    """
    Returns the FitExpert knowledge base.

    Batch 1 currently contains 45 meaningful rules.
    More rules will be added in later batches until the project reaches 90-100 rules.
    """

    rules: list[Rule] = [

        # ============================================================
        # AGE CLASSIFICATION RULES
        # ============================================================

        Rule(
            rule_id="R-AGE-001",
            name="Classify youth user",
            category=CATEGORY_AGE_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                has_fact("age"),
                fact_less_than("age", 18),
            ],
            actions=[
                add_fact_action(
                    "age_group",
                    "youth",
                    1.0,
                    "User is below 18 years old.",
                )
            ],
            condition_descriptions=[
                "User age is known",
                "Age is below 18",
            ],
            action_descriptions=[
                "Set age_group = youth",
            ],
            certainty_factor=1.0,
            explanation="Youth users require conservative exercise programming and supervision-focused recommendations.",
        ),

        Rule(
            rule_id="R-AGE-002",
            name="Classify adult user",
            category=CATEGORY_AGE_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                has_fact("age"),
                fact_between("age", 18, 60),
            ],
            actions=[
                add_fact_action(
                    "age_group",
                    "adult",
                    1.0,
                    "User age is between 18 and 59.",
                )
            ],
            condition_descriptions=[
                "User age is known",
                "Age is between 18 and 59",
            ],
            action_descriptions=[
                "Set age_group = adult",
            ],
            certainty_factor=1.0,
            explanation="Adult users can usually follow standard training recommendations unless limited by injuries or medical conditions.",
        ),

        Rule(
            rule_id="R-AGE-003",
            name="Classify senior user",
            category=CATEGORY_AGE_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                has_fact("age"),
                fact_greater_equal("age", 60),
            ],
            actions=[
                add_fact_action(
                    "age_group",
                    "senior",
                    1.0,
                    "User age is 60 or above.",
                )
            ],
            condition_descriptions=[
                "User age is known",
                "Age is 60 or above",
            ],
            action_descriptions=[
                "Set age_group = senior",
            ],
            certainty_factor=1.0,
            explanation="Senior users need joint-friendly programming, longer warm-ups, and careful intensity progression.",
        ),

        Rule(
            rule_id="R-AGE-004",
            name="Apply youth safety emphasis",
            category=CATEGORY_AGE_CLASSIFICATION,
            salience=SALIENCE["age_safety"],
            conditions=[
                fact_equals("age_group", "youth"),
            ],
            actions=[
                add_fact_action(
                    "needs_supervision_focus",
                    True,
                    0.9,
                    "Youth users should prioritize supervision and technique.",
                )
            ],
            condition_descriptions=[
                "age_group is youth",
            ],
            action_descriptions=[
                "Set needs_supervision_focus = True",
            ],
            certainty_factor=0.9,
            explanation="Youth training should avoid ego lifting and focus on safe movement learning.",
        ),

        Rule(
            rule_id="R-AGE-005",
            name="Apply senior low-impact preference",
            category=CATEGORY_AGE_CLASSIFICATION,
            salience=SALIENCE["age_safety"],
            conditions=[
                fact_equals("age_group", "senior"),
            ],
            actions=[
                add_fact_action(
                    "needs_low_impact_training",
                    True,
                    0.85,
                    "Senior users benefit from joint-friendly low-impact options.",
                )
            ],
            condition_descriptions=[
                "age_group is senior",
            ],
            action_descriptions=[
                "Set needs_low_impact_training = True",
            ],
            certainty_factor=0.85,
            explanation="Senior users may have higher joint stress risk, so lower-impact training is preferred.",
        ),

        # ============================================================
        # BMI CLASSIFICATION RULES
        # ============================================================

        Rule(
            rule_id="R-BMI-001",
            name="Classify underweight BMI",
            category=CATEGORY_BMI_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                has_fact("bmi"),
                fact_less_than("bmi", 18.5),
            ],
            actions=[
                add_fact_action(
                    "bmi_category",
                    "underweight",
                    1.0,
                    "BMI is below 18.5.",
                )
            ],
            condition_descriptions=[
                "BMI is known",
                "BMI is below 18.5",
            ],
            action_descriptions=[
                "Set bmi_category = underweight",
            ],
            certainty_factor=1.0,
            explanation="Underweight users may need conservative volume and strength-building focus.",
        ),

        Rule(
            rule_id="R-BMI-002",
            name="Classify normal BMI",
            category=CATEGORY_BMI_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                has_fact("bmi"),
                fact_between("bmi", 18.5, 25),
            ],
            actions=[
                add_fact_action(
                    "bmi_category",
                    "normal",
                    1.0,
                    "BMI is between 18.5 and 24.9.",
                )
            ],
            condition_descriptions=[
                "BMI is known",
                "BMI is between 18.5 and 24.9",
            ],
            action_descriptions=[
                "Set bmi_category = normal",
            ],
            certainty_factor=1.0,
            explanation="Normal BMI allows standard program selection based mainly on goal, experience, and equipment.",
        ),

        Rule(
            rule_id="R-BMI-003",
            name="Classify overweight BMI",
            category=CATEGORY_BMI_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                has_fact("bmi"),
                fact_between("bmi", 25, 30),
            ],
            actions=[
                add_fact_action(
                    "bmi_category",
                    "overweight",
                    1.0,
                    "BMI is between 25 and 29.9.",
                )
            ],
            condition_descriptions=[
                "BMI is known",
                "BMI is between 25 and 29.9",
            ],
            action_descriptions=[
                "Set bmi_category = overweight",
            ],
            certainty_factor=1.0,
            explanation="Overweight BMI may increase joint loading, especially during jumping or running.",
        ),

        Rule(
            rule_id="R-BMI-004",
            name="Classify obese BMI",
            category=CATEGORY_BMI_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                has_fact("bmi"),
                fact_greater_equal("bmi", 30),
            ],
            actions=[
                add_fact_action(
                    "bmi_category",
                    "obese",
                    1.0,
                    "BMI is 30 or above.",
                )
            ],
            condition_descriptions=[
                "BMI is known",
                "BMI is 30 or above",
            ],
            action_descriptions=[
                "Set bmi_category = obese",
            ],
            certainty_factor=1.0,
            explanation="Obese BMI increases the importance of low-impact conditioning and gradual progression.",
        ),

        Rule(
            rule_id="R-BMI-005",
            name="Detect joint stress risk for overweight user",
            category=CATEGORY_BMI_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                fact_equals("bmi_category", "overweight"),
            ],
            actions=[
                add_fact_action(
                    "joint_stress_risk",
                    "moderate",
                    0.75,
                    "Overweight BMI may moderately increase joint stress.",
                )
            ],
            condition_descriptions=[
                "bmi_category is overweight",
            ],
            action_descriptions=[
                "Set joint_stress_risk = moderate",
            ],
            certainty_factor=0.75,
            explanation="Extra body mass can increase knee and ankle stress during impact-based activities.",
        ),

        Rule(
            rule_id="R-BMI-006",
            name="Detect joint stress risk for obese user",
            category=CATEGORY_BMI_CLASSIFICATION,
            salience=SALIENCE["classification"],
            conditions=[
                fact_equals("bmi_category", "obese"),
            ],
            actions=[
                add_fact_action(
                    "joint_stress_risk",
                    "high",
                    0.9,
                    "Obese BMI may significantly increase joint stress.",
                )
            ],
            condition_descriptions=[
                "bmi_category is obese",
            ],
            action_descriptions=[
                "Set joint_stress_risk = high",
            ],
            certainty_factor=0.9,
            explanation="Higher BMI can increase impact forces, so safer low-impact training is preferred.",
        ),

        Rule(
            rule_id="R-BMI-007",
            name="Prefer low-impact training for high joint stress",
            category=CATEGORY_BMI_CLASSIFICATION,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("joint_stress_risk", "high"),
            ],
            actions=[
                add_fact_action(
                    "needs_low_impact_training",
                    True,
                    0.9,
                    "High joint stress risk detected.",
                )
            ],
            condition_descriptions=[
                "joint_stress_risk is high",
            ],
            action_descriptions=[
                "Set needs_low_impact_training = True",
            ],
            certainty_factor=0.9,
            explanation="Low-impact training reduces unnecessary stress on knees, hips, and ankles.",
        ),

        # ============================================================
        # EXPERIENCE RULES
        # ============================================================

        Rule(
            rule_id="R-EXP-001",
            name="Set beginner training volume",
            category=CATEGORY_EXPERIENCE_ANALYSIS,
            salience=SALIENCE["experience"],
            conditions=[
                fact_equals("experience_level", "beginner"),
            ],
            actions=[
                add_fact_action(
                    "training_volume",
                    "low",
                    0.95,
                    "Beginner users should start with lower volume.",
                )
            ],
            condition_descriptions=[
                "experience_level is beginner",
            ],
            action_descriptions=[
                "Set training_volume = low",
            ],
            certainty_factor=0.95,
            explanation="Beginners need lower training volume to learn technique and avoid excessive soreness.",
        ),

        Rule(
            rule_id="R-EXP-002",
            name="Set intermediate training volume",
            category=CATEGORY_EXPERIENCE_ANALYSIS,
            salience=SALIENCE["experience"],
            conditions=[
                fact_equals("experience_level", "intermediate"),
            ],
            actions=[
                add_fact_action(
                    "training_volume",
                    "moderate",
                    0.9,
                    "Intermediate users can tolerate moderate volume.",
                )
            ],
            condition_descriptions=[
                "experience_level is intermediate",
            ],
            action_descriptions=[
                "Set training_volume = moderate",
            ],
            certainty_factor=0.9,
            explanation="Intermediate users usually have enough skill and recovery capacity for moderate weekly volume.",
        ),

        Rule(
            rule_id="R-EXP-003",
            name="Set advanced training volume",
            category=CATEGORY_EXPERIENCE_ANALYSIS,
            salience=SALIENCE["experience"],
            conditions=[
                fact_equals("experience_level", "advanced"),
            ],
            actions=[
                add_fact_action(
                    "training_volume",
                    "high",
                    0.85,
                    "Advanced users can tolerate higher volume if no safety restrictions exist.",
                )
            ],
            condition_descriptions=[
                "experience_level is advanced",
            ],
            action_descriptions=[
                "Set training_volume = high",
            ],
            certainty_factor=0.85,
            explanation="Advanced users can use more volume and intensity, but injury rules still override this.",
        ),

        Rule(
            rule_id="R-EXP-004",
            name="Add beginner technique priority",
            category=CATEGORY_EXPERIENCE_ANALYSIS,
            salience=SALIENCE["experience"],
            conditions=[
                fact_equals("experience_level", "beginner"),
            ],
            actions=[
                add_fact_action(
                    "needs_technique_focus",
                    True,
                    0.95,
                    "Beginner user needs technique-first programming.",
                )
            ],
            condition_descriptions=[
                "experience_level is beginner",
            ],
            action_descriptions=[
                "Set needs_technique_focus = True",
            ],
            certainty_factor=0.95,
            explanation="Technique focus reduces injury risk and improves long-term progression.",
        ),

        Rule(
            rule_id="R-EXP-005",
            name="Allow advanced progression strategy",
            category=CATEGORY_EXPERIENCE_ANALYSIS,
            salience=SALIENCE["experience"],
            conditions=[
                fact_equals("experience_level", "advanced"),
                fact_equals("injury_none", True),
            ],
            actions=[
                add_fact_action(
                    "progression_style",
                    "advanced_progressive_overload",
                    0.85,
                    "Advanced user with no injuries can use stronger progression.",
                )
            ],
            condition_descriptions=[
                "experience_level is advanced",
                "No injuries are reported",
            ],
            action_descriptions=[
                "Set progression_style = advanced_progressive_overload",
            ],
            certainty_factor=0.85,
            explanation="Advanced users without injuries can progress load, reps, or volume more aggressively.",
        ),

        # ============================================================
        # SCHEDULE RULES
        # ============================================================

        Rule(
            rule_id="R-SCH-001",
            name="Select two-day full body split",
            category=CATEGORY_SCHEDULE_ANALYSIS,
            salience=SALIENCE["schedule"],
            conditions=[
                has_fact("available_days"),
                lambda facts: facts.get("available_days") <= 2,
            ],
            actions=[
                add_fact_action(
                    "training_split",
                    "full_body",
                    0.95,
                    "One to two training days works best with full-body sessions.",
                )
            ],
            condition_descriptions=[
                "available_days is known",
                "available_days is 1 or 2",
            ],
            action_descriptions=[
                "Set training_split = full_body",
            ],
            certainty_factor=0.95,
            explanation="With limited weekly availability, full-body sessions cover major movement patterns efficiently.",
        ),

        Rule(
            rule_id="R-SCH-002",
            name="Select three-day full body split",
            category=CATEGORY_SCHEDULE_ANALYSIS,
            salience=SALIENCE["schedule"],
            conditions=[
                fact_equals("available_days", 3),
            ],
            actions=[
                add_fact_action(
                    "training_split",
                    "three_day_full_body",
                    0.95,
                    "Three days per week suits a full-body routine.",
                )
            ],
            condition_descriptions=[
                "available_days is 3",
            ],
            action_descriptions=[
                "Set training_split = three_day_full_body",
            ],
            certainty_factor=0.95,
            explanation="A three-day full-body plan balances frequency, recovery, and simplicity.",
        ),

        Rule(
            rule_id="R-SCH-003",
            name="Select four-day upper lower split",
            category=CATEGORY_SCHEDULE_ANALYSIS,
            salience=SALIENCE["schedule"],
            conditions=[
                fact_equals("available_days", 4),
            ],
            actions=[
                add_fact_action(
                    "training_split",
                    "upper_lower",
                    0.95,
                    "Four days per week suits an upper/lower split.",
                )
            ],
            condition_descriptions=[
                "available_days is 4",
            ],
            action_descriptions=[
                "Set training_split = upper_lower",
            ],
            certainty_factor=0.95,
            explanation="Upper/lower split provides good frequency and recovery for four weekly sessions.",
        ),

        Rule(
            rule_id="R-SCH-004",
            name="Select five-day hybrid split",
            category=CATEGORY_SCHEDULE_ANALYSIS,
            salience=SALIENCE["schedule"],
            conditions=[
                fact_equals("available_days", 5),
            ],
            actions=[
                add_fact_action(
                    "training_split",
                    "hybrid_strength_conditioning",
                    0.9,
                    "Five days allows strength plus conditioning or accessory work.",
                )
            ],
            condition_descriptions=[
                "available_days is 5",
            ],
            action_descriptions=[
                "Set training_split = hybrid_strength_conditioning",
            ],
            certainty_factor=0.9,
            explanation="Five weekly days allow more specialization while still preserving recovery.",
        ),

        Rule(
            rule_id="R-SCH-005",
            name="Select six day push pull legs split",
            category=CATEGORY_SCHEDULE_ANALYSIS,
            salience=SALIENCE["schedule"],
            conditions=[
                has_fact("available_days"),
                lambda facts: facts.get("available_days") >= 6,
            ],
            actions=[
                add_fact_action(
                    "training_split",
                    "push_pull_legs",
                    0.85,
                    "Six or more days can support push/pull/legs programming.",
                )
            ],
            condition_descriptions=[
                "available_days is known",
                "available_days is 6 or more",
            ],
            action_descriptions=[
                "Set training_split = push_pull_legs",
            ],
            certainty_factor=0.85,
            explanation="Push/pull/legs works well for frequent training but must be adjusted if safety risks exist.",
        ),

        # ============================================================
        # EQUIPMENT RULES
        # ============================================================

        Rule(
            rule_id="R-EQP-001",
            name="Classify full gym equipment",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("equipment", "full_gym"),
            ],
            actions=[
                add_fact_action(
                    "equipment_level",
                    "full",
                    1.0,
                    "User has access to a full gym.",
                )
            ],
            condition_descriptions=[
                "equipment is full_gym",
            ],
            action_descriptions=[
                "Set equipment_level = full",
            ],
            certainty_factor=1.0,
            explanation="Full gym access allows machines, barbells, dumbbells, and cardio equipment.",
        ),

        Rule(
            rule_id="R-EQP-002",
            name="Classify dumbbell home equipment",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("equipment", "home_dumbbells"),
            ],
            actions=[
                add_fact_action(
                    "equipment_level",
                    "limited_weights",
                    1.0,
                    "User has dumbbells at home.",
                )
            ],
            condition_descriptions=[
                "equipment is home_dumbbells",
            ],
            action_descriptions=[
                "Set equipment_level = limited_weights",
            ],
            certainty_factor=1.0,
            explanation="Dumbbells support many strength exercises but limit heavy barbell-style progression.",
        ),

        Rule(
            rule_id="R-EQP-003",
            name="Classify bodyweight-only equipment",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("equipment", "bodyweight_only"),
            ],
            actions=[
                add_fact_action(
                    "equipment_level",
                    "bodyweight",
                    1.0,
                    "User has bodyweight-only training setup.",
                )
            ],
            condition_descriptions=[
                "equipment is bodyweight_only",
            ],
            action_descriptions=[
                "Set equipment_level = bodyweight",
            ],
            certainty_factor=1.0,
            explanation="Bodyweight training requires exercise progressions using leverage, tempo, and volume.",
        ),

        Rule(
            rule_id="R-EQP-004",
            name="Prefer dumbbell variations",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("equipment_level", "limited_weights"),
            ],
            actions=[
                add_fact_action(
                    "exercise_selection_style",
                    "dumbbell_based",
                    0.95,
                    "Dumbbell-based exercises should be prioritized.",
                )
            ],
            condition_descriptions=[
                "equipment_level is limited_weights",
            ],
            action_descriptions=[
                "Set exercise_selection_style = dumbbell_based",
            ],
            certainty_factor=0.95,
            explanation="Home dumbbell users need exercises that match available equipment.",
        ),

        Rule(
            rule_id="R-EQP-005",
            name="Prefer bodyweight progressions",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("equipment_level", "bodyweight"),
            ],
            actions=[
                add_fact_action(
                    "exercise_selection_style",
                    "bodyweight_progressions",
                    0.95,
                    "Bodyweight progressions should be prioritized.",
                )
            ],
            condition_descriptions=[
                "equipment_level is bodyweight",
            ],
            action_descriptions=[
                "Set exercise_selection_style = bodyweight_progressions",
            ],
            certainty_factor=0.95,
            explanation="Bodyweight-only users need movements such as squats, push-ups, bridges, planks, and progressions.",
        ),

        Rule(
            rule_id="R-EQP-006",
            name="Allow machine-supported exercise options",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("equipment_level", "full"),
            ],
            actions=[
                add_fact_action(
                    "exercise_selection_style",
                    "full_gym_options",
                    0.95,
                    "Full gym exercise options are available.",
                )
            ],
            condition_descriptions=[
                "equipment_level is full",
            ],
            action_descriptions=[
                "Set exercise_selection_style = full_gym_options",
            ],
            certainty_factor=0.95,
            explanation="A full gym allows safer machine alternatives, free-weight lifts, and cardio equipment.",
        ),

        # ============================================================
        # MEDICAL SAFETY RULES
        # ============================================================

        Rule(
            rule_id="R-MED-001",
            name="Detect no medical condition",
            category=CATEGORY_MEDICAL_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("condition_none", True),
            ],
            actions=[
                add_fact_action(
                    "medical_restriction_level",
                    "none",
                    1.0,
                    "User reported no medical conditions.",
                )
            ],
            condition_descriptions=[
                "condition_none is True",
            ],
            action_descriptions=[
                "Set medical_restriction_level = none",
            ],
            certainty_factor=1.0,
            explanation="No reported medical condition means normal exercise screening can continue.",
        ),

        Rule(
            rule_id="R-MED-002",
            name="Detect asthma condition",
            category=CATEGORY_MEDICAL_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("condition_asthma", True),
            ],
            actions=[
                add_fact_action(
                    "cardio_caution_required",
                    True,
                    0.9,
                    "Asthma condition requires cardio intensity caution.",
                )
            ],
            condition_descriptions=[
                "condition_asthma is True",
            ],
            action_descriptions=[
                "Set cardio_caution_required = True",
            ],
            certainty_factor=0.9,
            explanation="Asthma may affect tolerance to intense cardio, so gradual warm-up and controlled intensity are preferred.",
        ),

        Rule(
            rule_id="R-MED-003",
            name="Recommend extended warm-up for asthma",
            category=CATEGORY_MEDICAL_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("cardio_caution_required", True),
            ],
            actions=[
                add_fact_action(
                    "requires_extended_warmup",
                    True,
                    0.9,
                    "Cardio caution indicates need for extended warm-up.",
                )
            ],
            condition_descriptions=[
                "cardio_caution_required is True",
            ],
            action_descriptions=[
                "Set requires_extended_warmup = True",
            ],
            certainty_factor=0.9,
            explanation="A longer warm-up can reduce sudden intensity spikes for users with asthma.",
        ),

        Rule(
            rule_id="R-MED-004",
            name="Use controlled endurance protocol for asthma",
            category=CATEGORY_MEDICAL_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("condition_asthma", True),
                fact_equals("goal", "endurance"),
            ],
            actions=[
                add_fact_action(
                    "endurance_protocol",
                    "controlled_low_to_moderate_intensity",
                    0.85,
                    "Asthma plus endurance goal requires controlled intensity.",
                )
            ],
            condition_descriptions=[
                "condition_asthma is True",
                "goal is endurance",
            ],
            action_descriptions=[
                "Set endurance_protocol = controlled_low_to_moderate_intensity",
            ],
            certainty_factor=0.85,
            explanation="Endurance training can still be used, but intensity should progress gradually for asthma users.",
        ),

        # ============================================================
        # INJURY SAFETY RULES
        # ============================================================

        Rule(
            rule_id="R-INJ-001",
            name="Detect no injury",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("injury_none", True),
            ],
            actions=[
                add_fact_action(
                    "injury_restriction_level",
                    "none",
                    1.0,
                    "User reported no injuries.",
                )
            ],
            condition_descriptions=[
                "injury_none is True",
            ],
            action_descriptions=[
                "Set injury_restriction_level = none",
            ],
            certainty_factor=1.0,
            explanation="No reported injury means normal exercise selection can continue.",
        ),

        Rule(
            rule_id="R-INJ-002",
            name="Detect mild knee limitation",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("injury_knee", "mild"),
            ],
            actions=[
                add_fact_action(
                    "knee_risk_level",
                    "mild",
                    0.8,
                    "Mild knee issue detected.",
                )
            ],
            condition_descriptions=[
                "injury_knee is mild",
            ],
            action_descriptions=[
                "Set knee_risk_level = mild",
            ],
            certainty_factor=0.8,
            explanation="Mild knee discomfort does not fully block lower-body training but requires careful movement selection.",
        ),

        Rule(
            rule_id="R-INJ-003",
            name="Detect moderate knee limitation",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("injury_knee", "moderate"),
            ],
            actions=[
                add_fact_action(
                    "knee_risk_level",
                    "moderate",
                    0.9,
                    "Moderate knee issue detected.",
                )
            ],
            condition_descriptions=[
                "injury_knee is moderate",
            ],
            action_descriptions=[
                "Set knee_risk_level = moderate",
            ],
            certainty_factor=0.9,
            explanation="Moderate knee issues require avoiding jumping, sprinting, and deep knee-dominant exercises.",
        ),

        Rule(
            rule_id="R-INJ-004",
            name="Detect severe knee limitation",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("injury_knee", "severe"),
            ],
            actions=[
                add_fact_action(
                    "medical_clearance_required",
                    True,
                    0.95,
                    "Severe knee issue requires professional clearance.",
                )
            ],
            condition_descriptions=[
                "injury_knee is severe",
            ],
            action_descriptions=[
                "Set medical_clearance_required = True",
            ],
            certainty_factor=0.95,
            explanation="Severe knee pain should be evaluated before exercise recommendations are intensified.",
        ),

        Rule(
            rule_id="R-INJ-005",
            name="Prefer knee-safe training",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_in("knee_risk_level", {"mild", "moderate"}),
            ],
            actions=[
                add_fact_action(
                    "needs_knee_safe_training",
                    True,
                    0.9,
                    "Knee risk requires knee-safe exercise selection.",
                )
            ],
            condition_descriptions=[
                "knee_risk_level is mild or moderate",
            ],
            action_descriptions=[
                "Set needs_knee_safe_training = True",
            ],
            certainty_factor=0.9,
            explanation="Knee-safe training reduces high-impact movements and limits painful ranges of motion.",
        ),

        Rule(
            rule_id="R-INJ-006",
            name="Avoid high impact for knee risk",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("needs_knee_safe_training", True),
            ],
            actions=[
                add_fact_action(
                    "avoid_high_impact",
                    True,
                    0.9,
                    "Knee-safe training requires avoiding high-impact work.",
                )
            ],
            condition_descriptions=[
                "needs_knee_safe_training is True",
            ],
            action_descriptions=[
                "Set avoid_high_impact = True",
            ],
            certainty_factor=0.9,
            explanation="Jumping, sprinting, and aggressive plyometrics can aggravate knee symptoms.",
        ),

        Rule(
            rule_id="R-INJ-007",
            name="Detect lower back limitation",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                has_fact("injury_lower_back"),
                fact_in("injury_lower_back", {"mild", "moderate", "severe"}),
            ],
            actions=[
                add_fact_action(
                    "back_risk_level",
                    "present",
                    0.9,
                    "Lower back issue detected.",
                )
            ],
            condition_descriptions=[
                "Lower back injury fact exists",
                "Lower back injury severity is mild, moderate, or severe",
            ],
            action_descriptions=[
                "Set back_risk_level = present",
            ],
            certainty_factor=0.9,
            explanation="Lower back issues require careful core stability and avoidance of heavy spinal loading.",
        ),

        Rule(
            rule_id="R-INJ-008",
            name="Avoid heavy spinal loading",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("back_risk_level", "present"),
            ],
            actions=[
                add_fact_action(
                    "avoid_heavy_spinal_loading",
                    True,
                    0.9,
                    "Back risk requires avoiding heavy spinal loading.",
                )
            ],
            condition_descriptions=[
                "back_risk_level is present",
            ],
            action_descriptions=[
                "Set avoid_heavy_spinal_loading = True",
            ],
            certainty_factor=0.9,
            explanation="Heavy axial loading may aggravate lower back symptoms.",
        ),

        Rule(
            rule_id="R-INJ-009",
            name="Detect severe lower back issue",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("injury_lower_back", "severe"),
            ],
            actions=[
                add_fact_action(
                    "medical_clearance_required",
                    True,
                    0.95,
                    "Severe lower back issue requires professional clearance.",
                )
            ],
            condition_descriptions=[
                "injury_lower_back is severe",
            ],
            action_descriptions=[
                "Set medical_clearance_required = True",
            ],
            certainty_factor=0.95,
            explanation="Severe back pain should be cleared by a professional before exercise intensity is increased.",
        ),

        Rule(
            rule_id="R-INJ-010",
            name="Detect shoulder limitation",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                has_fact("injury_shoulder"),
                fact_in("injury_shoulder", {"mild", "moderate", "severe"}),
            ],
            actions=[
                add_fact_action(
                    "shoulder_risk_level",
                    "present",
                    0.9,
                    "Shoulder issue detected.",
                )
            ],
            condition_descriptions=[
                "Shoulder injury fact exists",
                "Shoulder injury severity is mild, moderate, or severe",
            ],
            action_descriptions=[
                "Set shoulder_risk_level = present",
            ],
            certainty_factor=0.9,
            explanation="Shoulder limitations require safer pressing angles and avoidance of painful overhead work.",
        ),

        Rule(
            rule_id="R-INJ-011",
            name="Avoid overhead pressing for shoulder risk",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("shoulder_risk_level", "present"),
            ],
            actions=[
                add_fact_action(
                    "avoid_overhead_pressing",
                    True,
                    0.85,
                    "Shoulder risk requires limiting overhead pressing.",
                )
            ],
            condition_descriptions=[
                "shoulder_risk_level is present",
            ],
            action_descriptions=[
                "Set avoid_overhead_pressing = True",
            ],
            certainty_factor=0.85,
            explanation="Overhead pressing can aggravate shoulder pain if mobility or stability is limited.",
        ),

        Rule(
            rule_id="R-INJ-012",
            name="Detect severe shoulder issue",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("injury_shoulder", "severe"),
            ],
            actions=[
                add_fact_action(
                    "medical_clearance_required",
                    True,
                    0.95,
                    "Severe shoulder issue requires professional clearance.",
                )
            ],
            condition_descriptions=[
                "injury_shoulder is severe",
            ],
            action_descriptions=[
                "Set medical_clearance_required = True",
            ],
            certainty_factor=0.95,
            explanation="Severe shoulder pain should be professionally assessed before upper-body loading.",
        ),

        # ============================================================
        # GOAL ANALYSIS RULES
        # ============================================================

        Rule(
            rule_id="R-GOAL-001",
            name="Set strength goal direction",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal", "strength"),
            ],
            actions=[
                add_fact_action(
                    "goal_direction",
                    "strength_focused",
                    0.95,
                    "User selected strength as primary goal.",
                )
            ],
            condition_descriptions=[
                "goal is strength",
            ],
            action_descriptions=[
                "Set goal_direction = strength_focused",
            ],
            certainty_factor=0.95,
            explanation="Strength goals prioritize compound movements, progressive overload, and lower-to-moderate rep ranges.",
        ),

        Rule(
            rule_id="R-GOAL-002",
            name="Set muscle gain goal direction",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal", "muscle_gain"),
            ],
            actions=[
                add_fact_action(
                    "goal_direction",
                    "hypertrophy_focused",
                    0.95,
                    "User selected muscle gain as primary goal.",
                )
            ],
            condition_descriptions=[
                "goal is muscle_gain",
            ],
            action_descriptions=[
                "Set goal_direction = hypertrophy_focused",
            ],
            certainty_factor=0.95,
            explanation="Muscle gain goals prioritize moderate volume, controlled tempo, and progressive resistance.",
        ),

        Rule(
            rule_id="R-GOAL-003",
            name="Set fat loss goal direction",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal", "fat_loss"),
            ],
            actions=[
                add_fact_action(
                    "goal_direction",
                    "fat_loss_focused",
                    0.95,
                    "User selected fat loss as primary goal.",
                )
            ],
            condition_descriptions=[
                "goal is fat_loss",
            ],
            action_descriptions=[
                "Set goal_direction = fat_loss_focused",
            ],
            certainty_factor=0.95,
            explanation="Fat loss goals benefit from resistance training plus conditioning while preserving safety.",
        ),

        Rule(
            rule_id="R-GOAL-004",
            name="Set endurance goal direction",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal", "endurance"),
            ],
            actions=[
                add_fact_action(
                    "goal_direction",
                    "endurance_focused",
                    0.95,
                    "User selected endurance as primary goal.",
                )
            ],
            condition_descriptions=[
                "goal is endurance",
            ],
            action_descriptions=[
                "Set goal_direction = endurance_focused",
            ],
            certainty_factor=0.95,
            explanation="Endurance goals prioritize cardiovascular capacity, pacing, and gradual workload progression.",
        ),

        Rule(
            rule_id="R-GOAL-005",
            name="Set flexibility goal direction",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal", "flexibility"),
            ],
            actions=[
                add_fact_action(
                    "goal_direction",
                    "mobility_focused",
                    0.95,
                    "User selected flexibility as primary goal.",
                )
            ],
            condition_descriptions=[
                "goal is flexibility",
            ],
            action_descriptions=[
                "Set goal_direction = mobility_focused",
            ],
            certainty_factor=0.95,
            explanation="Flexibility goals prioritize mobility, stretching, range of motion, and controlled movement quality.",
        ),

        Rule(
            rule_id="R-GOAL-006",
            name="Prefer low-impact fat loss when overweight",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "fat_loss_focused"),
                fact_in("bmi_category", {"overweight", "obese"}),
            ],
            actions=[
                add_fact_action(
                    "conditioning_style",
                    "low_impact_fat_loss",
                    0.85,
                    "Fat loss user with elevated BMI should use lower-impact conditioning.",
                )
            ],
            condition_descriptions=[
                "goal_direction is fat_loss_focused",
                "bmi_category is overweight or obese",
            ],
            action_descriptions=[
                "Set conditioning_style = low_impact_fat_loss",
            ],
            certainty_factor=0.85,
            explanation="Low-impact conditioning supports fat loss while reducing unnecessary joint stress.",
        ),

        Rule(
            rule_id="R-GOAL-007",
            name="Prefer technique-first strength for beginners",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "strength_focused"),
                fact_equals("experience_level", "beginner"),
            ],
            actions=[
                add_fact_action(
                    "program_emphasis",
                    "technique_first_strength",
                    0.9,
                    "Beginner strength goal requires technique-first loading.",
                )
            ],
            condition_descriptions=[
                "goal_direction is strength_focused",
                "experience_level is beginner",
            ],
            action_descriptions=[
                "Set program_emphasis = technique_first_strength",
            ],
            certainty_factor=0.9,
            explanation="Beginner strength training should build skill before heavier loading.",
        ),

        Rule(
            rule_id="R-GOAL-008",
            name="Prefer mobility base for flexibility goal",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "mobility_focused"),
            ],
            actions=[
                add_fact_action(
                    "program_emphasis",
                    "mobility_and_control",
                    0.9,
                    "Flexibility goal requires mobility and control emphasis.",
                )
            ],
            condition_descriptions=[
                "goal_direction is mobility_focused",
            ],
            action_descriptions=[
                "Set program_emphasis = mobility_and_control",
            ],
            certainty_factor=0.9,
            explanation="Flexibility improves best when stretching is combined with controlled range-of-motion practice.",
        ),

        # ============================================================
        # INTENSITY PROFILE RULES
        # ============================================================

        Rule(
            rule_id="R-INT-001",
            name="Set strength intensity profile",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "strength_focused"),
            ],
            actions=[
                add_fact_action(
                    "intensity_profile",
                    "strength_low_reps_progressive_load",
                    0.9,
                    "Strength goal requires lower reps and progressive loading.",
                )
            ],
            condition_descriptions=[
                "goal_direction is strength_focused",
            ],
            action_descriptions=[
                "Set intensity_profile = strength_low_reps_progressive_load",
            ],
            certainty_factor=0.9,
            explanation="Strength programs usually emphasize heavier resistance, lower repetitions, and gradual load progression.",
        ),

        Rule(
            rule_id="R-INT-002",
            name="Set hypertrophy intensity profile",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "hypertrophy_focused"),
            ],
            actions=[
                add_fact_action(
                    "intensity_profile",
                    "moderate_reps_muscle_tension",
                    0.9,
                    "Muscle gain goal requires moderate reps and controlled tension.",
                )
            ],
            condition_descriptions=[
                "goal_direction is hypertrophy_focused",
            ],
            action_descriptions=[
                "Set intensity_profile = moderate_reps_muscle_tension",
            ],
            certainty_factor=0.9,
            explanation="Hypertrophy training benefits from moderate repetitions, sufficient volume, and controlled movement tempo.",
        ),

        Rule(
            rule_id="R-INT-003",
            name="Set fat-loss intensity profile",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "fat_loss_focused"),
            ],
            actions=[
                add_fact_action(
                    "intensity_profile",
                    "resistance_plus_conditioning",
                    0.9,
                    "Fat-loss goal requires resistance training plus conditioning.",
                )
            ],
            condition_descriptions=[
                "goal_direction is fat_loss_focused",
            ],
            action_descriptions=[
                "Set intensity_profile = resistance_plus_conditioning",
            ],
            certainty_factor=0.9,
            explanation="Fat-loss programs should combine strength work with safe conditioning to improve energy expenditure while preserving muscle.",
        ),

        Rule(
            rule_id="R-INT-004",
            name="Set endurance intensity profile",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "endurance_focused"),
            ],
            actions=[
                add_fact_action(
                    "intensity_profile",
                    "aerobic_base_progression",
                    0.9,
                    "Endurance goal requires aerobic base progression.",
                )
            ],
            condition_descriptions=[
                "goal_direction is endurance_focused",
            ],
            action_descriptions=[
                "Set intensity_profile = aerobic_base_progression",
            ],
            certainty_factor=0.9,
            explanation="Endurance training should gradually build aerobic capacity before intense intervals are emphasized.",
        ),

        Rule(
            rule_id="R-INT-005",
            name="Set flexibility intensity profile",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "mobility_focused"),
            ],
            actions=[
                add_fact_action(
                    "intensity_profile",
                    "controlled_mobility_and_stretching",
                    0.9,
                    "Flexibility goal requires controlled mobility and stretching.",
                )
            ],
            condition_descriptions=[
                "goal_direction is mobility_focused",
            ],
            action_descriptions=[
                "Set intensity_profile = controlled_mobility_and_stretching",
            ],
            certainty_factor=0.9,
            explanation="Flexibility-focused users should prioritize controlled range of motion, breathing, and gradual stretch tolerance.",
        ),

        Rule(
            rule_id="R-INT-006",
            name="Override intensity when medical clearance is required",
            category=CATEGORY_MEDICAL_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("medical_clearance_required", True),
            ],
            actions=[
                add_fact_action(
                    "intensity_profile",
                    "clearance_required_before_training",
                    0.95,
                    "Severe injury requires medical clearance before intensity is assigned.",
                )
            ],
            condition_descriptions=[
                "medical_clearance_required is True",
            ],
            action_descriptions=[
                "Set intensity_profile = clearance_required_before_training",
            ],
            certainty_factor=0.95,
            explanation="Safety rules override normal training rules when severe injury risk is present.",
        ),

        # ============================================================
        # SETS, REPS, AND VOLUME RULES
        # ============================================================

        Rule(
            rule_id="R-VOL-001",
            name="Assign beginner set scheme",
            category=CATEGORY_EXPERIENCE_ANALYSIS,
            salience=SALIENCE["experience"],
            conditions=[
                fact_equals("training_volume", "low"),
            ],
            actions=[
                add_fact_action(
                    "set_scheme",
                    "2_to_3_sets_per_exercise",
                    0.9,
                    "Low training volume maps to 2–3 sets per exercise.",
                )
            ],
            condition_descriptions=[
                "training_volume is low",
            ],
            action_descriptions=[
                "Set set_scheme = 2_to_3_sets_per_exercise",
            ],
            certainty_factor=0.9,
            explanation="Beginners should start with fewer sets to learn technique and recover well.",
        ),

        Rule(
            rule_id="R-VOL-002",
            name="Assign intermediate set scheme",
            category=CATEGORY_EXPERIENCE_ANALYSIS,
            salience=SALIENCE["experience"],
            conditions=[
                fact_equals("training_volume", "moderate"),
            ],
            actions=[
                add_fact_action(
                    "set_scheme",
                    "3_to_4_sets_per_exercise",
                    0.9,
                    "Moderate training volume maps to 3–4 sets per exercise.",
                )
            ],
            condition_descriptions=[
                "training_volume is moderate",
            ],
            action_descriptions=[
                "Set set_scheme = 3_to_4_sets_per_exercise",
            ],
            certainty_factor=0.9,
            explanation="Intermediate users can usually handle moderate set volume while still recovering effectively.",
        ),

        Rule(
            rule_id="R-VOL-003",
            name="Assign advanced set scheme",
            category=CATEGORY_EXPERIENCE_ANALYSIS,
            salience=SALIENCE["experience"],
            conditions=[
                fact_equals("training_volume", "high"),
            ],
            actions=[
                add_fact_action(
                    "set_scheme",
                    "4_to_5_sets_per_main_exercise",
                    0.85,
                    "High training volume maps to 4–5 sets for main exercises.",
                )
            ],
            condition_descriptions=[
                "training_volume is high",
            ],
            action_descriptions=[
                "Set set_scheme = 4_to_5_sets_per_main_exercise",
            ],
            certainty_factor=0.85,
            explanation="Advanced users may benefit from higher volume if safety restrictions do not override it.",
        ),

        Rule(
            rule_id="R-VOL-004",
            name="Assign strength rep range",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal_direction", "strength_focused"),
            ],
            actions=[
                add_fact_action(
                    "rep_range",
                    "3_to_6_reps",
                    0.9,
                    "Strength training uses lower repetition ranges.",
                )
            ],
            condition_descriptions=[
                "goal_direction is strength_focused",
            ],
            action_descriptions=[
                "Set rep_range = 3_to_6_reps",
            ],
            certainty_factor=0.9,
            explanation="Lower repetition ranges support strength development when paired with safe progressive loading.",
        ),

        Rule(
            rule_id="R-VOL-005",
            name="Assign hypertrophy rep range",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal_direction", "hypertrophy_focused"),
            ],
            actions=[
                add_fact_action(
                    "rep_range",
                    "8_to_12_reps",
                    0.9,
                    "Muscle gain training uses moderate repetition ranges.",
                )
            ],
            condition_descriptions=[
                "goal_direction is hypertrophy_focused",
            ],
            action_descriptions=[
                "Set rep_range = 8_to_12_reps",
            ],
            certainty_factor=0.9,
            explanation="Moderate repetition ranges are commonly used for muscle-building programs.",
        ),

        Rule(
            rule_id="R-VOL-006",
            name="Assign fat-loss rep range",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal_direction", "fat_loss_focused"),
            ],
            actions=[
                add_fact_action(
                    "rep_range",
                    "10_to_15_reps",
                    0.85,
                    "Fat-loss resistance work uses moderate-to-higher reps.",
                )
            ],
            condition_descriptions=[
                "goal_direction is fat_loss_focused",
            ],
            action_descriptions=[
                "Set rep_range = 10_to_15_reps",
            ],
            certainty_factor=0.85,
            explanation="Moderate-to-higher reps can support conditioning and movement practice during fat-loss programs.",
        ),

        Rule(
            rule_id="R-VOL-007",
            name="Assign endurance session duration",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal_direction", "endurance_focused"),
            ],
            actions=[
                add_fact_action(
                    "cardio_duration",
                    "20_to_40_minutes",
                    0.9,
                    "Endurance training requires dedicated cardio duration.",
                )
            ],
            condition_descriptions=[
                "goal_direction is endurance_focused",
            ],
            action_descriptions=[
                "Set cardio_duration = 20_to_40_minutes",
            ],
            certainty_factor=0.9,
            explanation="Endurance development requires sustained cardiovascular work with gradual progression.",
        ),

        Rule(
            rule_id="R-VOL-008",
            name="Assign flexibility session duration",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal_direction", "mobility_focused"),
            ],
            actions=[
                add_fact_action(
                    "mobility_duration",
                    "10_to_20_minutes_daily_or_near_daily",
                    0.9,
                    "Flexibility training benefits from frequent mobility sessions.",
                )
            ],
            condition_descriptions=[
                "goal_direction is mobility_focused",
            ],
            action_descriptions=[
                "Set mobility_duration = 10_to_20_minutes_daily_or_near_daily",
            ],
            certainty_factor=0.9,
            explanation="Flexibility improves through consistent practice rather than rare high-intensity sessions.",
        ),

        Rule(
            rule_id="R-VOL-009",
            name="Apply conservative volume modifier for senior users",
            category=CATEGORY_AGE_CLASSIFICATION,
            salience=SALIENCE["age_safety"],
            conditions=[
                fact_equals("age_group", "senior"),
            ],
            actions=[
                add_fact_action(
                    "volume_modifier",
                    "conservative_progression",
                    0.85,
                    "Senior users should progress volume conservatively.",
                )
            ],
            condition_descriptions=[
                "age_group is senior",
            ],
            action_descriptions=[
                "Set volume_modifier = conservative_progression",
            ],
            certainty_factor=0.85,
            explanation="Conservative progression helps reduce recovery and joint-stress problems in senior users.",
        ),

        # ============================================================
        # EXERCISE SELECTION STYLE RULES
        # ============================================================

        Rule(
            rule_id="R-EXS-001",
            name="Select full-gym strength exercise mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "strength_focused"),
                fact_equals("equipment_level", "full"),
            ],
            actions=[
                add_fact_action(
                    "primary_resistance_mode",
                    "compound_lifts_with_machine_support",
                    0.9,
                    "Full gym strength user can use compound lifts and machines.",
                )
            ],
            condition_descriptions=[
                "goal_direction is strength_focused",
                "equipment_level is full",
            ],
            action_descriptions=[
                "Set primary_resistance_mode = compound_lifts_with_machine_support",
            ],
            certainty_factor=0.9,
            explanation="Full gym access allows compound strength training plus safer machine-supported alternatives.",
        ),

        Rule(
            rule_id="R-EXS-002",
            name="Select dumbbell strength exercise mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "strength_focused"),
                fact_equals("equipment_level", "limited_weights"),
            ],
            actions=[
                add_fact_action(
                    "primary_resistance_mode",
                    "dumbbell_compound_lifts",
                    0.88,
                    "Dumbbell strength user should use dumbbell compound variations.",
                )
            ],
            condition_descriptions=[
                "goal_direction is strength_focused",
                "equipment_level is limited_weights",
            ],
            action_descriptions=[
                "Set primary_resistance_mode = dumbbell_compound_lifts",
            ],
            certainty_factor=0.88,
            explanation="Dumbbells can support strength work through goblet squats, presses, rows, Romanian deadlifts, and split squats.",
        ),

        Rule(
            rule_id="R-EXS-003",
            name="Select bodyweight strength exercise mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "strength_focused"),
                fact_equals("equipment_level", "bodyweight"),
            ],
            actions=[
                add_fact_action(
                    "primary_resistance_mode",
                    "bodyweight_strength_progressions",
                    0.85,
                    "Bodyweight strength user should use leverage-based progressions.",
                )
            ],
            condition_descriptions=[
                "goal_direction is strength_focused",
                "equipment_level is bodyweight",
            ],
            action_descriptions=[
                "Set primary_resistance_mode = bodyweight_strength_progressions",
            ],
            certainty_factor=0.85,
            explanation="Without weights, strength progression can come from harder movement variations, tempo, pauses, and unilateral work.",
        ),

        Rule(
            rule_id="R-EXS-004",
            name="Select full-gym hypertrophy exercise mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "hypertrophy_focused"),
                fact_equals("equipment_level", "full"),
            ],
            actions=[
                add_fact_action(
                    "primary_resistance_mode",
                    "machines_cables_and_free_weights",
                    0.9,
                    "Full gym hypertrophy user can use machines, cables, and free weights.",
                )
            ],
            condition_descriptions=[
                "goal_direction is hypertrophy_focused",
                "equipment_level is full",
            ],
            action_descriptions=[
                "Set primary_resistance_mode = machines_cables_and_free_weights",
            ],
            certainty_factor=0.9,
            explanation="Hypertrophy training benefits from multiple exercise angles and stable machine or cable options.",
        ),

        Rule(
            rule_id="R-EXS-005",
            name="Select dumbbell hypertrophy exercise mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "hypertrophy_focused"),
                fact_equals("equipment_level", "limited_weights"),
            ],
            actions=[
                add_fact_action(
                    "primary_resistance_mode",
                    "dumbbell_hypertrophy_training",
                    0.88,
                    "Dumbbell hypertrophy user should use dumbbell volume training.",
                )
            ],
            condition_descriptions=[
                "goal_direction is hypertrophy_focused",
                "equipment_level is limited_weights",
            ],
            action_descriptions=[
                "Set primary_resistance_mode = dumbbell_hypertrophy_training",
            ],
            certainty_factor=0.88,
            explanation="Dumbbells can support muscle gain through presses, rows, lunges, curls, raises, and controlled tempo work.",
        ),

        Rule(
            rule_id="R-EXS-006",
            name="Select bodyweight hypertrophy exercise mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "hypertrophy_focused"),
                fact_equals("equipment_level", "bodyweight"),
            ],
            actions=[
                add_fact_action(
                    "primary_resistance_mode",
                    "bodyweight_volume_training",
                    0.82,
                    "Bodyweight hypertrophy user should use higher-volume progressions.",
                )
            ],
            condition_descriptions=[
                "goal_direction is hypertrophy_focused",
                "equipment_level is bodyweight",
            ],
            action_descriptions=[
                "Set primary_resistance_mode = bodyweight_volume_training",
            ],
            certainty_factor=0.82,
            explanation="Bodyweight hypertrophy depends on sufficient volume, controlled tempo, and harder variations.",
        ),

        Rule(
            rule_id="R-EXS-007",
            name="Select bodyweight fat-loss circuit mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "fat_loss_focused"),
                fact_equals("equipment_level", "bodyweight"),
            ],
            actions=[
                add_fact_action(
                    "primary_resistance_mode",
                    "bodyweight_circuit_training",
                    0.85,
                    "Bodyweight fat-loss user should use safe circuit training.",
                )
            ],
            condition_descriptions=[
                "goal_direction is fat_loss_focused",
                "equipment_level is bodyweight",
            ],
            action_descriptions=[
                "Set primary_resistance_mode = bodyweight_circuit_training",
            ],
            certainty_factor=0.85,
            explanation="Bodyweight circuits can improve conditioning without needing equipment.",
        ),

        Rule(
            rule_id="R-EXS-008",
            name="Select dumbbell fat-loss circuit mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "fat_loss_focused"),
                fact_equals("equipment_level", "limited_weights"),
            ],
            actions=[
                add_fact_action(
                    "primary_resistance_mode",
                    "dumbbell_circuit_training",
                    0.88,
                    "Dumbbell fat-loss user should use dumbbell circuit training.",
                )
            ],
            condition_descriptions=[
                "goal_direction is fat_loss_focused",
                "equipment_level is limited_weights",
            ],
            action_descriptions=[
                "Set primary_resistance_mode = dumbbell_circuit_training",
            ],
            certainty_factor=0.88,
            explanation="Dumbbell circuits combine resistance training and conditioning while fitting home equipment constraints.",
        ),

        Rule(
            rule_id="R-EXS-009",
            name="Select full-gym endurance mode",
            category=CATEGORY_EQUIPMENT_ANALYSIS,
            salience=SALIENCE["equipment"],
            conditions=[
                fact_equals("goal_direction", "endurance_focused"),
                fact_equals("equipment_level", "full"),
            ],
            actions=[
                add_fact_action(
                    "primary_cardio_mode",
                    "cardio_machine_supported",
                    0.9,
                    "Full gym endurance user can use treadmill, bike, rower, or elliptical.",
                )
            ],
            condition_descriptions=[
                "goal_direction is endurance_focused",
                "equipment_level is full",
            ],
            action_descriptions=[
                "Set primary_cardio_mode = cardio_machine_supported",
            ],
            certainty_factor=0.9,
            explanation="Full gym access provides multiple cardio tools, allowing safer selection based on joint tolerance.",
        ),

        Rule(
            rule_id="R-EXS-010",
            name="Select flexibility exercise mode",
            category=CATEGORY_GOAL_ANALYSIS,
            salience=SALIENCE["goal"],
            conditions=[
                fact_equals("goal_direction", "mobility_focused"),
            ],
            actions=[
                add_fact_action(
                    "primary_mobility_mode",
                    "mobility_flow_and_static_stretching",
                    0.9,
                    "Flexibility user should use mobility flows and static stretching.",
                )
            ],
            condition_descriptions=[
                "goal_direction is mobility_focused",
            ],
            action_descriptions=[
                "Set primary_mobility_mode = mobility_flow_and_static_stretching",
            ],
            certainty_factor=0.9,
            explanation="A combination of controlled mobility and static stretching supports flexibility goals.",
        ),

        # ============================================================
        # INJURY SUBSTITUTION RULES
        # ============================================================

        Rule(
            rule_id="R-SUB-001",
            name="Select knee-safe lower-body substitutions",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("needs_knee_safe_training", True),
            ],
            actions=[
                add_fact_action(
                    "knee_safe_lower_body_options",
                    "glute_bridge_box_squat_step_up_partial_range",
                    0.9,
                    "Knee-safe lower-body options selected.",
                )
            ],
            condition_descriptions=[
                "needs_knee_safe_training is True",
            ],
            action_descriptions=[
                "Set knee_safe_lower_body_options = glute_bridge_box_squat_step_up_partial_range",
            ],
            certainty_factor=0.9,
            explanation="Knee-safe lower-body choices reduce painful knee flexion and high-impact loading.",
        ),

        Rule(
            rule_id="R-SUB-002",
            name="Select knee-safe cardio substitutions",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("needs_knee_safe_training", True),
            ],
            actions=[
                add_fact_action(
                    "knee_safe_cardio_options",
                    "walking_cycling_elliptical_if_available",
                    0.9,
                    "Knee-safe cardio options selected.",
                )
            ],
            condition_descriptions=[
                "needs_knee_safe_training is True",
            ],
            action_descriptions=[
                "Set knee_safe_cardio_options = walking_cycling_elliptical_if_available",
            ],
            certainty_factor=0.9,
            explanation="Walking, cycling, and elliptical-style conditioning are usually lower impact than jumping or sprinting.",
        ),

        Rule(
            rule_id="R-SUB-003",
            name="Avoid deep knee flexion when knee risk exists",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("needs_knee_safe_training", True),
            ],
            actions=[
                add_fact_action(
                    "avoid_deep_knee_flexion",
                    True,
                    0.85,
                    "Knee risk requires avoiding painful deep knee flexion.",
                )
            ],
            condition_descriptions=[
                "needs_knee_safe_training is True",
            ],
            action_descriptions=[
                "Set avoid_deep_knee_flexion = True",
            ],
            certainty_factor=0.85,
            explanation="Deep knee flexion may aggravate symptoms in some users with knee limitations.",
        ),

        Rule(
            rule_id="R-SUB-004",
            name="Select lower-back-safe lower-body substitutions",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("back_risk_level", "present"),
            ],
            actions=[
                add_fact_action(
                    "back_safe_lower_body_options",
                    "glute_bridge_bird_dog_supported_split_squat",
                    0.9,
                    "Back-safe lower-body options selected.",
                )
            ],
            condition_descriptions=[
                "back_risk_level is present",
            ],
            action_descriptions=[
                "Set back_safe_lower_body_options = glute_bridge_bird_dog_supported_split_squat",
            ],
            certainty_factor=0.9,
            explanation="Back-safe substitutions reduce heavy spinal loading and emphasize controlled stability.",
        ),

        Rule(
            rule_id="R-SUB-005",
            name="Select back-safe core training style",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("back_risk_level", "present"),
            ],
            actions=[
                add_fact_action(
                    "core_training_style",
                    "anti_extension_and_anti_rotation_core",
                    0.9,
                    "Back-safe core training style selected.",
                )
            ],
            condition_descriptions=[
                "back_risk_level is present",
            ],
            action_descriptions=[
                "Set core_training_style = anti_extension_and_anti_rotation_core",
            ],
            certainty_factor=0.9,
            explanation="Anti-extension and anti-rotation core work can build trunk stability without repeated spinal flexion.",
        ),

        Rule(
            rule_id="R-SUB-006",
            name="Avoid loaded hip hinges when back risk exists",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("back_risk_level", "present"),
            ],
            actions=[
                add_fact_action(
                    "avoid_loaded_hinges",
                    True,
                    0.85,
                    "Back risk requires avoiding heavy loaded hinges.",
                )
            ],
            condition_descriptions=[
                "back_risk_level is present",
            ],
            action_descriptions=[
                "Set avoid_loaded_hinges = True",
            ],
            certainty_factor=0.85,
            explanation="Heavy loaded hinges may aggravate lower-back symptoms if tolerance is limited.",
        ),

        Rule(
            rule_id="R-SUB-007",
            name="Select shoulder-safe pressing options",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("shoulder_risk_level", "present"),
            ],
            actions=[
                add_fact_action(
                    "shoulder_safe_pressing_options",
                    "neutral_grip_press_floor_pushup_landmine_if_available",
                    0.88,
                    "Shoulder-safe pressing options selected.",
                )
            ],
            condition_descriptions=[
                "shoulder_risk_level is present",
            ],
            action_descriptions=[
                "Set shoulder_safe_pressing_options = neutral_grip_press_floor_pushup_landmine_if_available",
            ],
            certainty_factor=0.88,
            explanation="Neutral-grip and reduced-range pressing options are often more shoulder-friendly than painful overhead pressing.",
        ),

        Rule(
            rule_id="R-SUB-008",
            name="Prioritize pulling balance for shoulder risk",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("shoulder_risk_level", "present"),
            ],
            actions=[
                add_fact_action(
                    "upper_body_balance_priority",
                    "rows_rear_delts_scapular_control",
                    0.85,
                    "Shoulder risk requires upper-body pulling and scapular control priority.",
                )
            ],
            condition_descriptions=[
                "shoulder_risk_level is present",
            ],
            action_descriptions=[
                "Set upper_body_balance_priority = rows_rear_delts_scapular_control",
            ],
            certainty_factor=0.85,
            explanation="Rows, rear-delt work, and scapular control can support shoulder-friendly upper-body programming.",
        ),

        Rule(
            rule_id="R-SUB-009",
            name="Avoid upright rows for shoulder risk",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("shoulder_risk_level", "present"),
            ],
            actions=[
                add_fact_action(
                    "avoid_upright_rows",
                    True,
                    0.85,
                    "Shoulder risk requires avoiding upright rows.",
                )
            ],
            condition_descriptions=[
                "shoulder_risk_level is present",
            ],
            action_descriptions=[
                "Set avoid_upright_rows = True",
            ],
            certainty_factor=0.85,
            explanation="Upright rows can place the shoulder in a position that may be uncomfortable for users with shoulder limitations.",
        ),

        # ============================================================
        # CARDIO AND CONDITIONING RULES
        # ============================================================

        Rule(
            rule_id="R-CAR-001",
            name="Assign low-impact fat-loss cardio frequency",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("conditioning_style", "low_impact_fat_loss"),
            ],
            actions=[
                add_fact_action(
                    "cardio_frequency",
                    "3_to_4_low_impact_sessions_per_week",
                    0.85,
                    "Low-impact fat-loss conditioning selected.",
                )
            ],
            condition_descriptions=[
                "conditioning_style is low_impact_fat_loss",
            ],
            action_descriptions=[
                "Set cardio_frequency = 3_to_4_low_impact_sessions_per_week",
            ],
            certainty_factor=0.85,
            explanation="Low-impact cardio several times per week supports fat loss while limiting joint stress.",
        ),

        Rule(
            rule_id="R-CAR-002",
            name="Assign endurance cardio frequency",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["program_direction"],
            conditions=[
                fact_equals("goal_direction", "endurance_focused"),
                fact_equals("condition_none", True),
            ],
            actions=[
                add_fact_action(
                    "cardio_frequency",
                    "3_progressive_endurance_sessions_per_week",
                    0.88,
                    "Endurance goal with no medical condition allows progressive cardio frequency.",
                )
            ],
            condition_descriptions=[
                "goal_direction is endurance_focused",
                "condition_none is True",
            ],
            action_descriptions=[
                "Set cardio_frequency = 3_progressive_endurance_sessions_per_week",
            ],
            certainty_factor=0.88,
            explanation="Endurance users without medical caution can progress cardio frequency gradually.",
        ),

        Rule(
            rule_id="R-CAR-003",
            name="Assign controlled cardio for asthma caution",
            category=CATEGORY_MEDICAL_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("cardio_caution_required", True),
            ],
            actions=[
                add_fact_action(
                    "cardio_frequency",
                    "controlled_low_to_moderate_sessions_with_long_warmup",
                    0.9,
                    "Asthma caution requires controlled cardio sessions.",
                )
            ],
            condition_descriptions=[
                "cardio_caution_required is True",
            ],
            action_descriptions=[
                "Set cardio_frequency = controlled_low_to_moderate_sessions_with_long_warmup",
            ],
            certainty_factor=0.9,
            explanation="Asthma-related caution should override aggressive cardio prescriptions.",
        ),

        Rule(
            rule_id="R-CAR-004",
            name="Avoid jump-based HIIT when high impact is restricted",
            category=CATEGORY_INJURY_SAFETY,
            salience=SALIENCE["injury_safety"],
            conditions=[
                fact_equals("avoid_high_impact", True),
            ],
            actions=[
                add_fact_action(
                    "cardio_avoidance",
                    "avoid_jump_based_hiit_and_sprints",
                    0.9,
                    "High-impact restriction blocks jump-based HIIT and sprinting.",
                )
            ],
            condition_descriptions=[
                "avoid_high_impact is True",
            ],
            action_descriptions=[
                "Set cardio_avoidance = avoid_jump_based_hiit_and_sprints",
            ],
            certainty_factor=0.9,
            explanation="When impact is restricted, conditioning should avoid jumps, sprints, and aggressive plyometrics.",
        ),

        # ============================================================
        # FINAL PROGRAM TYPE RULES
        # ============================================================

        Rule(
            rule_id="R-FIN-001",
            name="Finalize beginner low-impact fat-loss plan",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["finalization"],
            conditions=[
                fact_equals("goal_direction", "fat_loss_focused"),
                fact_equals("experience_level", "beginner"),
                fact_equals("training_split", "upper_lower"),
                fact_equals("conditioning_style", "low_impact_fat_loss"),
            ],
            actions=[
                add_fact_action(
                    "final_program_type",
                    "beginner_4_day_low_impact_fat_loss",
                    0.9,
                    "Beginner four-day low-impact fat-loss plan finalized.",
                )
            ],
            condition_descriptions=[
                "goal_direction is fat_loss_focused",
                "experience_level is beginner",
                "training_split is upper_lower",
                "conditioning_style is low_impact_fat_loss",
            ],
            action_descriptions=[
                "Set final_program_type = beginner_4_day_low_impact_fat_loss",
            ],
            certainty_factor=0.9,
            explanation="The final plan combines beginner status, fat-loss goal, four-day availability, and joint-friendly conditioning.",
        ),

        Rule(
            rule_id="R-FIN-002",
            name="Finalize beginner strength foundation plan",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["finalization"],
            conditions=[
                fact_equals("goal_direction", "strength_focused"),
                fact_equals("experience_level", "beginner"),
                fact_equals("needs_technique_focus", True),
            ],
            actions=[
                add_fact_action(
                    "final_program_type",
                    "beginner_strength_foundation",
                    0.88,
                    "Beginner strength foundation plan finalized.",
                )
            ],
            condition_descriptions=[
                "goal_direction is strength_focused",
                "experience_level is beginner",
                "needs_technique_focus is True",
            ],
            action_descriptions=[
                "Set final_program_type = beginner_strength_foundation",
            ],
            certainty_factor=0.88,
            explanation="Beginner strength users should follow a foundation plan focused on technique and gradual loading.",
        ),

        Rule(
            rule_id="R-FIN-003",
            name="Finalize dumbbell hypertrophy split",
            category=CATEGORY_PROGRAM_DIRECTION,
            salience=SALIENCE["finalization"],
            conditions=[
                fact_equals("goal_direction", "hypertrophy_focused"),
                fact_equals("equipment_level", "limited_weights"),
                fact_equals("training_split", "upper_lower"),
            ],
            actions=[
                add_fact_action(
                    "final_program_type",
                    "dumbbell_upper_lower_hypertrophy",
                    0.86,
                    "Dumbbell upper/lower hypertrophy plan finalized.",
                )
            ],
            condition_descriptions=[
                "goal_direction is hypertrophy_focused",
                "equipment_level is limited_weights",
                "training_split is upper_lower",
            ],
            action_descriptions=[
                "Set final_program_type = dumbbell_upper_lower_hypertrophy",
            ],
            certainty_factor=0.86,
            explanation="A four-day upper/lower split works well for dumbbell-based muscle gain training.",
        ),

        Rule(
            rule_id="R-FIN-004",
            name="Finalize medical-clearance-first plan",
            category=CATEGORY_MEDICAL_SAFETY,
            salience=SALIENCE["medical_red_flag"],
            conditions=[
                fact_equals("medical_clearance_required", True),
            ],
            actions=[
                add_fact_action(
                    "final_program_type",
                    "medical_clearance_required_before_plan",
                    0.95,
                    "Severe issue detected, so medical clearance is required before a normal plan.",
                )
            ],
            condition_descriptions=[
                "medical_clearance_required is True",
            ],
            action_descriptions=[
                "Set final_program_type = medical_clearance_required_before_plan",
            ],
            certainty_factor=0.95,
            explanation="When severe injury risk exists, safety overrides the normal workout plan generation.",
        ),

    ]

    return rules