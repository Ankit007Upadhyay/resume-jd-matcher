import streamlit as st

SIGNALS = [
    ("semantic", "Semantic"),
    ("skills", "Skills"),
    ("rubric", "LLM rubric"),
]


def render_score_card(report):
    breakdown = report["breakdown"]

    st.subheader("Overall match")
    left, right = st.columns([1, 3])
    left.metric("Final score", f"{report['final_score']}/100")
    right.markdown(f"**{report['verdict']}**")
    right.progress(report["final_score"] / 100)

    columns = st.columns(len(SIGNALS))
    for column, (key, label) in zip(columns, SIGNALS):
        weight_percent = int(breakdown["weights"][key] * 100)
        column.metric(f"{label} ({weight_percent}%)", breakdown["components"][key])
        column.caption(f"adds {breakdown['contributions'][key]} points")