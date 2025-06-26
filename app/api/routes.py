# app/api/routes.py

from app.api.bp.search_routes import search_api
from app.api.bp.twilio_webhook import twilio_webhook

from flask import request, jsonify
from app.db.models import insert_user, update_user, delete_user, get_user, get_all_users
from app.supabase.sync import sync_users_from_supabase
from app.vector_store import rebuild_index
from app.utils.utils import get_embedding_model


def register_routes(app):
    model = get_embedding_model()

    # Standard-REST-Routen für records
    @app.route("/records", methods=["POST"])
    def create_record():
        data = request.json
        if not data or not all(k in data for k in ("supabase_id", "name", "bio")):
            return jsonify({"error": "Invalid payload"}), 400
        insert_user(data["supabase_id"], data["name"], data["bio"])
        return jsonify({"status": "created"}), 201

    @app.route("/records", methods=["GET"])
    def list_all_records():
        users = get_all_users()
        return jsonify(users), 200

    @app.route("/records/<int:user_id>", methods=["PUT"])
    def update_record(user_id):
        data = request.json
        if not data or not all(k in data for k in ("name", "bio")):
            return jsonify({"error": "Invalid payload"}), 400
        update_user(user_id, data["name"], data["bio"])
        return jsonify({"status": "updated"}), 200

    @app.route("/records/<int:user_id>", methods=["DELETE"])
    def delete_record(user_id):
        delete_user(user_id)
        return jsonify({"status": "deleted"}), 200

    @app.route("/records/<int:user_id>", methods=["GET"])
    def get_single_record(user_id):
        user = get_user(user_id)
        if not user:
            return jsonify({"error": "Not found"}), 404
        return jsonify(user), 200

    @app.route("/sync-supabase", methods=["POST"])
    def manual_sync():
        sync_users_from_supabase()
        return jsonify({"status": "supabase sync complete"}), 200

    @app.route("/rebuild-index", methods=["POST"])
    def rebuild():
        rebuild_index()
        return jsonify({"status": "index rebuilt"}), 200

    # ➕ Neue Blueprints registrieren
    app.register_blueprint(search_api)
    app.register_blueprint(twilio_webhook)



