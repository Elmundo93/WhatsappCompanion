# app/vector/remote_store.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import numpy as np

class RemoteVectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url="https://YOUR-QDRANT-URL",
            api_key="YOUR_KEY"
        )
        self.collection = "users"
        self._ensure_collection()

    def _ensure_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    def add_vector(self, id, vector, metadata):
        self.client.upsert(
            collection_name=self.collection,
            points=[PointStruct(id=id, vector=vector, payload=metadata)]
        )

    def query_vector(self, vector, top_k=5):
        result = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=top_k
        )
        return [r.payload for r in result]

    def delete_vector(self, id):
        self.client.delete(collection_name=self.collection, points_selector={"points": [id]})

    def reset(self):
        self._ensure_collection()