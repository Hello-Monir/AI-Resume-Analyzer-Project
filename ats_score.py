from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity_bert(resume_text: str, job_desc: str) -> float:
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embeddings_resume = model.encode([resume_text])
    embeddings_job = model.encode([job_desc])
    similarity = cosine_similarity(embeddings_resume, embeddings_job)[0][0]
    return similarity
