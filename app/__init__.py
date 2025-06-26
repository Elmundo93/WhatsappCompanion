# app/__init__.py
from flask import Flask
from app.utils.utils import init_logger, get_embedding_model
from app.db.db import init_db
from app.api.routes import register_routes
from app.db.chat_history import init_whatsapp_table


def create_app():
    app = Flask(__name__)
    init_logger()
    get_embedding_model()
    init_db()
    init_whatsapp_table()
    register_routes(app)
    print("init loaded")


    return app