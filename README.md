# FitExpert: Rule-Based Fitness & Exercise Advisor

FitExpert is a rule-based expert system developed as an undergraduate Artificial Intelligence term project. The system provides personalized fitness and exercise recommendations using a custom forward-chaining inference engine, a separate knowledge base, certainty factors, conflict resolution, and an explainable reasoning chain.

The project was designed to avoid a shallow form-based structure. Instead of directly mapping user input to output, FitExpert stores user information as facts, applies expert rules through an inference engine, resolves conflicts using rule priority, and explains why each conclusion was reached.

---

## Project Topic

**Selected Topic:** Fitness & Exercise Advisor

This topic was selected from the Healthcare & Medical Expert Systems category.

---

## Expert System Features

FitExpert includes the major components of a real expert system:

| Component | Implementation |
|---|---|
| Knowledge Base | `knowledge_base/rules.py` contains 94 meaningful expert rules |
| Working Memory | `engine/fact_base.py` stores user facts and derived facts |
| Inference Engine | `engine/inference_engine.py` performs forward chaining |
| Conflict Resolution | `engine/conflict_resolver.py` uses salience, specificity, and certainty factor |
| Certainty Factors | `engine/certainty.py` supports confidence-based reasoning |
| Explanation Module | `engine/explanation.py` records fired rules and reasoning chain |
| User Interface | `app.py` provides a Streamlit web interface |
| Testing | `tests/` contains multiple scenario-based test cases |

---

## Why This Is Not Simple If-Else Programming

A simple form-based system follows this pattern:

```text
Input → direct condition check → output