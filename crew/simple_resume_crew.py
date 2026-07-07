import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def call_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text


def local_resume_generator(resume_data):
    return f"""
# {resume_data.get("name", "")}

Email: {resume_data.get("email", "")}  
Phone: {resume_data.get("phone", "")}  
LinkedIn: {resume_data.get("linkedin", "")}  
GitHub: {resume_data.get("github", "")}

## Target Role
{resume_data.get("target_role", "")}

## Education
{resume_data.get("education", "")}

## Experience
{resume_data.get("experience", "")}

## Projects
{resume_data.get("projects", "")}

## Technical Skills
{resume_data.get("skills", "")}

## Key Courses
{resume_data.get("courses", "")}

## Achievements
{resume_data.get("achievements", "")}

## Extracurricular Activities
{resume_data.get("extra", "")}

---

Generated through Resume Writer Agent → ATS Optimizer Agent → Resume Formatter Agent.
"""


def run_simple_resume_crew(resume_data):
    try:
        writer_output = call_gemini(f"""
        Resume Writer Agent:
        Convert this raw resume data into professional resume content.
        Use action verbs. Do not invent fake information.

        {resume_data}
        """)

        ats_output = call_gemini(f"""
        ATS Optimizer Agent:
        Optimize this resume for ATS and target role.
        Target role: {resume_data.get("target_role", "General Role")}

        {writer_output}
        """)

        final_resume = call_gemini(f"""
        Resume Formatter Agent:
        Format this into clean markdown resume sections:
        NAME, CONTACT, EDUCATION, EXPERIENCE, PROJECTS,
        TECHNICAL SKILLS, KEY COURSES, ACHIEVEMENTS,
        EXTRACURRICULAR ACTIVITIES.

        {ats_output}
        """)

        return final_resume

    except Exception as e:
        print("Gemini failed. Using fallback:", e)
        return local_resume_generator(resume_data)