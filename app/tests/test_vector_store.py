import numpy as np
from app.vector_store import add_vector, query_vector, reset_store

def test_vector_add_and_query():
    reset_store()
    vec = np.random.rand(384).astype("float32")
    add_vector("test-id", vec.tolist(), {"name": "Test User"})

    results = query_vector(vec.tolist(), top_k=1)
    assert len(results) == 1
    assert results[0]["name"] == "Test User"