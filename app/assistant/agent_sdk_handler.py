# app/assistant/agent_sdk.py
from agents import Agent, Runner, WebSearchTool
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_MASTERSCHOOL")
# optional .env laden

# Agent erstellen (einmalig beim Start)
agent = Agent(
    name="AushilfBot",
    instructions=(
        "Du hilfst Menschen in ihrer Umgebung, Hilfe zu finden oder anzubieten. "
        "Nutze Web-Suche, um aktuelle externe Hilfeangebote zu finden."
    ),
    tools=[WebSearchTool()],
    model="gpt-4.1"  # oder "gpt-4.1-mini" je nach Bedarf
)

runner = Runner()