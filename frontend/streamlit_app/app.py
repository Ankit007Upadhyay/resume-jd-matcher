import os
import sys
import tempfile
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.services.analyzer import analyze  # noqa: E402
from components.criteria_table import render_criteria_table  # noqa: E402
from components.score_card import render_score_card  # noqa: E402
from components.suggestions import render_suggestions  # noqa: E402

st.set_page_config(page_title="Resume + JD Matcher", layout="wide")


def run_analysis(uploaded_file, jd_text):
    suffix = Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        return analyze(tmp_path, jd_text)
    finally:
        os.unlink(tmp_path)


st.title("AI Resume Analyzer / JD Matcher")
st.caption(
    "Hybrid score: semantic similarity + skill overlap + LLM rubric, "
    "with quoted evidence from your resume."
)

with st.sidebar:
    st.header("Input")
    uploaded_file = st.file_uploader("Resume (PDF or DOCX)", type=["pdf", "docx"])
    jd_text = st.text_area("Job description", height=300)
    analyze_clicked = st.button("Analyze", type="primary")
    st.caption(
        "Your resume text is sent to the Groq API for scoring. "
        "Files are not stored."
    )

if analyze_clicked:
    if uploaded_file is None or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        try:
            with st.spinner("Analyzing... this can take 15-40 seconds"):
                st.session_state["report"] = run_analysis(uploaded_file, jd_text)
        except Exception as error:
            st.session_state.pop("report", None)
            st.error(f"Analysis failed: {error}")

report = st.session_state.get("report")

if report:
    render_score_card(report)
    st.divider()
    render_criteria_table(report)
    st.divider()
    render_suggestions(report)
else:
    st.info("Upload a resume, paste a job description, and click Analyze.")