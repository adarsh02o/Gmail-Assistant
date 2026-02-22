from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Path to your credentials JSON
CREDENTIALS_FILE = "./credentials.json"
# We need 'modify' scope to read emails AND create labels/move emails
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Error: {CREDENTIALS_FILE} not found.")
        print("Please download your OAuth 2.0 Client credentials from Google Cloud Console.")
        print("Save the file as 'credentials.json' in this directory.")
        return

    # Load previously saved credentials if available
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, generate them
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the future
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    print("Tokens generated and saved to 'token.pickle'!")

if __name__ == '__main__':
    main()
