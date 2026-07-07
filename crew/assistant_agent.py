import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def clean_json(text):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def get_resume_command(user_message, resume_data):
    prompt = f"""
You are Resume Copilot.

You ONLY handle resume-related requests.
If unrelated, return out_of_scope.

Current resume data:
{resume_data}

User request:
{user_message}

Return ONLY valid JSON. No explanation.

Allowed intents:

1. update_field
{{"intent":"update_field","field":"name/roll_no/email/phone/linkedin/github/degree/institute/target_role","value":"..."}}

2. create_section
{{"intent":"create_section","section":"Section Name"}}

3. add_to_section
{{"intent":"add_to_section","section":"Section Name","content":"resume bullet/content"}}

4. delete_section
{{"intent":"delete_section","section":"Section Name"}}

5. rename_section
{{"intent":"rename_section","old_section":"Old Name","new_section":"New Name"}}

6. rewrite_projects
{{"intent":"rewrite_projects","instruction":"how to rewrite projects"}}

7. rewrite_experience
{{"intent":"rewrite_experience","instruction":"how to rewrite experience"}}

8. rewrite_all
{{"intent":"rewrite_all","instruction":"how to improve the whole resume"}}

9. suggest_improvements
{{"intent":"suggest_improvements","message":"resume improvement suggestions"}}

10. out_of_scope
{{"intent":"out_of_scope","message":"I can only help with resume editing."}}

Examples:
User: Add a new section named Meri Marzi
{{"intent":"create_section","section":"Meri Marzi"}}

User: Improve my projects for data engineer role
{{"intent":"rewrite_projects","instruction":"Rewrite project bullets for a Data Engineer role using strong action verbs and ATS keywords."}}

User: Make my experience sound professional
{{"intent":"rewrite_experience","instruction":"Rewrite experience bullets professionally with action verbs."}}

User: Make my whole resume better
{{"intent":"rewrite_all","instruction":"Improve all resume bullets and wording professionally."}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return clean_json(response.text)

    except Exception as e:
        error_text = str(e)
        if "RESOURCE_EXHAUSTED" in error_text or "quota" in error_text.lower() or "429" in error_text:
            return {
                "intent": "out_of_scope",
                "message": "You are out of Gemini API free requests for today. Please try again tomorrow or use basic resume edits like adding/deleting sections, updating phone/email, etc."
                }
        if "503" in error_text or "UNAVAILABLE" in error_text:
            return {
                "intent": "out_of_scope",
                "message": "Gemini is temporarily busy right now. Please try again after some time."
                }
        return {
            "intent": "out_of_scope",
            "message": "AI is temporarily unavailable. Please try again later."
            }


def rewrite_bullets_with_instruction(bullets, instruction, target_role):
    if not bullets:
        return []

    prompt = f"""
You are a professional resume writer.

Target role: {target_role}

Instruction:
{instruction}

Rewrite these resume bullets:
{bullets}

Rules:
- Keep meaning truthful.
- Do not invent fake metrics.
- Use strong action verbs.
- Make bullets ATS-friendly.
- Return ONLY JSON list of strings.

Example:
["Improved ...", "Developed ..."]
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return clean_json(response.text)

    except Exception:
        return bullets