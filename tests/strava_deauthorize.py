TEST_ORDER = -1

from src.Strava import Strava

if __name__ == "__main__":
    strava = Strava()
    if strava.authenticate():
        if strava.deauthorize():
            if strava.get_athlete() is not None:
                print("Athlete information should not be retrievable after deauthorization")
                exit(1)
            exit(0)
        else:
            print("Deauthorization failed")
            exit(1)
    else:
        print("Authentication failed")
        exit(1)