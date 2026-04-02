TEST_ORDER = 30

from src.Strava import Strava

if __name__ == "__main__":
        strava = Strava()
        if strava.authenticate():
            activity_id ='17941186814'
            laps = strava.get_laps(activity_id)
            if laps:
                if len(laps) != 18:
                    print(f"Expected 18 laps, got {len(laps)}")
                    exit(1)
                exit(0)
            else:
                print("No laps found for the specified activity")
                exit(1)
        else:
            print("Authentication failed")
            exit(1)