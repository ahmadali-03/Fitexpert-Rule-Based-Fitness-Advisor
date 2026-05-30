from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime

import streamlit as st

from engine.inference_engine import InferenceEngine
from knowledge_base.rules import get_rules
from models.user_profile import UserProfile
from services.profile_analyzer import ProfileAnalyzer
from services.workout_generator import WorkoutGenerator


def readable_label(value: str) -> str:
    return value.replace("_", " ").title()


def build_user_profile() -> UserProfile:
    st.sidebar.header("User Profile")

    age = st.sidebar.number_input(
        "Age",
        min_value=10,
        max_value=100,
        value=22,
        step=1,
    )

    height_cm = st.sidebar.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=230.0,
        value=170.0,
        step=1.0,
    )

    weight_kg = st.sidebar.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=250.0,
        value=78.0,
        step=1.0,
    )

    goal_options = {
        "Strength": "strength",
        "Muscle Gain": "muscle_gain",
        "Fat Loss": "fat_loss",
        "Endurance": "endurance",
        "Flexibility": "flexibility",
    }

    experience_options = {
        "Beginner": "beginner",
        "Intermediate": "intermediate",
        "Advanced": "advanced",
    }

    equipment_options = {
        "Full Gym": "full_gym",
        "Home with Dumbbells": "home_dumbbells",
        "Bodyweight Only": "bodyweight_only",
    }

    goal_label = st.sidebar.selectbox(
        "Primary Fitness Goal",
        list(goal_options.keys()),
        index=2,
    )

    experience_label = st.sidebar.selectbox(
        "Experience Level",
        list(experience_options.keys()),
        index=0,
    )

    available_days = st.sidebar.slider(
        "Available Training Days per Week",
        min_value=1,
        max_value=7,
        value=4,
    )

    equipment_label = st.sidebar.selectbox(
        "Workout Location / Equipment",
        list(equipment_options.keys()),
        index=1,
    )

    st.sidebar.header("Injuries & Medical Conditions")

    injury_severity_options = ["none", "mild", "moderate", "severe"]

    knee = st.sidebar.selectbox(
        "Knee Issue",
        injury_severity_options,
        index=1,
    )

    lower_back = st.sidebar.selectbox(
        "Lower Back Issue",
        injury_severity_options,
        index=0,
    )

    shoulder = st.sidebar.selectbox(
        "Shoulder Issue",
        injury_severity_options,
        index=0,
    )

    asthma = st.sidebar.checkbox("Asthma", value=False)

    injuries: dict[str, str] = {}

    if knee != "none":
        injuries["knee"] = knee

    if lower_back != "none":
        injuries["lower_back"] = lower_back

    if shoulder != "none":
        injuries["shoulder"] = shoulder

    medical_conditions: list[str] = []

    if asthma:
        medical_conditions.append("asthma")

    return UserProfile(
        age=int(age),
        height_cm=float(height_cm),
        weight_kg=float(weight_kg),
        goal=goal_options[goal_label],
        experience_level=experience_options[experience_label],
        available_days=int(available_days),
        equipment=equipment_options[equipment_label],
        injuries=injuries,
        medical_conditions=medical_conditions,
    )


def run_expert_system(profile: UserProfile):
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
        "rules": rules,
        "facts": final_facts,
        "explanation": explanation,
        "recommendation": recommendation,
    }


