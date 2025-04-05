import os
import time
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pywhatkit as kit
from pytz import timezone

# Google API scope (read-only contacts access)
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

def get_google_contacts():
    creds = None
    token_file = 'token.json'  # Saved OAuth token
    
    # 1. Check for existing token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # 2. If no valid token, authenticate via browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh expired token
        else:
            # First-time auth (opens browser)
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_930514105564-fsj3sec5l4rnv4re1mstrf5tfmtr0flr.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for future runs
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    # 3. Fetch contacts with birthdays
    service = build('people', 'v1', credentials=creds)
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,phoneNumbers,birthdays'
    ).execute()
    
    contacts = []
    for person in results.get('connections', []):
        # Extract name
        name = person.get('names', [{}])[0].get('displayName', '')
        
        # Extract phone (prioritize mobile numbers)
        phones = person.get('phoneNumbers', [])
        phone = None
        for p in phones:
            num = p.get('value', '').replace(' ', '').replace('-', '')
            if num:
                if p.get('type') == 'mobile' or not phone:  # Prefer mobile
                    phone = num
                    if not phone.startswith('+') and len(phone) == 10:  # Indian format
                        phone = f"+91{phone}"
        
        # Extract birthday
        birthdays = person.get('birthdays', [])
        birthday = None
        if birthdays:
            bday = birthdays[0].get('date', {})
            if bday:
                try:
                    birthday = datetime(
                        year=bday.get('year', 2000),  # Default year if missing
                        month=bday['month'],
                        day=bday['day']
                    ).date()
                except:
                    pass
        
        if name and phone and birthday:
            contacts.append({
                'Name': name,
                'Phone': phone,
                'Birthday': birthday
            })
    
    return contacts

def send_whatsapp_message(phone, message):
    try:
        kit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=15,
            tab_close=True
        )
        print(f"✅ Sent to {phone}")
        return True
    except Exception as e:
        print(f"❌ Failed to send to {phone}: {str(e)}")
        return False

def main():
    print("🎂 Checking birthdays...")
    contacts = get_google_contacts()
    today = datetime.now(timezone('Asia/Kolkata')).date()
    
    birthday_contacts = [
        c for c in contacts
        if c['Birthday'].month == today.month 
        and c['Birthday'].day == today.day
    ]
    
    if not birthday_contacts:
        print(f"No birthdays today ({today.strftime('%d-%b')})")
        return
    
    print(f"🎉 Found {len(birthday_contacts)} birthdays today!")
    
    for contact in birthday_contacts:
        name = contact['Name']
        phone = contact['Phone']
        message = f"""🎈 Happy Birthday {name}! 🎂

Wishing you a fantastic day filled with joy and happiness! ❤️"""
        
        print(f"Sending to {name} ({phone})...")
        send_whatsapp_message(phone, message)
        # time.sleep(20)  # Avoid rate limits

if __name__ == '__main__':
    main()