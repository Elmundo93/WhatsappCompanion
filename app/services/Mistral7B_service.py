import requests
from app.utils.config import HUGGINGFACE_API_KEY

def generate_help_post_mistral(user_input: str, mode: str = "suchen") -> str:
    role = "suchenden" if mode == "suchen" else "helfenden"
    prompt = (
        f"Du bist ein Assistent, der aus kurzen WhatsApp-Nachrichten freundliche, einladende Posts für eine Nachbarschaftshilfe-App generiert. "
        f"Der Text soll im Namen eines {role} Nutzers geschrieben sein, maximal 2–3 Sätze lang, höflich, gut verständlich und darf Emoji enthalten.\n\n"
        f"Nachricht: {user_input}\nAntwort:"
    )

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7,
        }
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
        headers=headers,
        json=payload
    )
    return response.json()[0]['generated_text'].split("Antwort:")[-1].strip()