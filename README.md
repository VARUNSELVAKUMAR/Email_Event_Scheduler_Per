# 📅 Event Scheduler App

Automatically reads **event-related Gmail emails**, extracts event details using **Gemini AI**, sends a **WhatsApp confirmation message**, and on approval:

- Schedules a **Google Calendar** event
- Schedules a **Twilio phone call** as a reminder

---

## 🚀 Features

✅ Read unread Gmail emails  
✅ Use Gemini AI to extract event name, date, time, and day  
✅ Send WhatsApp message with confirmation buttons  
✅ On approval:
  - 📆 Schedule Google Calendar event with 15-min alert
  - 📞 Schedule Twilio call 15 minutes before the event

---

## 🧩 Tech Stack

- Python
- Gmail API + Google Calendar API
- Gemini API (Google Generative AI)
- Twilio (WhatsApp + Voice Calls)
- Flask (Webhook handling)
- Ngrok (for local testing)

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/your-username/event-scheduler-app.git
cd event-scheduler-app
```

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Folder Structure
Ensure these folders exist:

```
mkdir -p config storage
```


