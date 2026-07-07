import streamlit as st
from crew.assistant_agent import get_resume_command, rewrite_bullets_with_instruction

st.title("✨ Resume Copilot")

st.write("Ask Resume Copilot to add, delete, edit, rewrite, or improve anything in your resume.")

if "resume_data" not in st.session_state:
    st.session_state.resume_data = {}

data = st.session_state.resume_data


def normalize(text):
    return text.strip().lower().replace(" section", "")


def add_custom_section(section, content=None):
    if "custom_sections" not in data:
        data["custom_sections"] = {}

    if section not in data["custom_sections"]:
        data["custom_sections"][section] = []

    if content:
        data["custom_sections"][section].append(content)


def delete_section(section):
    key = normalize(section)

    standard = {
        "courses": "courses",
        "key courses": "courses",
        "achievements": "achievements",
        "awards": "achievements",
        "extracurricular": "extra",
        "extracurricular activities": "extra",
        "positions": "positions",
        "positions of responsibility": "positions",
    }

    if key in standard:
        data[standard[key]] = ""
        return True

    if "custom_sections" in data:
        for existing in list(data["custom_sections"].keys()):
            if normalize(existing) == key:
                del data["custom_sections"][existing]
                return True

    return False


def rename_section(old, new):
    if "custom_sections" in data:
        for existing in list(data["custom_sections"].keys()):
            if normalize(existing) == normalize(old):
                data["custom_sections"][new] = data["custom_sections"].pop(existing)
                return True
    return False


def rewrite_projects(instruction):
    role = data.get("target_role", "General Role")

    for project in data.get("project_data", []):
        project["bullets"] = rewrite_bullets_with_instruction(
            project.get("bullets", []),
            instruction,
            role
        )


def rewrite_experience(instruction):
    role = data.get("target_role", "General Role")

    for exp in data.get("experience_data", []):
        exp["bullets"] = rewrite_bullets_with_instruction(
            exp.get("bullets", []),
            instruction,
            role
        )


def rewrite_all(instruction):
    rewrite_projects(instruction)
    rewrite_experience(instruction)


user_message = st.text_area(
    "What do you want to do?",
    placeholder="""Examples:
Add a new section named Conferences
Add AWS certification
Delete Courses section
Rename Conferences to Conferences Attended
Improve my projects for Data Engineer role
Rewrite my experience professionally
Make my whole resume ATS-friendly"""
)

if st.button("Run Resume Copilot"):
    if not user_message.strip():
        st.warning("Please type a resume-related command.")
    else:
        command = get_resume_command(user_message, data)
        intent = command.get("intent")

        if intent == "update_field":
            data[command["field"]] = command.get("value", "")
            st.success(f"Updated {command['field']}.")

        elif intent == "create_section":
            add_custom_section(command["section"])
            st.success(f"Created section: {command['section']}.")

        elif intent == "add_to_section":
            add_custom_section(command["section"], command.get("content", ""))
            st.success(f"Added to {command['section']}.")

        elif intent == "delete_section":
            if delete_section(command["section"]):
                st.success(f"Deleted {command['section']}.")
            else:
                st.warning("Section not found.")

        elif intent == "rename_section":
            if rename_section(command["old_section"], command["new_section"]):
                st.success(f"Renamed {command['old_section']} to {command['new_section']}.")
            else:
                st.warning("Only custom sections can be renamed currently.")

        elif intent == "rewrite_projects":
            rewrite_projects(command.get("instruction", "Rewrite projects professionally."))
            st.success("Projects rewritten successfully.")

        elif intent == "rewrite_experience":
            rewrite_experience(command.get("instruction", "Rewrite experience professionally."))
            st.success("Experience rewritten successfully.")

        elif intent == "rewrite_all":
            rewrite_all(command.get("instruction", "Improve the whole resume professionally."))
            st.success("Resume content improved successfully.")

        elif intent == "suggest_improvements":
            st.info(command.get("message", "No suggestions available."))

        elif intent == "out_of_scope":
            st.warning(command.get("message", "I can only help with resume editing."))

        else:
            st.warning("Could not understand command.")

        st.session_state.resume_data = data

st.divider()

st.subheader("Current Resume Data")
st.write(data)