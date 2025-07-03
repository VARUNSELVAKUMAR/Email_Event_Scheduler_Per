from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

client = Client(TWILIO_SID, TWILIO_AUTH)

# 🔁 Shared background scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def make_call(event_summary, event_time):
    try:
        message = f"Reminder: Your event '{event_summary}' is at {event_time.strftime('%I:%M %p')} today. Be prepared!"
        call = client.calls.create(
            twiml=f'<Response><Say>{message}</Say></Response>',
            to=TWILIO_TO,
            from_=TWILIO_FROM
        )
        print(f"📞 Call placed. SID: {call.sid}")
    except Exception as e:
        print(f"❌ Call failed: {e}")

def schedule_call(event_data):
    try:
        date_str = event_data["date"]
        time_str = event_data["time"].lower().replace(" ", "").replace(".", "")
        event_dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%y %I:%M%p")
        call_time = event_dt - timedelta(minutes=15)

        if call_time < datetime.now():
            print("⚠️ Skipping call: Already past.")
            return

        scheduler.add_job(
            make_call,
            'date',
            run_date=call_time,
            args=[event_data["event"], event_dt]
        )

        print(f"✅ Call scheduled for: {call_time.strftime('%d-%m-%Y %I:%M %p')}")
    except Exception as e:
        print(f"❌ Scheduling error: {e}")