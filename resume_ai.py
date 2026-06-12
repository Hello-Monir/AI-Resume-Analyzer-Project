from typing import Dict, Optional
import os
from dotenv import load_dotenv
load_dotenv()

def suggest_improvements(cos_sim: float, overlap_score: float) -> Dict[str, str]:
    # Non-LLM baseline suggestions
    tips = []
    if cos_sim < 0.6:
        tips.append("Align summary and experience with the top responsibilities in the job description.")
    if overlap_score < 60:
        tips.append("Add missing hard skills and tools from the JD in Skills and Experience bullets.")
    if overlap_score < 40:
        tips.append("Include quantified achievements that demonstrate the JD outcomes.")
    if not tips:
        tips.append("Resume already aligns well. Add role-specific metrics to stand out.")
    return {"suggestions": "\n- " + "\n- ".join(tips)}

def llm_rewrite_prompt(resume_text: str, jd_text: str) -> str:
    return (
        "Rewrite the following resume bullet points to better match the job description while staying truthful. "
        "Use crisp action verbs and include measurable outcomes. "
        "Resume:\n" + resume_text[:4000] + "\n\nJob Description:\n" + jd_text[:4000]
    )


