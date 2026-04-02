TEST_ORDER = 10

from src.Strava import Strava

if __name__ == "__main__":
    strava = Strava()
    if strava.authenticate():
        exit(0)
    else:
        exit(1)