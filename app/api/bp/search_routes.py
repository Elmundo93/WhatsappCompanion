'''api/bp/search_routes.py'''
from flask import Blueprint, request, jsonify
from app.utils.utils import get_embedding_model
from app.vector_store import query_vector

search_api = Blueprint("search_api", __name__)
model = get_embedding_model()

@search_api.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query param `q`"}), 400
    query_vec = model.encode(query).tolist()
    results = query_vector(query_vec)
    return jsonify(results), 200