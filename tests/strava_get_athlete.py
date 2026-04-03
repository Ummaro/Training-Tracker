TEST_ORDER = 40

from src.Strava import Strava

if __name__ == "__main__":
    strava = Strava()
    if strava.authenticate():
        athlete = strava.get_athlete()
        if athlete:
            if athlete.id != '1355550282'and athlete.firstname != 'DEV' and athlete.lastname != 'Ummaro':
                print("Retrieved athlete information does not match expected values")
                exit(1)
            exit(0)
        else:
            print("Failed to retrieve athlete information")
            exit(1)
    else:
        print("Authentication failed")
        exit(1)