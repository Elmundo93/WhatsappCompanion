# 🤖📱 WhatsApp AI Matcher – Neighborhood Support via Twilio & AI

This project is part of my advanced training at **Masterschool** and serves as a practical demonstration of how artificial intelligence, messaging services, and community-based platforms can be seamlessly integrated.

The solution is designed for **"Wir helfen aus e.V."**, a non-profit initiative behind the [AushilfApp](https://www.wir-helfen-aus.de) – an app that connects people who want to help with those who need assistance. This backend service turns WhatsApp into an intelligent access point to the ecosystem of neighborhood aid.

---

## 🌟 Project Goal

To provide **low-barrier, AI-assisted access** to the AushilfApp network using WhatsApp.

After a user registers in the AushilfApp, they automatically receive a message via WhatsApp, inviting them to describe their personal help scenario. Whether they need help or want to offer it – they just type it in natural language.

Behind the scenes, an AI processes the message and runs a **vector similarity search** on existing user bios to find the best matches for their request. The results are sent back via WhatsApp, making the process simple, inclusive, and human-centered.

---

## 🧠 Tech Stack

| Technology            | Purpose                                           |
|------------------------|---------------------------------------------------|
| Flask (Python)        | Lightweight web server for Twilio webhook         |
| Twilio                | WhatsApp Messaging API                            |
| SentenceTransformers  | NLP model for semantic embedding & similarity     |
| Local JSON Store      | Vector-based user profile storage (or Qdrant)     |
| Python Logging        | Structured, production-ready debugging            |

---

## 🎓 Educational Focus

This project showcases practical skills in:

- Natural Language Processing (NLP)
- Twilio API & webhook handling
- AI-enhanced user matching
- Full-stack architecture using Python
- Working with vector databases (semantic search)
- Clean code structure, validation, logging & scalability patterns

---

## 🚀 Features

- ✅ WhatsApp integration via Twilio Sandbox
- ✅ Automatic onboarding message (`start` keyword)
- ✅ AI-based similarity search using SentenceTransformers
- ✅ JSON-based vector store for fast prototyping
- ✅ Modular, production-ready Python structure
- ✅ Extendable to Supabase or live vector DBs (e.g., Qdrant, Pinecone)

---

## 📦 Installation


git clone https://github.com/YOUR_USERNAME/whatsapp-ai-matcher.git
cd whatsapp-ai-matcher
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt

---

## ⚙️ Configuration

Edit the config.py file:

TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
VECTOR_DB_PATH = "data/users_embeddings.json"

Set up your Twilio WhatsApp Sandbox and point the webhook to /whatsapp.

---

💬 Example Flow
	1.	User sends:
"I’m looking for someone who can help me with gardening."
	2.	AI processes text → generates embedding → compares with bios
	3.	Response via WhatsApp:
“Here are some people who might be able to help:
Anna (Score: 0.91)
Leo (Score: 0.87)”

---

🛠 Development Notes
	•	Sample bios and vector data live in data/users_embeddings.json
	•	Create new vectors using: generate_vectorstore_from_users(users)
	•	Easily replace the JSON store with Qdrant or Chroma if needed

---

🌐 Use Cases & Potential

This project could evolve into a fully-fledged matching system for:
	•	Community aid & local volunteering
	•	First-contact systems for NGOs
	•	Mental health chat routing
	•	Skills-based mentorship programs

---

🤝 About the Initiative

“Wir helfen aus e.V.” is a non-profit association based in Germany. Its goal is to foster communication and mutual support between neighbors. Learn more at wir-helfen-aus.de

---

📜 License

MIT – free to use, adapt, remix & contribute. Contributions welcome!

---

🙌 Made with Purpose

Created as part of my Masterschool journey – learning by doing with real-world impact.
