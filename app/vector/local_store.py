# app/vector/local_store.py
import faiss
import numpy as np

class LocalVectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)  # z. B. MiniLM
        self.id_map = {}

    def add_vector(self, id, vector, metadata):
        vec = np.array([vector]).astype("float32")
        self.index.add(vec)
        self.id_map[self.index.ntotal - 1] = {"id": id, **metadata}

    def query_vector(self, vector, top_k=5):
        vec = np.array([vector]).astype("float32")
        distances, indices = self.index.search(vec, top_k)
        return [self.id_map.get(i) for i in indices[0] if i in self.id_map]

    def delete_vector(self, id):
        # FAISS kann das nur mit IVF oder Flat with remove workaround
        pass

    def reset(self):
        self.__init__()