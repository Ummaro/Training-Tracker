import flask
import threading
import time
from src.Strava import Strava

class Server:
    def __init__(self, dev=True):
        self.app = flask.Flask(__name__)
        self.strava = Strava(dev=dev)

        if dev:
            self.debug = True
            self.port = 5000
            self.host = "localhost"
        else:
            self.debug = False
            self.port = 8000
            self.host = "0.0.0.0"
    
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route("/authorization")
        def authorization():
            code = flask.request.args.get("code")
            if not code:
                return "Missing code", 400

            success = self.strava.authenticate(code=code)
            if success:
                return "Authentication successful", 200
            else:
                return "Authentication failed", 500
            
        @self.app.route("/authenticate")
        def authenticate():
            url = self.strava.generate_url()
            return flask.redirect(url)
        
    def run(self):
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        time.sleep(1)