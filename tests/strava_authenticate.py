TEST_ORDER = 10

from src.Strava import Strava
from src.Server import Server

if __name__ == "__main__":
    server = Server(dev=True)
    server.run()
    if not server.strava.authenticate():
        exit(1)

    strava = Strava()
    if not strava.authenticate():
        exit(1)
    
    exit(0)