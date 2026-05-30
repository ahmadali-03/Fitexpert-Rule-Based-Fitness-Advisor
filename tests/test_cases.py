from __future__ import annotations

from engine.inference_engine import InferenceEngine
from knowledge_base.rules import get_rules
from services.profile_analyzer import ProfileAnalyzer
from services.workout_generator import WorkoutGenerator
from tests.sample_profiles import get_sample_profiles


def run_single_test_case(case_name, profile):
    analyzer = ProfileAnalyzer()
    facts = analyzer.create_initial_facts(profile)

    rules = get_rules()
    engine = InferenceEngine(rules=rules)

    final_facts, explanation = engine.run(facts)

    generator = WorkoutGenerator()
    recommendation = generator.generate(
        final_facts,
        reasoning_summary=explanation.format_reasoning_chain(),
    )

    return {
        "case_name": case_name,
        "profile": profile,
        "rule_count": len(rules),
        "fired_rule_count": len(explanation.fired_rules),
        "final_facts": final_facts,
        "recommendation": recommendation,
        "explanation": explanation,
    }


def print_test_result(result):
    final_facts = result["final_facts"]
    recommendation = result["recommendation"]
    explanation = result["explanation"]

    print("\n" + "=" * 90)
    print(result["case_name"])
    print("=" * 90)

    print(f"Rules loaded: {result['rule_count']}")
    print(f"Rules fired: {result['fired_rule_count']}")

    print("\nKey inferred facts:")
    key_facts = [
        "age_group",
        "bmi_category",
        "goal_direction",
        "training_split",
        "training_volume",
        "set_scheme",
        "rep_range",
        "intensity_profile",
        "equipment_level",
        "exercise_selection_style",
        "needs_low_impact_training",
        "needs_knee_safe_training",
        "avoid_high_impact",
        "avoid_overhead_pressing",
        "avoid_heavy_spinal_loading",
        "cardio_caution_required",
        "medical_clearance_required",
        "final_program_type",
    ]

    for fact_name in key_facts:
        if final_facts.has(fact_name):
            print(
                f"- {fact_name}: {final_facts.get(fact_name)} "
                f"(CF={final_facts.get_certainty(fact_name)})"
            )

    print("\nRecommendation summary:")
    print(f"- Program: {recommendation.program_title}")
    print(f"- Split: {recommendation.training_split}")
    print(f"- Weekly days: {recommendation.weekly_days}")

    print("\nSafety notes:")
    for note in recommendation.safety_notes:
        print(f"- {note}")

    print("\nFirst 5 fired rules:")
    for trace in explanation.fired_rules[:5]:
        print(f"- {trace.rule_id}: {trace.rule_name} | salience={trace.salience}")


def run_all_test_cases():
    profiles = get_sample_profiles()

    results = []

    for case_name, profile in profiles:
        result = run_single_test_case(case_name, profile)
        results.append(result)
        print_test_result(result)

    print("\n" + "=" * 90)
    print("TESTING COMPLETE")
    print("=" * 90)
    print(f"Total scenarios tested: {len(results)}")

    return results


if __name__ == "__main__":
    run_all_test_cases()