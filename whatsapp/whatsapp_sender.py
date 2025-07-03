from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")


client = Client(TWILIO_SID, TWILIO_AUTH)

def send_event_message(event_data):
    message = f"""
{event_data}

Reply with "Schedule" or "Don't Schedule".
"""
    msg = client.messages.create(
        body=message,
        from_ = WHATSAPP_FROM,
        to = WHATSAPP_TO
    )
    return msg.sid