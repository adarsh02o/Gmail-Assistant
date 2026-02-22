import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def main():
    # Load the token file
    creds = None
    TOKEN_FILE = "token.pickle"
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Check if the credentials are valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Invalid token. Please regenerate it!")
            return

    # Authenticate and build the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    
    # Test: List the user's Gmail labels
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print("No labels found in the Gmail account.")
    else:
        print("Labels:")
        for label in labels:
            print(f"- {label['name']}")

if __name__ == '__main__':
    main()
