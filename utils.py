import logging

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