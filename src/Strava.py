from stravalib import Client
from stravalib.util.limiter import DefaultRateLimiter
from dotenv import load_dotenv
from src.Database import Database
import os
import json
import logging
import time

logging.getLogger("stravalib.util.limiter.SleepingRateLimitRule").setLevel(logging.ERROR)

class Strava:
    def __init__(self, dev=True):
        load_dotenv()
        self.dev = dev
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")

        if self.dev:
            self.url = os.getenv("DEV_URL")
            self.rate_limiter = DefaultRateLimiter(priority="high")
            temp_dir = os.path.join(self.project_root, "temp")
            self.db = Database(os.path.join(temp_dir, "strava_dev.db"))
        else:
            self.url = os.getenv("PROD_URL")
            self.rate_limiter = DefaultRateLimiter(priority="low")
            self.db = Database(os.path.join(self.project_root, "strava_prod.db"))

    def authenticate(self, code=None, athlete_id=None):
            client = Client(rate_limiter=self.rate_limiter)
            token_data = None

            if self.dev and not code and not athlete_id:
                token_file = os.path.join(self.project_root, "strava_token.json")
                if os.path.exists(token_file):
                    try:
                        with open(token_file, "r") as f:
                            token_data = json.load(f)
                    except Exception as e:
                        print(f"Error loading file: {e}")

            if code:
                try:
                    token_data = client.exchange_code_for_token(
                        client_id=self.client_id, client_secret=self.client_secret, code=code
                    )
                except Exception as e:
                    print(f"Error exchange: {e}")
                    return False
            
            elif athlete_id:
                token_data = self.db.get_token_by_athlete_id(athlete_id)
            
            if not token_data:
                if self.dev:
                    url = client.authorization_url(client_id=self.client_id, redirect_uri=f"{self.url}/authorization")
                    print(f"Authorize here: {url}")
                    code = input("Code: ")
                    return self.authenticate(code=code)
                return False

            client.access_token = token_data["access_token"]
            client.refresh_token = token_data["refresh_token"]
            client.token_expires = token_data["expires_at"]

            if time.time() >= client.token_expires:
                token_data = self.refresh_token(client, athlete_id)
                if not token_data: return False

            if code and not self.dev:
                athlete = self.get_athlete(client)
                self.db.insert_token({
                    "athlete_id": athlete.id,
                    "access_token": token_data["access_token"],
                    "refresh_token": token_data["refresh_token"],
                    "expires_at": token_data["expires_at"],
                })
                self.db.insert_athlete(athlete)

            return client

    def refresh_token(self, client, athlete_id):
        try:
            res = client.refresh_access_token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                refresh_token=client.refresh_token
            )
            token_data = {
                "access_token": res["access_token"],
                "refresh_token": res["refresh_token"],
                "expires_at": res["expires_at"]
            }
            
            if athlete_id:
                db_data = token_data.copy()
                db_data["athlete_id"] = athlete_id
                self.db.insert_token(db_data)

            if self.dev:
                token_file = os.path.join(self.project_root, "strava_token.json")
                with open(token_file, "w") as f:
                    json.dump(token_data, f)
            
            return token_data
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None

    def get_activities(self, client, after=None, before=None, limit=None):
        try:
            activities = client.get_activities(after=after, before=before, limit=limit)
            return list(activities)
        except Exception as e:
            print(f"Error fetching activities: {e}")
            return []

    def get_laps(self, client, activity_id):
        try:
            laps = client.get_activity_laps(activity_id)
            return list(laps)
        except Exception as e:
            print(f"Error fetching laps for activity {activity_id}: {e}")
            return []
        
    def deauthorize(self, client):
        try:
            client.deauthorize()
            token_file = os.path.join(self.project_root, "strava_token.json")
            if os.path.exists(token_file):
                os.remove(token_file)
            return True
        except Exception as e:
            print(f"Error during deauthorization: {e}")
            return False

    def get_athlete(self, client):
        try:
            athlete = client.get_athlete()
            return athlete
        except Exception as e:
            print(f"Error fetching athlete information: {e}")
            return None