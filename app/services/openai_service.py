from openai import OpenAI
from app.utils.config import OPENAI_API_KEY_MASTERSCHOOL

client = OpenAI(api_key=OPENAI_API_KEY_MASTERSCHOOL)

def generate_help_post(user_input: str, mode: str = "suchen") -> tuple[str, int]:
    role = "suchenden" if mode == "suchen" else "helfenden"

    system_prompt = (
        f"Du bist ein Assistent, der aus kurzen WhatsApp-Nachrichten freundliche, einladende Posts für eine Nachbarschaftshilfe-App generiert. "
        f"Der Text soll im Namen eines {role} Nutzers geschrieben sein, maximal 2–3 Sätze lang, höflich, gut verständlich und darf Emoji enthalten."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        max_tokens=100,
        temperature=0.7,
    )

    post_text = response.choices[0].message.content.strip()
    token_count = response.usage.total_tokens

    return post_text, token_count