from stravalib.client import Client
from dotenv import load_dotenv
import os


def setup_strava_webhook():
    client = Client()
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")

    callback_url = os.getenv("PROD_URL") + "/strava/webhook"

    verify_token = os.getenv("STRAVA_VERIFY_TOKEN")

    try:
        response = client.create_subscription(
            client_id=client_id,
            client_secret=client_secret,
            callback_url=callback_url,
            verify_token=verify_token
        )
        print(f"Subscription created: {response.id}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load_dotenv()
    setup_strava_webhook()