TEST_ORDER = 20

from src.Strava import Strava
import datetime

if __name__ == "__main__":
    strava = Strava()
    client = strava.authenticate()
    if client:
        activities = strava.get_activities(client, limit=2)
        if len(activities) != 2:
            print(f"Expected 2 activities, got {len(activities)}")
            exit(1)
        
        after = datetime.datetime(2026, 3, 25, tzinfo=datetime.timezone.utc)
        before = datetime.datetime(2026, 3, 26, tzinfo=datetime.timezone.utc)
        activities = strava.get_activities(client, after=after, before=before)
        if activities:
            for activity in activities:
                if activity.start_date < after or activity.start_date > before:
                    print(f"Activity {activity.id} has start date {activity.start_date} outside of range")
                    exit(1)

            exit(0)
        else:
            print("No activities found in the specified date range")
            exit(1)
    else:
        print("Authentication failed")
        exit(1)