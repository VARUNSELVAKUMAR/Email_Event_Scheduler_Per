from google.generativeai import GenerativeModel
import google.generativeai as genai
import re
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")

now = datetime.now()

def extract_event_info(email_text):
    prompt = f"""You are given with an email. Go through it and look for any event mentioned in it like interview, course, lecture or deadline.
    for example if the mail says "You have an interview with google at 4 p.m. tomorrow then in the event field you should mention "Interview With Google".
    or if the mail has "Artificial Intelligence Course" mentioined in the subject or any other place and if the mail says "Assignment due this Saturday", then in the event field yo should mention "Artificial Intelligence Assignment". 
    Now extract the information and mention it in the format:
    Event:
    Date: (dd.mm.yy)
    Time:
    Day:

    Note: In case a day is mentioned, like today r tomorrow then mention the respective date for that day in the "Date" field in the format dd.mm.yy, if any partiular day is mentioned like Sunday or Monday then mention the date of the upcoming specified day. If today or tomorrow is mentioned then check the date the mail was sent and respond accordingly, if it's today then then it'd be the same date, if it's tomorrow then it'd be the next date and so on.
    In case date is mentioned then mention the respective day in the "Day" field.

    In case you don't find any event then just respond with "None".

    Also mention the date with "a.m." or "p.m.", for example if the input is 23:25, then it should be "11:25 p.m.".

Return only the structured data in that exact format. If no event is found or if event has already happened, respond with: "None".

Here is the email: {email_text}
Here is the current date and time {now}
"""

    response = model.generate_content(prompt)
    content = response.text.strip()

    if content.lower() == "none" or "event:" not in content.lower():
        return None

    return content