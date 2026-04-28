import flask
import threading
import time
from waitress import serve
from src.Strava import Strava

class Server:
    def __init__(self, dev=True):
        self.app = flask.Flask(__name__)
        self.strava = Strava(dev=dev)
        self.dev = dev
        
        if self.dev:
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
            if self.dev:
                thread = threading.Thread(
                    target=serve, 
                    args=(self.app,), 
                    kwargs={'host': self.host, 'port': self.port, '_quiet': True},
                    daemon=True
                )
                thread.start()
                time.sleep(1)
                print(f"Serveur de TEST démarré sur {self.host}:{self.port}")
            else:
                print(f"Serveur PROD démarré sur {self.host}:{self.port}")
                serve(self.app, host=self.host, port=self.port)