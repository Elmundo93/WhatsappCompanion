import anthropic
from app.utils.config import CLAUDE_API_KEY

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def generate_help_post_claude(user_input: str, mode: str = "suchen") -> str:
    role = "suchenden" if mode == "suchen" else "helfenden"
    system_prompt = (
        f"Du bist ein Assistent, der aus kurzen WhatsApp-Nachrichten freundliche, einladende Posts für eine Nachbarschaftshilfe-App generiert. "
        f"Der Text soll im Namen eines {role} Nutzers geschrieben sein, maximal 2–3 Sätze lang, höflich, gut verständlich und darf Emoji enthalten."
    )

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=100,
        temperature=0.7,
        messages=[
            {"role": "user", "content": f"{system_prompt}\n\nNachricht: {user_input}"}
        ]
    )
    return response.content[0].text.strip()