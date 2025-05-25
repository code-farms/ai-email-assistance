from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

qdrant_url = os.getenv("QDRANT_DB_URL")

def get_qdrant_client():
    client = QdrantClient(qdrant_url)
    print("✅ Qdrant client created successfully!")
    return client

def ensure_collection(client: QdrantClient, collection_name: str):
    existing_collections = client.get_collections().collections
    if collection_name not in [col.name for col in existing_collections]:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            ),
        )
        print(f"✅ Collection '{collection_name}' created successfully!")
    else:
        print(f"✅ Collection '{collection_name}' already exists!")

def add_email_embedding(embedding: list[float], metadata: dict, collection_name: str = "emails"):
    client = get_qdrant_client()
    ensure_collection(client, collection_name)

    if len(embedding) != 384:
        raise ValueError("Embedding vector must be of length 384")

    point_id = metadata.get("id", str(uuid.uuid4()))

    try:
        client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=metadata,
                )
            ],
        )
        print("✅ Email embedding added successfully!")
    except Exception as e:
        print(f"❌ Failed to add embedding: {e}")

    return point_id