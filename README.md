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

## 🔐 Environment Setup

### 4. .env File
Create a .env file in the root directory, if it already exists then update it:

```
# Twilio
TWILIO_SID=your_twilio_sid
TWILIO_AUTH=your_twilio_auth
TWILIO_FROM=your_from_number
TWILIO_TO=+your_phone_number

# WhatsApp via Twilio
WHATSAPP_FROM=whatsapp:your_from_number
WHATSAPP_TO=whatsapp:your_phone_number

# Gemini API
GEMINI_API_KEY=your_gemini_api_key
```

## 📧 Gmail & Calendar API Setup

### Step 1: Enable APIs
* Visit Google Cloud Console
* Create a project
* Enable:
  * Gmail API
  * Google Calendar API

### Step 2: Create OAuth 2.0 Credentials
* Go to APIs & Services → Credentials
* Create OAuth client ID (Desktop App)
* Download credentials.json
* Place it in:
```
config/credentials.json
```

### Step 3: Run Auth Once to Generate Token
```
python gmail/gmail_reader.py
```

## 🌐 Ngrok (for WhatsApp Webhook)
```
ngrok http 5000
```
Use the generated URL (e.g., https://abc123.ngrok.io) to configure Twilio WhatsApp webhook as:
```
https://abc123.ngrok.io/webhook
```

## 💻 Running the App
Run the Webhook Server:
```
python webhook/webhook_handler.py
```
Run the Gmail Event Processor:
```
python main.py
```

✅ The program should be running and you should be able to see the logs in the terminals.

---

## 🧠 Sample Email Format
Gemini AI can parse various formats. Even this will work:
```
Subject: AI Course
Body: Your assignment is due this Sunday at 4 p.m.
```

Gemini will extract:
```
Event: AI Course Assignment
Date: 07.07.25
Time: 4:00 p.m.
Day: Sunday
```

---

## 📁 Project Structure




