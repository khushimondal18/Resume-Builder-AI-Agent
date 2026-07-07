from crewai import Agent, LLM
import os

def get_ats_agent():
    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )

    return Agent(
        role="ATS Optimizer",
        goal="Improve resume content for ATS screening and target job relevance.",
        backstory="You are an ATS expert who knows keywords, action verbs, and resume screening systems.",
        llm=llm,
        verbose=True
    )