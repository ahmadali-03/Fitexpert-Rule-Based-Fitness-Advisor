from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from io import BytesIO

import streamlit as st

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from engine.inference_engine import InferenceEngine
from knowledge_base.rules import get_rules
from models.user_profile import UserProfile
from services.profile_analyzer import ProfileAnalyzer
from services.workout_generator import WorkoutGenerator


st.set_page_config(
    page_title="FitExpert",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(124, 58, 237, 0.20), transparent 32%),
                radial-gradient(circle at top right, rgba(37, 99, 235, 0.16), transparent 30%),
                linear-gradient(135deg, #070b14 0%, #0b1020 44%, #090b12 100%);
            color: #f8fafc;
        }
        header[data-testid="stHeader"] {
            background: rgba(7, 11, 20, 0.96);
            border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        }
        .block-container {
            padding-top: 3.25rem;
            padding-bottom: 2rem;
            padding-left: 2.1rem;
            padding-right: 2.1rem;
            max-width: 1420px;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #090e1a 0%, #101827 58%, #080c14 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.14);
        }
        [data-testid="stSidebar"] * { color: #e5e7eb; }
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #e5e7eb !important;
        }
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stNumberInput,
        [data-testid="stSidebar"] .stSlider,
        [data-testid="stSidebar"] .stCheckbox {
            margin-bottom: 0.45rem;
        }
        h1, h2, h3 { color: #f8fafc !important; letter-spacing: -0.02em; }
        p, li, span, label { color: #dbe4ef; }
        .stButton > button {
            width: 100%;
            border-radius: 14px;
            border: 1px solid rgba(168, 85, 247, 0.55);
            background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
            color: white;
            font-weight: 800;
            padding: 0.72rem 1rem;
            box-shadow: 0 12px 34px rgba(79, 70, 229, 0.30);
        }
        .stButton > button:hover {
            border-color: rgba(216, 180, 254, 0.95);
            box-shadow: 0 16px 40px rgba(124, 58, 237, 0.40);
        }
        .stDownloadButton > button {
            border-radius: 14px;
            background: rgba(15, 23, 42, 0.88);
            color: #f8fafc;
            border: 1px solid rgba(148, 163, 184, 0.25);
            font-weight: 800;
            padding: 0.7rem 1rem;
            width: 100%;
        }
        div[data-testid="stTabs"] {
            margin-top: 0.5rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
            padding: 10px;
            margin-bottom: 1.35rem;
            overflow-x: auto;
        }
        .stTabs [data-baseweb="tab"] {
            min-height: 46px;
            border-radius: 14px;
            color: #dbe4ef !important;
            font-weight: 850;
            padding: 0 18px;
            background: rgba(30, 41, 59, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.08);
        }
        .stTabs [data-baseweb="tab"] p {
            color: #dbe4ef !important;
            font-weight: 850 !important;
            font-size: 0.98rem;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.98), rgba(37, 99, 235, 0.98)) !important;
            color: white !important;
            border-color: rgba(216, 180, 254, 0.38);
            box-shadow: 0 10px 24px rgba(79, 70, 229, 0.28);
        }
        .stTabs [aria-selected="true"] p {
            color: white !important;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            display: none;
        }
        div[data-testid="stExpander"] {
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 16px;
            background: rgba(15, 23, 42, 0.38);
            overflow: hidden;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.16);
        }
        div[data-testid="stAlert"] {
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.18);
        }
        .logo-box {
            background: rgba(124, 58, 237, 0.16);
            border: 1px solid rgba(167, 139, 250, 0.24);
            border-radius: 20px;
            padding: 14px 16px;
            margin-bottom: 1rem;
            text-align: center;
        }
        .logo-main { color: #ffffff; font-weight: 950; font-size: 1.55rem; }
        .logo-sub {
            color: #a78bfa;
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            margin-top: 2px;
        }
        .hero-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.72));
            border: 1px solid rgba(148, 163, 184, 0.17);
            border-radius: 26px;
            padding: 28px 30px;
            box-shadow: 0 22px 70px rgba(0, 0, 0, 0.35);
            margin-bottom: 1.1rem;
        }
        .hero-eyebrow {
            color: #a78bfa;
            text-transform: uppercase;
            font-size: 0.82rem;
            letter-spacing: 0.16em;
            font-weight: 850;
            margin-bottom: 0.35rem;
        }
        .hero-title { font-size: 2.45rem; line-height: 1.05; font-weight: 950; color: #ffffff; margin: 0; }
        .hero-title span {
            background: linear-gradient(135deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle { margin-top: 0.85rem; color: #cbd5e1; font-size: 1.02rem; max-width: 920px; }
        .metric-card {
            background: rgba(15, 23, 42, 0.76);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 20px;
            padding: 18px 18px;
            box-shadow: 0 14px 45px rgba(0, 0, 0, 0.22);
            min-height: 118px;
        }
        .metric-icon {
            width: 38px;
            height: 38px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.28), rgba(37, 99, 235, 0.24));
            border: 1px solid rgba(167, 139, 250, 0.28);
            border-radius: 12px;
            font-size: 1.2rem;
            margin-bottom: 12px;
        }
        .metric-label {
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 5px;
        }
        .metric-value { color: #f8fafc; font-size: 1.08rem; font-weight: 900; }
        .glass-card {
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 22px;
            padding: 22px;
            box-shadow: 0 16px 55px rgba(0, 0, 0, 0.24);
            margin-bottom: 1rem;
        }
        .section-title { color: #f8fafc; font-size: 1.18rem; font-weight: 900; margin-bottom: 16px; }
        .summary-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 11px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        }
        .summary-row:last-child { border-bottom: none; }
        .summary-key { color: #94a3b8; font-weight: 700; font-size: 0.92rem; }
        .summary-value { color: #f8fafc; font-weight: 900; font-size: 0.94rem; text-align: right; }
        .pill {
            display: inline-flex;
            align-items: center;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(251, 146, 60, 0.14);
            border: 1px solid rgba(251, 146, 60, 0.24);
            color: #fdba74;
            font-weight: 850;
            font-size: 0.8rem;
        }
        .good-pill { background: rgba(34, 197, 94, 0.13); border: 1px solid rgba(34, 197, 94, 0.25); color: #86efac; }
        .confidence-ring {
            width: 176px;
            height: 176px;
            border-radius: 50%;
            margin: 12px auto 12px auto;
            background: radial-gradient(circle at center, #0f172a 0 58%, transparent 59%),
                        conic-gradient(from 180deg, #8b5cf6 0deg, #3b82f6 235deg, rgba(148, 163, 184, 0.18) 235deg 360deg);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 42px rgba(124, 58, 237, 0.24);
        }
        .confidence-number { font-size: 2.3rem; font-weight: 950; color: white; line-height: 1; }
        .confidence-label { text-align: center; color: #94a3b8; font-weight: 750; font-size: 0.86rem; margin-top: 5px; }
        .overview-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
            margin-top: 1rem;
        }
        .overview-card {
            background: rgba(15, 23, 42, 0.66);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 18px;
            padding: 16px;
            min-height: 116px;
        }
        .overview-card-icon { font-size: 1.4rem; margin-bottom: 10px; }
        .overview-card-label { color: #94a3b8; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; }
        .overview-card-value { color: #f8fafc; font-weight: 900; font-size: 1rem; margin-top: 4px; }
        .banner {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.24), rgba(37, 99, 235, 0.18));
            border: 1px solid rgba(167, 139, 250, 0.24);
            border-radius: 18px;
            padding: 16px 18px;
            color: #e9d5ff;
            margin-top: 1rem;
            font-weight: 700;
        }
        .workout-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 18px;
            padding: 17px;
            margin-bottom: 12px;
        }
        .exercise-title { color: #ffffff; font-weight: 900; font-size: 1rem; }
        .exercise-meta { color: #cbd5e1; font-size: 0.88rem; margin-top: 4px; }
        .exercise-note { color: #94a3b8; font-size: 0.84rem; margin-top: 8px; }
        @media (max-width: 900px) {
            .overview-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .hero-title { font-size: 2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def readable_label(value: object) -> str:
    if value is None:
        return "Not inferred"
    return str(value).replace("_", " ").title()


def get_bmi_badge(bmi_category: str | None) -> str:
    if not bmi_category:
        return '<span class="pill">Unknown</span>'
    if bmi_category == "normal":
        return '<span class="pill good-pill">Normal</span>'
    return f'<span class="pill">{readable_label(bmi_category)}</span>'


def safe_fact(facts, name: str, default: str = "Not inferred") -> str:
    value = facts.get(name, default)
    return readable_label(value)


def estimate_plan_confidence(facts) -> int:
    important_facts = [
        "final_program_type",
        "goal_direction",
        "training_split",
        "training_volume",
        "intensity_profile",
        "set_scheme",
        "rep_range",
    ]
    certainties = [float(facts.get_certainty(name)) for name in important_facts if facts.has(name)]
    if not certainties:
        return 75
    return max(60, min(98, round(sum(certainties) / len(certainties) * 100)))


def build_user_profile() -> UserProfile:
    st.sidebar.markdown(
        """
        <div class="logo-box">
            <div class="logo-main">🏋️ FitExpert</div>
            <div class="logo-sub">AI Fitness Advisor</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.subheader("Profile Input")

    age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=22, step=1)
    height_cm = st.sidebar.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=170.0, step=1.0)
    weight_kg = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=78.0, step=1.0)

    goal_options = {
        "Fat Loss": "fat_loss",
        "Strength": "strength",
        "Muscle Gain": "muscle_gain",
        "Endurance": "endurance",
        "Flexibility": "flexibility",
    }
    experience_options = {"Beginner": "beginner", "Intermediate": "intermediate", "Advanced": "advanced"}
    equipment_options = {
        "Home with Dumbbells": "home_dumbbells",
        "Full Gym": "full_gym",
        "Bodyweight Only": "bodyweight_only",
    }

    goal_label = st.sidebar.selectbox("Primary Fitness Goal", list(goal_options.keys()), index=0)
    experience_label = st.sidebar.selectbox("Experience Level", list(experience_options.keys()), index=0)
    available_days = st.sidebar.slider("Available Training Days per Week", 1, 7, 4)
    equipment_label = st.sidebar.selectbox("Workout Location / Equipment", list(equipment_options.keys()), index=0)

    st.sidebar.divider()
    st.sidebar.subheader("Injuries & Medical")

    injury_options = ["none", "mild", "moderate", "severe"]
    knee = st.sidebar.selectbox("Knee Issue", injury_options, index=1)
    lower_back = st.sidebar.selectbox("Lower Back Issue", injury_options, index=0)
    shoulder = st.sidebar.selectbox("Shoulder Issue", injury_options, index=0)
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


def run_expert_system(profile: UserProfile) -> dict:
    analyzer = ProfileAnalyzer()
    facts = analyzer.create_initial_facts(profile)

    rules = get_rules()
    engine = InferenceEngine(rules=rules)
    final_facts, explanation = engine.run(facts)

    generator = WorkoutGenerator()
    recommendation = generator.generate(final_facts, reasoning_summary=explanation.format_reasoning_chain())

    return {"rules": rules, "facts": final_facts, "explanation": explanation, "recommendation": recommendation}


def display_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-eyebrow">Rule-Based Expert System</div>
            <div class="hero-title">Welcome to <span>FitExpert</span></div>
            <div class="hero-subtitle">
                A dark professional dashboard for personalized fitness recommendations using
                forward chaining, certainty factors, conflict resolution, and explainable AI reasoning.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_top_metric_cards(profile: UserProfile) -> None:
    columns = st.columns(4)
    cards = [
        ("🎯", "Goal", readable_label(profile.goal)),
        ("👤", "Experience", readable_label(profile.experience_level)),
        ("📅", "Days / Week", f"{profile.available_days} Days"),
        ("🏋️", "Equipment", readable_label(profile.equipment)),
    ]
    for column, (icon, label, value) in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def display_dashboard(result: dict, profile: UserProfile) -> None:
    facts = result["facts"]
    recommendation = result["recommendation"]
    explanation = result["explanation"]
    rules = result["rules"]
    confidence = estimate_plan_confidence(facts)

    display_hero()
    display_top_metric_cards(profile)
    st.write("")

    left, right = st.columns([1.25, 0.85])
    injury_text = "None"
    if profile.injuries:
        injury_text = ", ".join(f"{readable_label(name)} ({readable_label(level)})" for name, level in profile.injuries.items())

    with left:
        bmi_badge = get_bmi_badge(facts.get("bmi_category"))
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="section-title">Your Summary</div>
                <div class="summary-row"><div class="summary-key">Age</div><div class="summary-value">{profile.age}</div></div>
                <div class="summary-row"><div class="summary-key">BMI</div><div class="summary-value">{facts.get('bmi', 'N/A')} &nbsp; {bmi_badge}</div></div>
                <div class="summary-row"><div class="summary-key">Injury</div><div class="summary-value">{injury_text}</div></div>
                <div class="summary-row"><div class="summary-key">Focus</div><div class="summary-value">{safe_fact(facts, 'goal_direction')}</div></div>
                <div class="summary-row"><div class="summary-key">Training Style</div><div class="summary-value">{safe_fact(facts, 'intensity_profile')}</div></div>
                <div class="summary-row"><div class="summary-key">Rules Fired</div><div class="summary-value">{len(explanation.fired_rules)} / {len(rules)}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="section-title">Recommendation Confidence</div>
                <div class="confidence-ring">
                    <div>
                        <div class="confidence-number">{confidence}%</div>
                        <div class="confidence-label">Confidence</div>
                    </div>
                </div>
                <div style="text-align:center;color:#cbd5e1;font-weight:750;">
                    High confidence in recommended plan
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="overview-grid">
            <div class="overview-card">
                <div class="overview-card-icon">🏋️</div>
                <div class="overview-card-label">Workout Split</div>
                <div class="overview-card-value">{safe_fact(facts, 'training_split')}</div>
            </div>
            <div class="overview-card">
                <div class="overview-card-icon">❤️</div>
                <div class="overview-card-label">Cardio</div>
                <div class="overview-card-value">{safe_fact(facts, 'cardio_frequency')}</div>
            </div>
            <div class="overview-card">
                <div class="overview-card-icon">🎯</div>
                <div class="overview-card-label">Program Type</div>
                <div class="overview-card-value">{safe_fact(facts, 'final_program_type')}</div>
            </div>
            <div class="overview-card">
                <div class="overview-card-icon">📈</div>
                <div class="overview-card-label">Progression</div>
                <div class="overview-card-value">{safe_fact(facts, 'progression_style', 'Gradual Progression')}</div>
            </div>
        </div>
        <div class="banner">
            🛡️ FitExpert uses rule-based reasoning, certainty factors, and safety-first conflict resolution to deliver personalized workout recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="section-title">Recommended Program</div>
            <div style="font-size:1.45rem;font-weight:950;color:#ffffff;">{recommendation.program_title}</div>
            <div style="color:#94a3b8;margin-top:6px;font-weight:700;">
                Split: {readable_label(recommendation.training_split)} &nbsp; • &nbsp; Weekly Days: {recommendation.weekly_days}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_workout_plan(result: dict) -> None:
    recommendation = result["recommendation"]
    st.header("Workout Plan")

    for workout_day in recommendation.workout_days:
        with st.expander(f"{workout_day.day_name}: {workout_day.focus}", expanded=True):
            if not workout_day.exercises:
                st.warning("No exercises assigned because safety clearance is required first.")
                continue
            for exercise in workout_day.exercises:
                st.markdown(
                    f"""
                    <div class="workout-card">
                        <div class="exercise-title">{exercise.name}</div>
                        <div class="exercise-meta">
                            Category: <b>{readable_label(exercise.category)}</b>
                            &nbsp; • &nbsp; Sets: <b>{exercise.sets}</b>
                            &nbsp; • &nbsp; Reps / Duration: <b>{exercise.reps}</b>
                            &nbsp; • &nbsp; CF: <b>{exercise.certainty}</b>
                        </div>
                        <div class="exercise-note">{exercise.notes}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.subheader("Safety Notes")
    for note in recommendation.safety_notes:
        st.warning(note)

    st.subheader("Progression Notes")
    for note in recommendation.progression_notes:
        st.success(note)


def display_reasoning(result: dict) -> None:
    explanation = result["explanation"]
    st.header("Explainable Reasoning Chain")
    st.write("These are the rules that fired during forward chaining, shown in firing order.")

    for index, trace in enumerate(explanation.fired_rules, start=1):
        with st.expander(f"{index}. {trace.rule_id}: {trace.rule_name}", expanded=False):
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


def display_facts(result: dict) -> None:
    facts = result["facts"]
    st.header("Working Memory / Final Facts")
    fact_rows = [
        {
            "Fact": fact.name,
            "Value": fact.value,
            "Certainty": fact.certainty,
            "Source": fact.source_rule,
            "Explanation": fact.explanation,
        }
        for fact in facts.all_facts()
    ]
    st.dataframe(fact_rows, use_container_width=True, hide_index=True)


def display_rule_table(result: dict) -> None:
    rules = result["rules"]
    st.header("Knowledge Base Rules")
    rule_rows = [
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
        for rule in rules
    ]
    st.dataframe(rule_rows, use_container_width=True, hide_index=True)


def build_export_data(profile: UserProfile, result: dict) -> dict:
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


def build_text_plan(profile: UserProfile, result: dict) -> str:
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
    lines.append(f"Medical Conditions: {profile.medical_conditions if profile.medical_conditions else 'None'}")
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
            lines.append(f"  - {exercise.name}: {exercise.sets} sets, {exercise.reps}, CF={exercise.certainty}")
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



def _pdf_safe(value: object) -> str:
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _make_table(data: list[list[object]], column_widths: list[float] | None = None) -> "Table":
    table = Table(data, colWidths=column_widths, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#111827")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def build_pdf_plan(profile: UserProfile, result: dict) -> bytes:
    """
    Build a professional PDF workout plan for the user.

    Requires reportlab. Add reportlab>=4.2.0 to requirements.txt for deployment.
    """
    if not REPORTLAB_AVAILABLE:
        raise RuntimeError("PDF export requires reportlab. Add reportlab>=4.2.0 to requirements.txt")

    facts = result["facts"]
    explanation = result["explanation"]
    recommendation = result["recommendation"]

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title="FitExpert Workout Plan",
    )

    base_styles = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "FitExpertTitle",
            parent=base_styles["Title"],
            textColor=colors.HexColor("#111827"),
            fontSize=22,
            leading=26,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "FitExpertSubtitle",
            parent=base_styles["Normal"],
            textColor=colors.HexColor("#475569"),
            fontSize=10,
            leading=14,
            spaceAfter=14,
        ),
        "heading": ParagraphStyle(
            "FitExpertHeading",
            parent=base_styles["Heading2"],
            textColor=colors.HexColor("#4F46E5"),
            fontSize=14,
            leading=18,
            spaceBefore=10,
            spaceAfter=8,
        ),
        "normal": ParagraphStyle(
            "FitExpertNormal",
            parent=base_styles["Normal"],
            textColor=colors.HexColor("#1F2937"),
            fontSize=9.5,
            leading=13,
        ),
        "small": ParagraphStyle(
            "FitExpertSmall",
            parent=base_styles["Normal"],
            textColor=colors.HexColor("#475569"),
            fontSize=8.3,
            leading=11,
        ),
    }

    story = []

    story.append(Paragraph("FitExpert Workout Recommendation", styles["title"]))
    story.append(
        Paragraph(
            "Rule-Based Fitness & Exercise Advisor | Forward Chaining | Certainty Factors | Explainable Reasoning",
            styles["subtitle"],
        )
    )
    story.append(Paragraph(f"Generated at: {_pdf_safe(datetime.now().isoformat(timespec='seconds'))}", styles["small"]))
    story.append(Spacer(1, 10))

    confidence = estimate_plan_confidence(facts)
    injury_text = "None"
    if profile.injuries:
        injury_text = ", ".join(f"{readable_label(k)} ({readable_label(v)})" for k, v in profile.injuries.items())

    medical_text = ", ".join(profile.medical_conditions) if profile.medical_conditions else "None"

    story.append(Paragraph("1. User Profile Summary", styles["heading"]))
    profile_table = [
        ["Field", "Value"],
        ["Age", _pdf_safe(profile.age)],
        ["Height", f"{profile.height_cm} cm"],
        ["Weight", f"{profile.weight_kg} kg"],
        ["BMI", _pdf_safe(facts.get("bmi", "N/A"))],
        ["BMI Category", _pdf_safe(readable_label(facts.get("bmi_category", "Not inferred")))],
        ["Goal", _pdf_safe(readable_label(profile.goal))],
        ["Experience", _pdf_safe(readable_label(profile.experience_level))],
        ["Available Days", _pdf_safe(profile.available_days)],
        ["Equipment", _pdf_safe(readable_label(profile.equipment))],
        ["Injuries", _pdf_safe(injury_text)],
        ["Medical Conditions", _pdf_safe(medical_text)],
    ]
    story.append(_make_table(profile_table, [1.55 * inch, 4.8 * inch]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Final Recommendation", styles["heading"]))
    recommendation_table = [
        ["Item", "Conclusion"],
        ["Program Title", _pdf_safe(recommendation.program_title)],
        ["Training Split", _pdf_safe(readable_label(recommendation.training_split))],
        ["Weekly Days", _pdf_safe(recommendation.weekly_days)],
        ["Final Program Type", _pdf_safe(readable_label(facts.get("final_program_type", "Not inferred")))],
        ["Plan Confidence", f"{confidence}%"],
        ["Goal Direction", _pdf_safe(readable_label(facts.get("goal_direction", "Not inferred")))],
        ["Intensity Profile", _pdf_safe(readable_label(facts.get("intensity_profile", "Not inferred")))],
        ["Set Scheme", _pdf_safe(readable_label(facts.get("set_scheme", "Not inferred")))],
        ["Rep Range", _pdf_safe(readable_label(facts.get("rep_range", "Not inferred")))],
    ]
    story.append(_make_table(recommendation_table, [1.75 * inch, 4.6 * inch]))

    story.append(Paragraph("3. Workout Plan", styles["heading"]))
    for workout_day in recommendation.workout_days:
        story.append(Paragraph(f"<b>{_pdf_safe(workout_day.day_name)}: {_pdf_safe(workout_day.focus)}</b>", styles["normal"]))

        if not workout_day.exercises:
            story.append(Paragraph("No exercises assigned because safety clearance is required.", styles["normal"]))
            story.append(Spacer(1, 6))
            continue

        workout_table = [["Exercise", "Category", "Sets", "Reps / Duration", "CF"]]
        for exercise in workout_day.exercises:
            workout_table.append(
                [
                    Paragraph(_pdf_safe(exercise.name), styles["small"]),
                    Paragraph(_pdf_safe(readable_label(exercise.category)), styles["small"]),
                    _pdf_safe(exercise.sets),
                    Paragraph(_pdf_safe(exercise.reps), styles["small"]),
                    _pdf_safe(exercise.certainty),
                ]
            )
        story.append(_make_table(workout_table, [2.05 * inch, 1.15 * inch, 0.55 * inch, 1.75 * inch, 0.45 * inch]))
        story.append(Spacer(1, 8))

    story.append(Paragraph("4. Safety Notes", styles["heading"]))
    for note in recommendation.safety_notes:
        story.append(Paragraph(f"• {_pdf_safe(note)}", styles["normal"]))

    story.append(Paragraph("5. Progression Notes", styles["heading"]))
    for note in recommendation.progression_notes:
        story.append(Paragraph(f"• {_pdf_safe(note)}", styles["normal"]))

    story.append(PageBreak())
    story.append(Paragraph("6. Explainable Reasoning Summary", styles["heading"]))
    story.append(
        Paragraph(
            "The following table shows the rules fired by the forward-chaining inference engine. "
            "Rules with higher salience fired earlier, so medical and injury safety logic overrides normal exercise selection.",
            styles["normal"],
        )
    )
    story.append(Spacer(1, 8))

    rule_table = [["#", "Rule ID", "Rule Name", "Category", "Salience", "Created Facts"]]
    for index, trace in enumerate(explanation.fired_rules, start=1):
        rule_table.append(
            [
                str(index),
                _pdf_safe(trace.rule_id),
                Paragraph(_pdf_safe(trace.rule_name), styles["small"]),
                Paragraph(_pdf_safe(trace.category), styles["small"]),
                str(trace.salience),
                Paragraph(_pdf_safe(", ".join(trace.created_facts) if trace.created_facts else "None"), styles["small"]),
            ]
        )
    story.append(_make_table(rule_table, [0.3 * inch, 0.75 * inch, 1.8 * inch, 1.2 * inch, 0.65 * inch, 1.75 * inch]))

    story.append(Paragraph("7. Important Final Facts", styles["heading"]))
    important_fact_names = [
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
    fact_table = [["Fact", "Value", "CF", "Source"]]
    for fact_name in important_fact_names:
        if facts.has(fact_name):
            fact = next(f for f in facts.all_facts() if f.name == fact_name)
            fact_table.append(
                [
                    _pdf_safe(fact.name),
                    Paragraph(_pdf_safe(readable_label(fact.value)), styles["small"]),
                    _pdf_safe(round(float(fact.certainty), 3)),
                    _pdf_safe(fact.source_rule),
                ]
            )
    story.append(_make_table(fact_table, [1.75 * inch, 2.55 * inch, 0.65 * inch, 1.05 * inch]))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def display_export(profile: UserProfile, result: dict) -> None:
    st.header("Save Generated Plan")
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Download Professional PDF</div>
            <div style="color:#cbd5e1;">
                FitExpert does not permanently store users. Download this professional PDF
                if you want to keep or submit the generated recommendation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not REPORTLAB_AVAILABLE:
        st.error(
            "PDF export requires the reportlab package. Add `reportlab>=4.2.0` "
            "to requirements.txt, install it locally, and redeploy the app."
        )
        return

    pdf_data = build_pdf_plan(profile, result)

    st.download_button(
        label="📄 Download Plan as PDF",
        data=pdf_data,
        file_name="fitexpert_workout_plan.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


def main() -> None:
    inject_css()
    profile = build_user_profile()

    if st.sidebar.button("Generate Plan", type="primary"):
        try:
            st.session_state["profile"] = profile
            st.session_state["result"] = run_expert_system(profile)
        except Exception as error:
            st.error(f"Could not generate recommendation: {error}")

    st.sidebar.caption("The app is stateless. It does not permanently store user data.")

    if "result" not in st.session_state:
        display_hero()
        display_top_metric_cards(profile)
        st.markdown(
            """
            <div class="glass-card">
                <div class="section-title">Ready to Generate</div>
                <div style="color:#cbd5e1;font-size:1rem;">
                    Enter user details in the sidebar, then click <b>Generate Plan</b>.
                    FitExpert will run its forward-chaining inference engine and produce a personalized workout recommendation with explainable reasoning.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    result = st.session_state["result"]
    saved_profile = st.session_state["profile"]

    tab_dashboard, tab_plan, tab_reasoning, tab_facts, tab_rules, tab_export = st.tabs(
        ["Dashboard", "Workout Plan", "Reasoning Chain", "Final Facts", "Rule Base", "Save Plan"]
    )

    with tab_dashboard:
        display_dashboard(result, saved_profile)
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
