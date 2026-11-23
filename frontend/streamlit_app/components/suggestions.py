import streamlit as st


def render_suggestions(report):
    skills = report["skills"]

    st.subheader("Skills check")
    left, right = st.columns(2)

    left.markdown("**Matched skills**")
    if skills["matched"]:
        left.success(", ".join(skills["matched"]))
    else:
        left.write("None")

    right.markdown("**Missing keywords**")
    if skills["missing"]:
        right.warning(", ".join(skills["missing"]))
    else:
        right.write("None")

    if skills["missing"]:
        st.info(
            "Add a missing skill to your resume only if you truly have it. "
            "Mention where you used it (project or job), not just in a skills list."
        )

    weak = [c["criterion"] for c in report["criteria"] if c["weak_match"]]
    if weak:
        st.markdown("**Criteria with weak resume evidence**")
        for criterion in weak:
            st.write(f"- {criterion}")