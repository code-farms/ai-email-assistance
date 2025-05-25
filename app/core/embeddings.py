from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def email_embedder(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding.tolist()