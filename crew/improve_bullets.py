import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def improve_single_bullet(bullet, target_role):
    if not bullet.strip():
        return bullet

    prompt = f"""
    Improve this resume bullet for the role: {target_role}

    Original bullet:
    {bullet}

    Rules:
    - Keep it truthful
    - Do not invent fake numbers
    - Start with a strong action verb
    - Make it concise
    - Return only one bullet point
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text.strip().lstrip("-• ").strip()
    except Exception:
        return bullet