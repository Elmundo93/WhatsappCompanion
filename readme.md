# 🤖 WhatsAppCompanion for AushilfApp

**WhatsAppCompanion** is a smart Flask-based backend service for [AushilfApp](https://www.wir-helfen-aus.de). It enables natural WhatsApp interaction with users to collect help requests or offers, understand them, and return matching contacts – fully local, privacy-first, and app-free.

## 🚀 Project Goal

Enable easy access to neighborhood assistance, especially for older or non-technical people – via **WhatsApp**, without requiring app installation or registration. The system handles all communication automatically via the official Twilio WhatsApp bot.

## 🧱 Tech Stack

| Component                | Description                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| **Backend**              | Python 3.9, Flask                                                            |
| **Database**             | SQLite (local, persistent)                                                   |
| **Vector Search**        | SentenceTransformer (MiniLM), FAISS (local) or Qdrant (optional)             |
| **NLP Model**            | `all-MiniLM-L6-v2`                                                           |
| **WhatsApp API**         | Twilio Sandbox                                                               |
| **Testing & Dev Tools**  | ngrok (local), pytest                                                        |

## 🧠 Features

- 📲 **Natural dialog** via WhatsApp
- 💬 **Session tracking** with simple state machine (e.g., "awaiting_help_desc")
- 🔎 **Semantic vector search** over user bios
- 💾 **Persistent chat history** stored in SQLite
- 🔐 **Privacy-first**, local-only execution
- 🧪 **pytest suite** for core logic

## 🗂️ Project Structure

```bash
app/
├── api/                  # Flask Blueprints and webhook routes
├── db/                   # SQLite handling, chat history, models
├── services/             # Business logic & session handling
├── twilio/               # Dialog engine and Twilio client
├── utils/                # Helpers (e.g., embeddings)
├── templates/            # WhatsApp templates (optional)
├── __init__.py           # App factory
└── run.py                # Entry-point (localhost:5050)
```

## ⚙️ Local Setup

```bash
git clone https://github.com/Elmundo93/WhatsAppCompanion.git
cd WhatsAppCompanion
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Example .env

```env
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...

TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

VECTOR_DB_PATH=data/users_embeddings.index
DB_PATH=data/chat.db
PORT=5050
OPENAI_API_KEY=...

```

## 💬 WhatsApp Integration

1. [Activate Twilio Sandbox](https://www.twilio.com/console/sms/whatsapp/learn)
2. Scan QR with your test phone
3. Start ngrok:
   ```bash
   ngrok http 5050
   ```
4. Set your webhook to:
   ```
   https://<ngrok-url>/webhook/twilio
   ```

## 🧪 Run Tests

```bash
pytest tests/
```

## 🧭 Roadmap

- 📡 Switch to real vector DB (e.g., Qdrant)
- 🔐 Input validation & abuse prevention
- 🗺️ Geo-based matching
- 💬 Contextual dialog memory (session-based prompting)

## 👥 Contribute

This project is part of the nonprofit initiative [Wir helfen aus e.V.](https://www.wir-helfen-aus.de). Contact: **Lemont-Kim@Wir-helfen-aus.de**

## 📄 License

MIT License


# 🤖 WhatsAppCompanion für AushilfApp

**WhatsAppCompanion** ist ein intelligentes Flask-basiertes Backend für die [AushilfApp](https://www.wir-helfen-aus.de), das über WhatsApp mit Nutzer:innen interagiert, um Hilfeanfragen oder -angebote automatisiert entgegenzunehmen, zu verstehen und passende Kontakte zu vermitteln – vollständig datenschutzfreundlich und lokal lauffähig.

## 🚀 Ziel des Projekts

Menschen, insbesondere ältere oder weniger technikaffine Personen, sollen auf einfache Weise Zugang zu nachbarschaftlicher Hilfe erhalten – **per WhatsApp**, ohne App-Installation oder Registrierung. Die Kommunikation erfolgt durch eine natürliche Dialogführung über den offiziellen Twilio WhatsApp-Bot der AushilfApp.

## 🧱 Tech Stack

| Komponente               | Beschreibung                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| **Backend**              | Python 3.9, Flask                                                            |
| **Datenbank**            | SQLite (lokal, persistent)                                                   |
| **Vektor-Suche**         | SentenceTransformer (MiniLM), FAISS (lokal) oder Qdrant (optional)           |
| **NLP-Modell**           | `all-MiniLM-L6-v2`                                                           |
| **WhatsApp**             | Twilio Sandbox API                                                           |
| **Deployment & Testing** | ngrok (lokal), pytest                                                        |

## 🧠 Funktionen

- 📲 **Dialogbasierte Kommunikation** per WhatsApp
- 💬 **Zustandsspeicherung** der Nutzer-Session mit Zustandsmaschine (z. B. "awaiting_help_desc")
- 🔎 **Semantische Vektor-Suche** über Hilfeangebote per User-Bio
- 💾 **Nachrichtenverlauf** persistent in SQLite gespeichert
- 🔐 **DSGVO-freundlich**, lokal ausführbar ohne externe Speicherung
- 🧪 **Testsuite** mit `pytest` für alle Kernkomponenten

## 🗂️ Projektstruktur

```bash
app/
├── api/                  # Flask Blueprints und Webhook-Endpunkte
├── db/                   # SQLite-Verwaltung, Models und Chatverlauf
├── services/             # Business-Logik & Speicherstrategien
├── twilio/               # Dialoglogik und Twilio-Antwortsystem
├── utils/                # Hilfsfunktionen (z. B. Embeddings)
├── templates/            # WhatsApp Templates (optional)
├── __init__.py           # App Factory
└── run.py                # Entry-Point (localhost:5050)
```

## ⚙️ Installation (lokal)

```bash
git clone https://github.com/Elmundo93/WhatsAppCompanion.git
cd WhatsAppCompanion
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### .env Datei (Beispiel):

```env
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...

TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

VECTOR_DB_PATH=data/users_embeddings.index
DB_PATH=data/chat.db
PORT=5050
```

## 💬 WhatsApp Integration

1. [Twilio Sandbox aktivieren](https://www.twilio.com/console/sms/whatsapp/learn)
2. Testnummer hinzufügen & QR-Code scannen
3. ngrok starten:
   ```bash
   ngrok http 5050
   ```
4. Webhook setzen:
   ```
   https://<ngrok-url>/webhook/twilio
   ```

## 🧪 Tests ausführen

```bash
pytest tests/
```

## 🧭 Ausblick

- 📡 Integration mit echter Vektor-Datenbank
- 🔐 Eingabevalidierung & Abuse-Prevention
- 🗺️ Geobasierte Vermittlung
- 💬 Kontextuelles Verständnis (Session Prompting)

## 👥 Mitwirken

Das Projekt ist Teil der gemeinnützigen Initiative [Wir helfen aus e.V.](https://www.wir-helfen-aus.de). Kontakt: **Lemont-Kim@Wir-helfen-aus.de**

## 📄 Lizenz

MIT License