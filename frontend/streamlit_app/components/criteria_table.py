import streamlit as st


def yes_no(value):
    return "Yes" if value else "No"


def render_criteria_table(report):
    st.subheader("Criteria breakdown")

    rows = [
        {
            "Criterion": c["criterion"],
            "Score (0-100)": c["final_points"],
            "Found": yes_no(c["found"]),
            "Quote verified": yes_no(c["grounded"]),
            "Weak retrieval": yes_no(c["weak_match"]),
        }
        for c in report["criteria"]
    ]
    st.dataframe(rows, hide_index=True, use_container_width=True)

    st.markdown("**Evidence from the resume**")
    for c in report["criteria"]:
        with st.expander(f"{c['criterion']}  |  {c['final_points']}/100"):
            if c["evidence"]:
                st.text(c["evidence"])
                if not c["grounded"]:
                    st.warning(
                        "This quote could not be found in the resume, "
                        "so the score was capped."
                    )
            else:
                st.write("No supporting evidence found.")