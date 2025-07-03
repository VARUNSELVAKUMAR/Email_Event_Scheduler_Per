from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    token_path = 'config/calendar_token.pickle'

    # 🔁 Load token if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # 🔐 Login if no token or invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # ✅ Ensure config folder exists before saving token
        os.makedirs(os.path.dirname(token_path), exist_ok=True)

        # 💾 Save new token
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def schedule_event(event):
    """
    Expects event dict:
    {
        "event": "Interview with IBM",
        "date": "03.07.25",
        "time": "2:30 p.m.",
        "day": "Thursday"
    }
    """
    service = get_calendar_service()

    # Convert string to datetime
    date_str = event["date"]
    time_str = event["time"].strip().lower()
    time_str = time_str.replace("a.m.", "am").replace("p.m.", "pm").replace(".", "")

    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%y %I:%M %p")
    except Exception as e:
        print(f"❌ Date/time parsing error: {e}")
        return



    start_time = dt.isoformat()
    end_time = (dt + timedelta(hours=1)).isoformat()  # assume 1-hour duration

    event_body = {
        'summary': event["event"],
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 15}
            ]
        }
    }

    service.events().insert(calendarId='primary', body=event_body).execute()
    print(f"📅 Event scheduled: {event['event']} on {event['date']} at {event['time']}")