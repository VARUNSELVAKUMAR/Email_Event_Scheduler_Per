from flask import Flask, request, jsonify
from dotenv import load_dotenv
from calendar_api.google_calendar import schedule_event
from call.twilio_caller import schedule_call
from collections import deque
import os

load_dotenv()
app = Flask(__name__)

# Queue to store multiple events
event_queue = deque()

@app.route("/")
def home():
    return "✅ Webhook is running!"

@app.route("/set_event", methods=["POST"])
def set_event():
    event_data = request.json
    event_queue.append(event_data)
    print(f"📥 New event added to queue:\n{event_data}")
    return jsonify({"status": "event stored"}), 200

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    if not event_queue:
        return "⚠️ No events in queue.", 200

    incoming_msg = request.values.get("Body", "").strip().lower()
    print(f"📨 WhatsApp: {incoming_msg}")

    current_event = event_queue[0]

    if incoming_msg in ["schedule", "yes", "y"]:
        try:
            print("✅ User approved event.")
            schedule_event(current_event)
            schedule_call(current_event)
            event_queue.popleft()
            return "✅ Event scheduled! Next one coming soon.", 200
        except Exception as e:
            print(f"💥 Schedule error: {e}")
            return "❌ Scheduling failed.", 500

    elif incoming_msg in ["no", "n", "don't", "dont"]:
        print("❌ User rejected event.")
        event_queue.popleft()
        return "❌ Event discarded. Next one coming soon.", 200

    else:
        print("🤖 Invalid input.")
        return "🤖 Reply with *Schedule* or *Don't Schedule*", 200

if __name__ == "__main__":
    try:
        app.run(port=5000)
    except Exception as e:
        print(f"💥 Flask error: {e}")