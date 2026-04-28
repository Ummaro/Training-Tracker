TEST_ORDER = 30

from src.Strava import Strava
import json

if __name__ == "__main__":
        strava = Strava()
        client = strava.authenticate()
        if client:
            activity_id ='17962925643'
            laps = strava.get_laps(client, activity_id)

            with open("laps.json", "w") as f:
                json.dump(laps, f, default=str)

            if laps:
                if len(laps) != 7:
                    print(f"Expected 7 laps, got {len(laps)}")
                    exit(1)
                exit(0)
            else:
                print("No laps found for the specified activity")
                exit(1)
        else:
            print("Authentication failed")
            exit(1)