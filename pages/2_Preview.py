import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Resume Preview", layout="wide")

data = st.session_state.get("resume_data", {})

if not data:
    st.warning("Please fill and save your resume details first.")
    st.stop()


def safe(value):
    return str(value or "").strip()


def bullet_list(items):
    if not items:
        return ""
    html = "<ul>"
    for item in items:
        if safe(item):
            html += f"<li>{safe(item)}</li>"
    html += "</ul>"
    return html


html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    background-color: #f2f2f2;
    font-family: "Times New Roman", serif;
}}

.resume-page {{
    width: 850px;
    min-height: 1100px;
    background: white;
    margin: 20px auto;
    padding: 45px 55px;
    color: black;
    box-shadow: 0 0 12px rgba(0,0,0,0.25);
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}

.name {{
    font-size: 26px;
    font-weight: bold;
}}

.left-info, .right-info {{
    font-size: 16px;
    line-height: 1.25;
}}

.right-info {{
    text-align: right;
}}

.section-title {{
    font-variant: small-caps;
    font-size: 17px;
    margin-top: 18px;
    border-bottom: 2px solid #333;
    padding-bottom: 2px;
}}

.edu-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 15px;
}}

.edu-table th, .edu-table td {{
    border: 1px solid #333;
    padding: 5px;
    text-align: center;
}}

.item-head {{
    font-size: 16px;
    font-weight: bold;
    margin-top: 10px;
}}

.item-sub {{
    font-size: 15px;
    font-style: italic;
}}

.right {{
    float: right;
    font-style: italic;
    font-weight: normal;
}}

ul {{
    margin-top: 4px;
    margin-bottom: 6px;
    padding-left: 18px;
}}

li {{
    font-size: 15px;
    margin-bottom: 3px;
}}

.skill-line {{
    font-size: 15px;
    margin-top: 4px;
}}
</style>
</head>

<body>
<div class="resume-page">

<div class="header">
    <div class="left-info">
        <div class="name">{safe(data.get("name")).upper()}</div>
        <div>Roll No.: {safe(data.get("roll_no"))}</div>
        <div>{safe(data.get("degree"))}</div>
        <div>{safe(data.get("institute"))}</div>
    </div>

    <div class="right-info">
        <div>{safe(data.get("phone"))}</div>
        <div>{safe(data.get("email"))}</div>
        <div>{safe(data.get("github"))}</div>
        <div>{safe(data.get("linkedin"))}</div>
    </div>
</div>
"""

education = data.get("education_data", [])
if education:
    html += """
    <div class="section-title">Education</div>
    <table class="edu-table">
    <tr>
        <th>Degree/Certificate</th>
        <th>Institute/School(Board)</th>
        <th>CGPA/Percentage</th>
        <th>Year</th>
    </tr>
    """
    for edu in education:
        html += f"""
        <tr>
            <td>{safe(edu.get("degree"))}</td>
            <td>{safe(edu.get("institute"))}</td>
            <td>{safe(edu.get("score"))}</td>
            <td>{safe(edu.get("year"))}</td>
        </tr>
        """
    html += "</table>"

experience = data.get("experience_data", [])
if experience:
    html += '<div class="section-title">Experience</div>'
    for exp in experience:
        html += f"""
        <div class="item-head">
            • {safe(exp.get("company"))}
            <span class="right">{safe(exp.get("duration"))}</span>
        </div>
        <div class="item-sub">
            {safe(exp.get("role"))}
            <span class="right">{safe(exp.get("location"))}</span>
        </div>
        {bullet_list(exp.get("bullets", []))}
        """

projects = data.get("project_data", [])
if projects:
    html += '<div class="section-title">Projects</div>'
    for project in projects:
        html += f"""
        <div class="item-head">
            • {safe(project.get("name"))} | {safe(project.get("tech_stack"))}
            <span class="right">{safe(project.get("duration"))}</span>
        </div>
        <div class="item-sub">{safe(project.get("link"))}</div>
        {bullet_list(project.get("bullets", []))}
        """

skills = {
    "Programming Languages": data.get("programming", ""),
    "Web Technologies & Frameworks": data.get("frameworks", ""),
    "Databases": data.get("databases", ""),
    "Tools": data.get("tools", ""),
    "Cloud / Platforms": data.get("cloud", ""),
    "Soft Skills": data.get("soft_skills", ""),
}

skills = {k: v for k, v in skills.items() if safe(v)}

if skills:
    html += '<div class="section-title">Technical Skills</div>'
    for key, value in skills.items():
        html += f'<div class="skill-line">• <b>{key}:</b> {safe(value)}</div>'

if safe(data.get("courses")):
    html += '<div class="section-title">Key Courses Taken</div><ul>'
    for course in data.get("courses", "").split("\n"):
        if safe(course):
            html += f"<li>{safe(course)}</li>"
    html += "</ul>"

if safe(data.get("achievements")):
    html += '<div class="section-title">Achievements</div><ul>'
    for achievement in data.get("achievements", "").split("\n"):
        if safe(achievement):
            html += f"<li>{safe(achievement).lstrip('-• ')}</li>"
    html += "</ul>"

if safe(data.get("positions")):
    html += '<div class="section-title">Positions of Responsibility</div><ul>'
    for position in data.get("positions", "").split("\n"):
        if safe(position):
            html += f"<li>{safe(position).lstrip('-• ')}</li>"
    html += "</ul>"

if safe(data.get("extra")):
    html += '<div class="section-title">Extracurricular</div><ul>'
    for item in data.get("extra", "").split("\n"):
        if safe(item):
            html += f"<li>{safe(item).lstrip('-• ')}</li>"
    html += "</ul>"
custom_sections = data.get("custom_sections", {})

for section_name, items in custom_sections.items():
    if items:
        html += f'<div class="section-title">{section_name.upper()}</div><ul>'
        for item in items:
            html += f"<li>{safe(item)}</li>"
        html += "</ul>"
html += """
</div>
</body>
</html>
"""

components.html(html, height=1250, scrolling=True)