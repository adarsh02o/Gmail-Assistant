import pickle
import base64
import os

token_file = "token.pickle"

if os.path.exists(token_file):
    with open(token_file, "rb") as token:
        creds = pickle.load(token)
        # Pickle the credentials object to bytes
        pickled_data = pickle.dumps(creds)
        # Encode bytes to base64 string
        b64_token = base64.b64encode(pickled_data).decode('utf-8')
        print("\n=== YOUR GMAIL_TOKEN_BASE64 SECRET ===")
        print(b64_token)
        print("======================================\n")
        print("Copy everything between the lines above and paste it into GitHub Secrets as GMAIL_TOKEN_BASE64")
else:
    print(f"Error: {token_file} not found. format_token.py must be run in the same directory as token.pickle")
