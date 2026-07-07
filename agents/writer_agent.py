from crewai import Agent, LLM
import os

def get_resume_writer_agent():
    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )

    return Agent(
        role="Professional Resume Writer",
        goal="Convert raw user resume details into strong professional resume content.",
        backstory="You are an expert resume writer who writes clear, ATS-friendly resume points.",
        llm=llm,
        verbose=True
    )