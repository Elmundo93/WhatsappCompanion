# app/services/openai_transcribe.py
import requests
import time
from io import BytesIO
import logging
from openai import OpenAI
from app.utils.config import OPENAI_API_KEY_MASTERSCHOOL

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY_MASTERSCHOOL)

def transcribe_voice_message(media_url: str) -> str:
    try:
        start = time.perf_counter()
        response = requests.get(media_url, timeout=10)
        audio = BytesIO(response.content)
        audio.name = "voice.ogg"

        transcription = client.audio.transcriptions.create(
            file=audio,
            model="whisper-1",
            response_format="text",
            language="de"
        )
        duration = time.perf_counter() - start
        logger.info(f"🕓 Whisper-Transkription abgeschlossen in {duration:.2f}s")
        return transcription.strip()

    except requests.exceptions.Timeout:
        logger.warning("⚠️ Whisper: Timeout beim Laden der Audiodatei.")
        return "[Timeout bei Sprachnachricht. Bitte erneut senden.]"

    except Exception as e:
        logger.error(f"❌ Whisper-Fehler: {e}")
        return "[Sprachnachricht konnte nicht erkannt werden.]"