TEST_ORDER = 60

from src.Server import Server
import requests

if __name__ == "__main__":
    server = Server(dev=True)
    server.run()

    request = requests.post("http://localhost:5000/strava/webhook", json={
        "aspect_type": "create",
        "event_time": 1234567890,
        "object_id": 17962925643,
        "object_type": "activity",
        "owner_id": 1355550282,
        "subscription_id": 1234567890
    })

    if not (request.status_code == 200 and request.text == "EVENT_RECEIVED"):
        exit(1)

    if server.strava.db.get_activity(activity_id=17962925643) is None:
        exit(1)
    
    if server.strava.db.get_laps_by_activity_id(activity_id=17962925643) is None:
        exit(1)

    exit(0)