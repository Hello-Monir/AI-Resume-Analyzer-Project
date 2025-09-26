import os
import openai
from dotenv import load_dotenv

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_MODEL = os.getenv("AZURE_OPENAI_MODEL")

openai.api_type = "azure"
openai.api_base = AZURE_ENDPOINT
openai.api_version = "2023-07-01-preview"
openai.api_key = AZURE_API_KEY

def get_report(resume_text: str, job_desc: str) -> str:
    prompt = f"""
# Context:
- You are an AI Resume Analyzer.
- Analyze Candidate's Resume and Job Description.

# Instruction:
- Evaluate skills, experience, and job-relevant points.
- Score each point out of 5 and add emoji (✅, ❌, ⚠️)
- Final heading: "Suggestions to improve your resume:" 

Candidate Resume: {resume_text}
---
Job Description: {job_desc}

Output format: Score + emoji + explanation per point
"""
    response = openai.ChatCompletion.create(
        engine=AZURE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800
    )
    return response.choices[0].message.content
