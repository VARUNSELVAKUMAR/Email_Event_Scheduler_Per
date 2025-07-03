from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import os
import pickle
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def read_latest_emails():
    creds = None
    token_path = 'config/token.pickle'

    # ✅ Load token if it exists
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # 🔒 If no token or expired, run OAuth login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        os.makedirs(os.path.dirname(token_path), exist_ok=True)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    # ✅ Build Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # 📬 Get unread messages
    results = service.users().messages().list(userId='me', q='in:inbox is:unread').execute()
    messages = results.get('messages', [])

    if not messages:
        return []

    # 📥 Parse each unread email's content
    structured_emails = []

    for msg in messages:
        msg_id = msg['id']
        msg_data = service.users().messages().get(userId='me', id=msg_id).execute()
        payload = msg_data.get('payload', {})
        parts = payload.get('parts', [])

        email_text = ""

        # 🧠 If multipart
        if parts:
            for part in parts:
                if part.get('mimeType') == 'text/html':
                    data = part['body']['data']
                    decoded = base64.urlsafe_b64decode(data).decode('utf-8')
                    soup = BeautifulSoup(decoded, "html.parser")
                    email_text = soup.get_text()
                    break
        else:
            # 🧠 Fallback for single part emails
            body = payload.get('body', {}).get('data')
            if body:
                decoded = base64.urlsafe_b64decode(body).decode('utf-8')
                soup = BeautifulSoup(decoded, "html.parser")
                email_text = soup.get_text()

        structured_emails.append({
            "id": msg_id,
            "content": email_text
        })

    return structured_emails