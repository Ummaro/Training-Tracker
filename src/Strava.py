from stravalib import Client
from dotenv import load_dotenv
import os
import json

class Strava:
    def __init__(self, dev=True):
        load_dotenv()
        self.dev = dev
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        if self.dev:
            self.url = os.getenv("DEV_URL")
        else:
            self.url = os.getenv("PROD_URL")
        self.client = Client()

    def authenticate(self):
        #Dev only, should be replaced by db storage on prod
        token_file = os.path.join(self.project_root, "strava_token.json")
        if os.path.exists(token_file):
            try:
                with open(token_file, "r") as f:
                    token_data = json.load(f)
                    self.client = Client(
                        access_token=token_data["access_token"],
                        refresh_token=token_data["refresh_token"],
                        token_expires=token_data["expires_at"]
                    )
                    return True
            except Exception as e:
                print(f"Error loading token from file: {e}. Proceeding with authentication flow.")

        if self.dev:
            url = self.client.authorization_url(
                client_id=self.client_id,
                redirect_uri=f"{self.url}/authorization",
            )
            print(f"Dev environment: Please go to the following URL and authorize the application: {url}")
            code = input(f"Then enter the authorization code in url (code=###): ")

        else:
            #TODO Get code from url from a flask endpoint and pass it to this function
            code = PLACEHOLDER
        try:
            token_response = self.client.exchange_code_for_token(
                client_id=self.client_id, client_secret=self.client_secret, code=code
            )
        except Exception as e:
            print(f"Error exchanging code for token: {e}")
            return False

        access_token = token_response["access_token"]
        refresh_token = token_response["refresh_token"]
        expires_at = token_response["expires_at"]

        # replace with db storage on prod
        with open(token_file, "w") as f:
            json.dump({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at
            }, f)

        self.client = Client(access_token=access_token, refresh_token=refresh_token, token_expires=expires_at)
        return True

if __name__ == "__main__":
    strava = Strava()
    strava.authenticate()