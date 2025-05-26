'''utils/utils.py'''
from sentence_transformers import SentenceTransformer
import logging

_model = None

def is_valid_whatsapp_request(req):
    return req.method == "POST" and "Body" in req.form and "From" in req.form

def init_logger():
    logger = logging.getLogger("whatsapp_matcher")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model