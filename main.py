import requests
import re
from datetime import datetime
from gmail.gmail_reader import read_latest_emails
from nlp.gemini_parser import extract_event_info
from whatsapp.whatsapp_sender import send_event_message
from utils.processed_tracker import load_processed_ids, save_processed_ids

def parse_event_text_to_json(text):
    lines = text.strip().split("\n")
    data = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip().lower()] = value.strip()

    return {
        "event": data.get("event", "Untitled Event"),
        "date": data.get("date", "01.01.70"),
        "time": data.get("time", "12:00 p.m."),
        "day": data.get("day", "Unknown")
    }

def is_future_event(event_json):
    try:
        time_str = event_json["time"].lower().replace(" ", "").replace(".", "")
        date_str = event_json["date"]

        if not re.search(r"\d{1,2}:\d{2}(a|p)m", time_str):
            return False, None

        time_str = time_str.replace("am", "AM").replace("pm", "PM")
        dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%y %I:%M%p")
        return dt > datetime.now(), dt
    except Exception as e:
        print("⛔ Invalid datetime format:", e)
        return False, None

def main():
    print("🔄 Checking for new emails...")
    emails = read_latest_emails()
    if not emails:
        print("📭 No unread emails found.")
        return

    processed_ids = load_processed_ids()
    updated_ids = processed_ids.copy()

    for email in emails:
        email_id = email["id"]
        content = email["content"]

        if email_id in processed_ids:
            print(f"⏩ Email {email_id} already processed.")
            continue

        extracted = extract_event_info(content)
        if not extracted:
            print("⚠️ Skipping: Gemini failed to extract event info.")
            continue

        print("🔍 Gemini Extracted:\n", extracted)

        try:
            event_json = parse_event_text_to_json(extracted)
        except Exception as e:
            print("❌ Failed to parse Gemini response:", e)
            continue

        is_future, dt = is_future_event(event_json)
        if not is_future:
            print(f"⏰ Skipping past or invalid event at {dt}")
            continue

        print(f"✅ Valid event at future time: {dt}")

        # 📤 Send WhatsApp message
        message = (
            f"You have a new event:\n\n{extracted}\n\n"
            "Reply with *Schedule* or *Don't Schedule*."
        )
        send_event_message(message)

        # 📩 Send to webhook for further scheduling
        try:
            response = requests.post("http://localhost:5000/set_event", json=event_json)
            print("📬 Webhook response:", response.status_code)
        except Exception as e:
            print("❌ Failed to send event to webhook:", e)

        # ✅ Mark this email as processed
        updated_ids.add(email_id)

    # 💾 Save processed email IDs
    save_processed_ids(updated_ids)
    print("✅ Done processing emails.")

if __name__ == "__main__":
    main()