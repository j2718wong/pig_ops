# generate_token.py
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', 
        SCOPES
    )
    
    # Use a fixed port instead of random
    creds = flow.run_local_server(
        host='localhost',
        port=8080,  # Fixed port
        authorization_prompt_message='Please visit this URL: {url}',
        success_message='The auth flow is complete; you may close this window.',
        open_browser=True
    )

    with open('token.json', 'w') as token:
        token.write(creds.to_json())
        print("✅ token.json created successfully!")

if __name__ == '__main__':
    main()