def display_summary(result) -> None:
    facts = result["facts"]
    explanation = result["explanation"]
    recommendation = result["recommendation"]
    rules = result["rules"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rules Loaded", len(rules))

    with col2:
        st.metric("Rules Fired", len(explanation.fired_rules))

    with col3:
        st.metric("BMI", facts.get("bmi", "N/A"))

    with col4:
        st.metric("Training Days", facts.get("available_days", "N/A"))

    st.subheader(recommendation.program_title)

    st.write(f"**Training Split:** {readable_label(recommendation.training_split)}")
    st.write(f"**Weekly Days:** {recommendation.weekly_days}")

    final_program_type = facts.get("final_program_type")

    if final_program_type:
        st.info(f"Final inferred program type: `{final_program_type}`")


def display_workout_plan(result) -> None:
    recommendation = result["recommendation"]

    st.header("Workout Plan")

    for workout_day in recommendation.workout_days:
        with st.expander(
            f"{workout_day.day_name}: {workout_day.focus}",
            expanded=True,
        ):
            if not workout_day.exercises:
                st.warning(
                    "No exercises assigned because safety clearance is required first."
                )
                continue

            for exercise in workout_day.exercises:
                st.markdown(
                    f"""
                    **{exercise.name}**  
                    Category: `{exercise.category}`  
                    Sets: **{exercise.sets}**  
                    Reps / Duration: **{exercise.reps}**  
                    Exercise CF: **{exercise.certainty}**
                    """
                )

                if exercise.notes:
                    st.caption(exercise.notes)

                st.divider()

    st.subheader("Safety Notes")

    for note in recommendation.safety_notes:
        st.warning(note)

    st.subheader("Progression Notes")

    for note in recommendation.progression_notes:
        st.success(note)


def display_reasoning(result) -> None:
    explanation = result["explanation"]

    st.header("Explainable Reasoning Chain")

    st.write(
        "These are the rules that fired during forward chaining, shown in firing order."
    )

    for index, trace in enumerate(explanation.fired_rules, start=1):
        with st.expander(
            f"{index}. {trace.rule_id}: {trace.rule_name}",
            expanded=False,
        ):
            st.write(f"**Category:** {trace.category}")
            st.write(f"**Priority / Salience:** {trace.salience}")
            st.write(f"**Certainty Factor:** {trace.certainty_factor}")

            st.write("**IF Conditions:**")
            for condition in trace.conditions:
                st.write(f"- {condition}")

            st.write("**THEN Actions:**")
            for action in trace.actions:
                st.write(f"- {action}")

            if trace.created_facts:
                st.write("**Created / Updated Facts:**")
                for fact in trace.created_facts:
                    st.code(fact)

            st.write("**Explanation:**")
            st.info(trace.explanation)


def display_facts(result) -> None:
    facts = result["facts"]

    st.header("Working Memory / Final Facts")

    fact_rows = []

    for fact in facts.all_facts():
        fact_rows.append(
            {
                "Fact": fact.name,
                "Value": fact.value,
                "Certainty": fact.certainty,
                "Source": fact.source_rule,
                "Explanation": fact.explanation,
            }
        )

    st.dataframe(fact_rows, use_container_width=True)


def display_rule_table(result) -> None:
    rules = result["rules"]

    st.header("Knowledge Base Rules")

    rule_rows = []

    for rule in rules:
        rule_rows.append(
            {
                "Rule ID": rule.rule_id,
                "Name": rule.name,
                "Category": rule.category,
                "Salience": rule.salience,
                "CF": rule.certainty_factor,
                "IF": " | ".join(rule.condition_descriptions),
                "THEN": " | ".join(rule.action_descriptions),
                "Explanation": rule.explanation,
            }
        )

    st.dataframe(rule_rows, use_container_width=True)


def build_export_data(profile: UserProfile, result) -> dict:
    facts = result["facts"]
    explanation = result["explanation"]
    recommendation = result["recommendation"]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "profile": asdict(profile),
        "recommendation": asdict(recommendation),
        "final_facts": [
            {
                "name": fact.name,
                "value": fact.value,
                "certainty": fact.certainty,
                "source_rule": fact.source_rule,
                "explanation": fact.explanation,
            }
            for fact in facts.all_facts()
        ],
        "fired_rules": [
            {
                "rule_id": trace.rule_id,
                "rule_name": trace.rule_name,
                "category": trace.category,
                "salience": trace.salience,
                "certainty_factor": trace.certainty_factor,
                "conditions": trace.conditions,
                "actions": trace.actions,
                "created_facts": trace.created_facts,
                "explanation": trace.explanation,
            }
            for trace in explanation.fired_rules
        ],
    }


