from engine.inference_engine import InferenceEngine
from knowledge_base.rules import get_rules
from models.user_profile import UserProfile
from services.profile_analyzer import ProfileAnalyzer
from services.workout_generator import WorkoutGenerator


def print_recommendation(recommendation):
    print("\n========== WORKOUT RECOMMENDATION ==========")
    print(f"Program Title: {recommendation.program_title}")
    print(f"Training Split: {recommendation.training_split}")
    print(f"Weekly Days: {recommendation.weekly_days}")

    print("\n========== WORKOUT DAYS ==========")
    for workout_day in recommendation.workout_days:
        print(f"\n{workout_day.day_name}: {workout_day.focus}")

        if not workout_day.exercises:
            print("  No exercises assigned because safety clearance is required.")
            continue

        for exercise in workout_day.exercises:
            print(
                f"  - {exercise.name} | "
                f"{exercise.sets} sets | "
                f"{exercise.reps} | "
                f"CF={exercise.certainty}"
            )
            if exercise.notes:
                print(f"    Note: {exercise.notes}")

    print("\n========== SAFETY NOTES ==========")
    for note in recommendation.safety_notes:
        print(f"- {note}")

    print("\n========== PROGRESSION NOTES ==========")
    for note in recommendation.progression_notes:
        print(f"- {note}")


def main():
    profile = UserProfile(
        age=22,
        height_cm=170,
        weight_kg=78,
        goal="fat_loss",
        experience_level="beginner",
        available_days=4,
        equipment="home_dumbbells",
        injuries={
            "knee": "mild",
        },
        medical_conditions=[],
    )

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

    print("\n========== FITEXPERT ENGINE TEST ==========")
    print(f"Total rules loaded: {len(rules)}")
    print(f"Total rules fired: {len(explanation.fired_rules)}")

    print("\n========== FINAL FACTS ==========")
    for fact in final_facts.all_facts():
        print(
            f"{fact.name} = {fact.value} "
            f"(CF={fact.certainty}, source={fact.source_rule})"
        )

    print_recommendation(recommendation)

    print("\n========== REASONING CHAIN ==========")
    print(explanation.format_reasoning_chain())


if __name__ == "__main__":
    main()