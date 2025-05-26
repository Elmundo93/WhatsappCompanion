# app/utils/twilio_templates.py
import os
from twilio.rest import Client


def send_template_message(to_number: str, template_sid: str, variables: dict):
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))

    response = client.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_FROM"),
        content_sid=template_sid,
        content_variables=str(variables).replace("'", '"'),
        to=f'whatsapp:{to_number}'
    )

    return response.sid