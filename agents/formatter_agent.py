from crewai import Agent, LLM
import os

def get_formatter_agent():
    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )

    return Agent(
        role="Resume Formatter",
        goal="Format the optimized content into a clean professional resume structure.",
        backstory="You format resumes into sections like Education, Experience, Projects, Skills, Achievements.",
        llm=llm,
        verbose=True
    )