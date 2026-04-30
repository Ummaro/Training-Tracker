TEST_ORDER = 0

from src.Database import Database
from src.Strava import Strava

if __name__ == "__main__":
    strava = Strava()
    db = strava.db

    activity = {
        "id": 17962925642,
        "athlete": {"id": 1355550282},
        "name": "Lunch Run",
        "sport_type": {"root": "Run"},
        "distance": 6009.0,
        "moving_time": 1990,
        "elapsed_time": 2065,
        "total_elevation_gain": 70.4,
        "average_speed": 3.02,
        "max_speed": 9.88,
        "average_watts": 329.4,
        "max_watts": 535.0,
        "manual": False,
        "start_date": "2026-03-25T11:19:55Z"
    }

    lap = {
        "id": 64246604952,
        "activity_id": 17962925642,
        "athlete": {"id": 1355550282},
        "lap_index": 1,
        "split": 1,
        "distance": 1000.0,
        "moving_time": 318,
        "elapsed_time": 321,
        "total_elevation_gain": 18.6,
        "average_speed": 3.14,
        "max_speed": 9.88,
        "average_watts": 343.1,
        "start_date": "2026-03-25T11:19:55Z",
        "start_index": 0,
        "end_index": 326
    }

    athlete = {
        "id": 1355550282,
        "firstname": "DEV",
        "lastname": "Ummaro",
        "city": "Paris",
        "state": "Île-de-France",
        "country": "France",
        "created_at": "2026-04-03T14:09:05Z",
        "sex": None,
        "measurement_preference": None,
        "date_preference": None,
        "email": None,
        "email_language": None,
        "username": None,
        "dateofbirth": None,
        "sample_race_distance": None,
        "sample_race_time": None
    }

    token = {
        "athlete_id": 1355550282,
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
    if not athlete_from_db or athlete_from_db != athlete:
        print("Failed to retrieve athlete")
        exit(1)

    token_from_db = db.get_token_by_athlete_id(token["athlete_id"])
    if not token_from_db or token_from_db.get("athlete_id") != token["athlete_id"]:
        print("Failed to retrieve token")
        exit(1)
    
    activities_from_db = db.get_activities_by_athlete_id(athlete["id"])
    if len(activities_from_db) != 1 or activities_from_db[0]["id"] != activity["id"]:
        print("Failed to retrieve activities")
        exit(1)

    laps_from_db = db.get_laps_by_activity_id(activity["id"])
    if len(laps_from_db) != 1 or laps_from_db[0]["id"] != lap["id"]:
        print("Failed to retrieve laps")
        exit(1)

    exit(0)