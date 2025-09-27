import re

def clean_text(t: str) -> str:
    t = t or ""
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def extract_keywords(text: str, top_k: int = 30):
    text = text.lower()
    tokens = re.findall(r"[a-zA-Z]+", text)
    stop = set("""
        a an the of and to in for on with by from as at this that these those is are was were be been have has had
        i you he she it we they them us our your his her their
    """.split())
    freq = {}
    for tok in tokens:
        if tok in stop or len(tok) < 3:
            continue
        freq[tok] = freq.get(tok, 0) + 1
    return sorted(freq, key=freq.get, reverse=True)[:top_k]
