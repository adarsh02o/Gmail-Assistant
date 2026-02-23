import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN_FILE = "token.pickle"
# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """Sends a message to the configured Telegram chat."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("Telegram Bot Token not configured. Skipping Telegram notification.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram notification sent successfully.")
        else:
            print(f"Failed to send Telegram notification: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def get_service():
    """Authenticates and returns the Gmail service."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Invalid token. Please regenerate it using generate_token.py")
            return None

    return build('gmail', 'v1', credentials=creds)

def fetch_emails(service, query="is:unread", max_results=5):
    """Searches for emails matching the query."""
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        return messages
    except Exception as e:
        print(f"An error occurred while fetching emails: {e}")
        return []

def get_email_details(service, msg_id):
    """Gets headers (Subject, From) and snippet from a message ID."""
    try:
        message = service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
        snippet = message.get('snippet', '')
        return {'id': msg_id, 'subject': subject, 'sender': sender, 'date': date, 'snippet': snippet}
    except Exception as e:
        print(f"Error getting details for message {msg_id}: {e}")
        return None

def create_label(service, label_name):
    """Creates a new label if it doesn't exist, returns the label ID."""
    try:
        # First check if label exists
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        for label in labels:
            if label['name'].lower() == label_name.lower():
                return label['id']
        
        # Create if not found
        label_object = {'name': label_name, 'labelListVisibility': 'labelShow', 'messageListVisibility': 'show'}
        created_label = service.users().labels().create(userId='me', body=label_object).execute()
        return created_label['id']
    except Exception as e:
        print(f"Error creating/finding label: {e}")
        return None

def move_email_to_label(service, msg_id, label_id):
    """Moves an email to a specific label (folder) by adding the label and removing from INBOX."""
    try:
        body = {
            'addLabelIds': [label_id],
            'removeLabelIds': ['INBOX']
        }
        service.users().messages().modify(userId='me', id=msg_id, body=body).execute()
        print(f"Moved email {msg_id} to label ID {label_id}")
    except Exception as e:
        print(f"Error moving email: {e}")

def main():
    service = get_service()
    if not service:
        return

    print("--- Gmail Automator ---")
    report = "📧 *Gmail Automator Report*\n"

    # --- JOB HUNT MODE ---
    # 1. Job Application Updates (Interviews, Shortlists, HR Replies)
    print("\n🔍 Checking for Job Application Updates...")
    job_queries = [
        'subject:(interview OR shortlisted OR "next steps" OR scheduled OR "moving forward" OR invitation)', 
        '("talent acquisition" OR recruiter OR "hiring team") -category:promotions',
        'subject:(assessment OR test OR exam OR coding OR challenge) (hackerrank OR leetcode OR codility OR glider OR "test link")'
    ]
    
    found_job_emails = []
    seen_ids = set()

    for q in job_queries:
        msgs = fetch_emails(service, query=f"{q} is:unread", max_results=5)
        for m in msgs:
            if m['id'] not in seen_ids:
                found_job_emails.append(m)
                seen_ids.add(m['id'])

    if found_job_emails:
        report += "\n🚀 *Job Updates (Interviews/Assessments):*\n"
        print(f"Found {len(found_job_emails)} job-related emails.")
        for msg in found_job_emails:
            details = get_email_details(service, msg['id'])
            if details:
                # Add an extra "URGENT" tag if it looks like an interview or test
                prefix = ""
                subject_lower = details['subject'].lower()
                if any(x in subject_lower for x in ['test', 'assessment', 'exam', 'hackerrank']):
                    prefix = "📝 [TEST LINK] "
                elif any(x in subject_lower for x in ['interview', 'schedule', 'meet']):
                    prefix = "📅 [INTERVIEW] "
                
                report += f" • {prefix}{details['subject']} (from {details['sender']})\n"
                print(f" - {prefix}{details['subject']}")
    else:
        print("No specific job updates found.")

    # 2. General "Important" Filter
    keyword = "important"

    print(f"\nSearching for emails with keyword: '{keyword}'...")
    messages = fetch_emails(service, query=keyword, max_results=3)

    if messages:
        report += f"\n🔍 *Found {len(messages)} '{keyword}' emails:*\n"
        print(f"Found {len(messages)} emails:")
        for msg in messages:
            details = get_email_details(service, msg['id'])
            if details:
                report += f" • {details['subject']} (from {details['sender']})\n"
                print(f" - [{details['date']}] {details['sender']}: {details['subject']}")
    else:
        report += f"\n🔍 No emails found with keyword '{keyword}'.\n"
        print("No emails found with that keyword.")

    # 2. Sort Promotional Emails: Find 'category:promotions' and move them to a label "Promo_Processed"
    print("\nProcessing promotional emails...")
    promo_msgs = fetch_emails(service, query="category:promotions is:unread", max_results=2)
    
    if promo_msgs:
        promo_label_id = create_label(service, "Promo_Processed")
        if promo_label_id:
            count = 0
            for msg in promo_msgs:
                details = get_email_details(service, msg['id'])
                print(f" - Moving '{details['subject']}' to 'Promo_Processed'...")
                move_email_to_label(service, msg['id'], promo_label_id)
                count += 1
            report += f"\n🧹 Moved {count} promotional emails to 'Promo_Processed'.\n"
    else:
        report += "\n🧹 No new promotional emails to sort.\n"
        print("No new promotional emails to sort.")

    # 3. Daily Summary: List unread emails from the last 24 hours
    print("\n--- Daily Email Summary (Last 24h) ---")
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
    # search for emails after yesterday
    daily_msgs = fetch_emails(service, query=f"after:{yesterday} is:unread", max_results=10)
    
    if daily_msgs:
        report += "\n📅 *Daily Summary (Last 24h):*\n"
        for msg in daily_msgs:
            details = get_email_details(service, msg['id'])
            report += f" • {details['subject']} (from {details['sender']})\n"
            print(f"FROM: {details['sender']}\nSUBJ: {details['subject']}\n--")
    else:
        report += "\n📅 No new unread emails in the last 24 hours.\n"
        print("No new unread emails in the last 24 hours.")

    send_telegram_message(report)

if __name__ == '__main__':
    main()
