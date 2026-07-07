from resume.docx_generator import create_resume_docx
import streamlit as st
from dotenv import load_dotenv
from crew.simple_resume_crew import run_simple_resume_crew
from crew.improve_bullets import improve_single_bullet

load_dotenv()

st.title("🤖 Generate AI Resume")

resume_data = st.session_state.get("resume_data", {})

if not resume_data:
    st.warning("Please fill and save your resume details first.")
else:
    st.write("Your saved resume data is ready.")
    if st.button("✨ Improve Bullets with AI"):
        with st.spinner("Improving bullets..."):
            target_role = resume_data.get("target_role", "General Role")
            for exp in resume_data.get("experience_data", []):
                exp["bullets"] = [
                improve_single_bullet(bullet, target_role)
                for bullet in exp.get("bullets", [])
            ]
            for project in resume_data.get("project_data", []):
                project["bullets"] = [
                improve_single_bullet(bullet, target_role)
                for bullet in project.get("bullets", [])
            ]

        st.session_state["resume_data"] = resume_data

        st.success("Bullets improved successfully!")
    if st.button("Generate Resume"):
        with st.spinner("AI agents are working on your resume..."):
            try:
                final_resume = run_simple_resume_crew(resume_data)
                st.session_state["final_resume"] = final_resume
                st.success("Resume generated successfully!")
                st.markdown(final_resume)
            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)

if "final_resume" in st.session_state:
    st.subheader("Final AI Resume")
    st.markdown(st.session_state["final_resume"])
    if st.button("Create DOCX Resume"):
        file_path = create_resume_docx(
            st.session_state["resume_data"],
            st.session_state["final_resume"])
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download DOCX Resume",
                data=file,
                file_name="generated_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )