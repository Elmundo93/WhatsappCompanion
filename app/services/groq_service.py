import requests
from app.utils.config import GROQ_API_KEY

def generate_help_post_groq(user_input: str, mode: str = "suchen") -> str:
    role = "suchenden" if mode == "suchen" else "helfenden"
    system_prompt = (
        f"Du bist ein Assistent, der aus kurzen WhatsApp-Nachrichten freundliche, einladende Posts für eine Nachbarschaftshilfe-App generiert. "
        f"Der Text soll im Namen eines {role} Nutzers geschrieben sein, maximal 2–3 Sätze lang, höflich, gut verständlich und darf Emoji enthalten."
    )

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama3-8b-8192",  # oder "mixtral-8x7b-32768"
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7,
            "max_tokens": 100,
        }
    )
    return response.json()["choices"][0]["message"]["content"].strip()