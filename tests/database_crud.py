TEST_ORDER = 0

from src.Database import Database
from src.Strava import Strava

if __name__ == "__main__":
    strava = Strava()
    db = strava.db

    activity = {
        "id": 123,
        "athlete_id": 456,
        "name": "Morning Run",
        "type": "Run",
        "distance": 5000.0,
        "moving_time": 1500,
        "elapsed_time": 1600,
        "total_elevation_gain": 50.0,
        "start_date": "2024-01-01T07:00:00Z",
        "start_date_local": "2024-01-01T08:00:00Z",
        "timezone": "(GMT+01:00) Europe/Berlin"
    }

    lap = {
        "id": 789,
        "activity_id": 123,
        "athlete_id": 456,
        "name": "Lap 1",
        "type": "Run",
        "distance": 1000.0,
        "moving_time": 300,
        "elapsed_time": 320,
        "total_elevation_gain": 10.0,
        "start_date": "2024-01-01T07:00:00Z",
        "start_date_local": "2024-01-01T08:00:00Z",
        "timezone": "(GMT+01:00) Europe/Berlin"
    }

    athlete = {
        "id": 456,
        "firstname": "John",
        "lastname": "Doe",
        "city": "Berlin",
        "state": "Berlin",
        "country": "Germany"
    }

    token = {
        "athlete_id": 456,
        "access_token": "test",
        "refresh_token": "test",
        "expires_at": 1700000000
    }

    if not db.create_tables():
        print("Failed to create database tables")
        exit(1)

    if not db.insert_athlete(athlete):
        print("Failed to insert athlete")
        exit(1)

    if not db.insert_token(token):
        print("Failed to insert token")
        exit(1)

    if not db.insert_activity(activity):
        print("Failed to insert activity")
        exit(1)

    if not db.insert_lap(lap, activity["id"]):
        print("Failed to insert lap")
        exit(1)

    athlete_from_db = db.get_athlete(athlete["id"])
    if athlete_from_db != athlete:
        print("Failed to retrieve athlete")
        exit(1)

    token_from_db = db.get_token_by_athlete_id(token["athlete_id"])
    if token_from_db != token:
        print("Failed to retrieve token")
        exit(1)
    
    activities_from_db = db.get_activities_by_athlete_id(athlete["id"])
    if len(activities_from_db) != 1 or activities_from_db[0] != activity:
        print("Failed to retrieve activities")
        exit(1)

    laps_from_db = db.get_laps_by_activity_id(activity["id"])
    if len(laps_from_db) != 1 or laps_from_db[0] != lap:
        print("Failed to retrieve laps")
        exit(1)

    exit(0)