def build_text_plan(profile: UserProfile, result) -> str:
    recommendation = result["recommendation"]
    facts = result["facts"]
    explanation = result["explanation"]

    lines: list[str] = []

    lines.append("FITEXPERT WORKOUT PLAN")
    lines.append("=" * 60)
    lines.append(f"Generated At: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")

    lines.append("USER PROFILE")
    lines.append("-" * 60)
    lines.append(f"Age: {profile.age}")
    lines.append(f"Height: {profile.height_cm} cm")
    lines.append(f"Weight: {profile.weight_kg} kg")
    lines.append(f"BMI: {facts.get('bmi')}")
    lines.append(f"Goal: {profile.goal}")
    lines.append(f"Experience: {profile.experience_level}")
    lines.append(f"Available Days: {profile.available_days}")
    lines.append(f"Equipment: {profile.equipment}")
    lines.append(f"Injuries: {profile.injuries if profile.injuries else 'None'}")
    lines.append(
        f"Medical Conditions: "
        f"{profile.medical_conditions if profile.medical_conditions else 'None'}"
    )
    lines.append("")

    lines.append("RECOMMENDATION")
    lines.append("-" * 60)
    lines.append(f"Program Title: {recommendation.program_title}")
    lines.append(f"Training Split: {recommendation.training_split}")
    lines.append(f"Weekly Days: {recommendation.weekly_days}")
    lines.append("")

    lines.append("WORKOUT DAYS")
    lines.append("-" * 60)

    for workout_day in recommendation.workout_days:
        lines.append(f"{workout_day.day_name}: {workout_day.focus}")

        if not workout_day.exercises:
            lines.append("  No exercises assigned because safety clearance is required.")
            lines.append("")
            continue

        for exercise in workout_day.exercises:
            lines.append(
                f"  - {exercise.name}: {exercise.sets} sets, "
                f"{exercise.reps}, CF={exercise.certainty}"
            )

            if exercise.notes:
                lines.append(f"    Note: {exercise.notes}")

        lines.append("")

    lines.append("SAFETY NOTES")
    lines.append("-" * 60)
    for note in recommendation.safety_notes:
        lines.append(f"- {note}")

    lines.append("")

    lines.append("PROGRESSION NOTES")
    lines.append("-" * 60)
    for note in recommendation.progression_notes:
        lines.append(f"- {note}")

    lines.append("")

    lines.append("REASONING CHAIN")
    lines.append("-" * 60)
    lines.append(explanation.format_reasoning_chain())

    return "\n".join(lines)


def display_export(profile: UserProfile, result) -> None:
    st.header("Save Generated Plan")

    st.write(
        "FitExpert does not permanently store users. "
        "Use these buttons to save the generated plan manually."
    )

    export_data = build_export_data(profile, result)
    json_data = json.dumps(export_data, indent=4, ensure_ascii=False)

    text_plan = build_text_plan(profile, result)

    st.download_button(
        label="Download Plan as JSON",
        data=json_data,
        file_name="fitexpert_plan.json",
        mime="application/json",
    )

    st.download_button(
        label="Download Plan as Text",
        data=text_plan,
        file_name="fitexpert_plan.txt",
        mime="text/plain",
    )


def main() -> None:
    st.set_page_config(
        page_title="FitExpert",
        page_icon="🏋️",
        layout="wide",
    )

    st.title("🏋️ FitExpert")
    st.caption("Rule-Based Fitness & Exercise Advisor Expert System")

    st.markdown(
        """
        FitExpert uses a custom forward-chaining inference engine with a separate
        knowledge base, conflict resolution strategy, certainty factors, and an
        explainable reasoning chain.
        """
    )

    profile = build_user_profile()

    if st.sidebar.button("Generate Expert Recommendation", type="primary"):
        try:
            st.session_state["profile"] = profile
            st.session_state["result"] = run_expert_system(profile)

        except Exception as error:
            st.error(f"Could not generate recommendation: {error}")

    if "result" not in st.session_state:
        st.info("Enter user details in the sidebar, then click **Generate Expert Recommendation**.")
        return

    result = st.session_state["result"]
    saved_profile = st.session_state["profile"]

    display_summary(result)

    tab_plan, tab_reasoning, tab_facts, tab_rules, tab_export = st.tabs(
        [
            "Workout Plan",
            "Reasoning Chain",
            "Final Facts",
            "Rule Base",
            "Save Plan",
        ]
    )

    with tab_plan:
        display_workout_plan(result)

    with tab_reasoning:
        display_reasoning(result)

    with tab_facts:
        display_facts(result)

    with tab_rules:
        display_rule_table(result)

    with tab_export:
        display_export(saved_profile, result)


if __name__ == "__main__":
    main()