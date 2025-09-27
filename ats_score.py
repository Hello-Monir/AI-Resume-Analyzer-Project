from typing import Dict
from utils import extract_keywords

def keyword_overlap_score(resume_text: str, jd_text: str) -> Dict[str, any]:
    resume_keys = set(extract_keywords(resume_text, 80))
    jd_keys = set(extract_keywords(jd_text, 80))
    hits = sorted(list(resume_keys & jd_keys))
    miss = sorted(list(jd_keys - resume_keys))
    coverage = 0.0 if not jd_keys else 100.0 * len(hits) / len(jd_keys)
    return {
        "score": round(coverage, 2),
        "matched_keywords": hits,
        "missing_keywords": miss,
        "resume_keywords": sorted(list(resume_keys)),
        "jd_keywords": sorted(list(jd_keys)),
    }
