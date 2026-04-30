import flask
import threading
import time
import os
from dotenv import load_dotenv
from waitress import serve
from src.Strava import Strava

class Server:
    def __init__(self, dev=True):
        load_dotenv()
        self.app = flask.Flask(__name__)
        self.app.secret_key = os.getenv("SECRET_KEY")
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

            client = self.strava.authenticate(code=code)
            if client:
                athlete_id = client.get_athlete().id
                flask.session['athlete_id'] = athlete_id
                return flask.redirect("/dashboard")
            else:
                return "Authentication failed", 500
            
        @self.app.route("/authenticate")
        def authenticate():
            url = self.strava.generate_url()
            return flask.redirect(url)
        
        @self.app.route("/dashboard")
        def dashboard():
            athlete_id = flask.session.get('athlete_id')
            if not athlete_id:
                return flask.redirect("/login")
            
        @self.app.route("/login")
        def login():
            return "Please authenticate <a href='/authenticate'>here</a>"
        
        @self.app.route('/strava/webhook', methods=['GET', 'POST'])
        def strava_webhook():
            if flask.request.method == 'GET':
                verify_token = os.getenv("STRAVA_VERIFY_TOKEN")
                mode = flask.request.args.get('hub.mode')
                token = flask.request.args.get('hub.verify_token')
                challenge = flask.request.args.get('hub.challenge')
                mode = flask.request.args.get('hub.mode')
                token = flask.request.args.get('hub.verify_token')
                challenge = flask.request.args.get('hub.challenge')

                if mode == 'subscribe' and token == verify_token:
                    return flask.jsonify({"hub.challenge": challenge}), 200
                return "Forbidden", 403

            if flask.request.method == 'POST':
                data = flask.request.json

                if data and data.get('object_type') == 'activity':
                    athlete_id = data.get('owner_id')
                    if athlete_id:
                        client = self.strava.authenticate(athlete_id=athlete_id)
                        if client:
                            activity_id = data.get('object_id')
                            if activity_id:
                                activity = self.strava.get_activity(client, activity_id)
                                if activity:
                                    self.strava.db.insert_activity(activity)
                                    laps = self.strava.get_laps(client, activity_id)
                                    for lap in laps:
                                        self.strava.db.insert_lap(lap, activity_id)

                return "EVENT_RECEIVED", 200
        
    def run(self):
            if self.dev:
                thread = threading.Thread(
                    target=serve, 
                    args=(self.app,), 
                    kwargs={'host': self.host, 'port': self.port, '_quiet': True},
                    daemon=True,
                )
                thread.start()
                time.sleep(1)
                print(f"Serveur de TEST démarré sur {self.host}:{self.port}")
                return thread
            else:
                print(f"Serveur PROD démarré sur {self.host}:{self.port}")
                return serve(self.app, host=self.host, port=self.port)