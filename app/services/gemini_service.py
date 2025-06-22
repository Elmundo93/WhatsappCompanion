import requests
from app.utils.config import GEMINI_API_KEY

def generate_help_post_gemini(user_input: str, mode: str = "suchen") -> str:
    role = "suchenden" if mode == "suchen" else "helfenden"
    prompt = (
        f"Du bist ein Assistent, der aus kurzen WhatsApp-Nachrichten freundliche, einladende Posts für eine Nachbarschaftshilfe-App generiert. "
        f"Der Text soll im Namen eines {role} Nutzers geschrieben sein, maximal 2–3 Sätze lang, höflich, gut verständlich und darf Emoji enthalten.\n\n"
        f"Nachricht: {user_input}"
    )

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 100}
    }

    response = requests.post(f"{url}?key={GEMINI_API_KEY}", json=payload, headers=headers)
    return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()