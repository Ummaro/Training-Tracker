import atexit
import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self._closed = False
        atexit.register(self.close)
        self.create_tables()

    def close(self):
        if self.connection and not self._closed:
            self.connection.close()
            self._closed = True
            self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    @staticmethod
    def _get_value(item, key):
        if isinstance(item, dict):
            return item[key]
        return getattr(item, key)

    @staticmethod
    def _row_to_dict(row):
        return dict(row) if row is not None else None
    
    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY,
                    athlete_id INTEGER,
                    average_speed REAL,
                    average_watts REAL,
                    distance REAL,
                    elapsed_time INTEGER,
                    manual INTEGER,
                    max_speed REAL,
                    max_watts REAL,
                    moving_time INTEGER,
                    name TEXT,
                    sport_type TEXT,
                    start_date TEXT,
                    total_elevation_gain REAL
                )
            ''')

        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS laps (
                id INTEGER PRIMARY KEY,
                activity_id INTEGER,
                athlete_id INTEGER,
                average_speed REAL,
                distance REAL,
                elapsed_time INTEGER,
                end_index INTEGER,
                lap_index INTEGER,
                max_speed REAL,
                moving_time INTEGER,
                split INTEGER,
                start_date TEXT,
                start_index INTEGER,
                total_elevation_gain REAL,
                average_watts REAL
            )
        ''')

        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS athlete (
                id INTEGER PRIMARY KEY,
                city TEXT,
                country TEXT,
                created_at TEXT,
                firstname TEXT,
                lastname TEXT,
                sex TEXT,
                state TEXT,
                measurement_preference TEXT,
                date_preference TEXT,
                email TEXT,
                email_language TEXT,
                username TEXT,
                dateofbirth TEXT,
                sample_race_distance REAL,
                sample_race_time INTEGER
            )
        ''')

        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS token (
                athlete_id INTEGER PRIMARY KEY,
                access_token TEXT,
                refresh_token TEXT,
                expires_at INTEGER
            )
        ''')

        return True

    def insert_activity(self, activity):
        with self.connection:
            self.connection.execute('''
                INSERT INTO activities (id, athlete_id, average_speed, average_watts, distance, elapsed_time, manual, max_speed, max_watts, moving_time, name, sport_type, start_date, total_elevation_gain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self._get_value(activity, "id"),
                self._get_value(activity, "athlete_id"),
                self._get_value(activity, "average_speed"),
                self._get_value(activity, "average_watts"),
                self._get_value(activity, "distance"),
                self._get_value(activity, "elapsed_time"),
                self._get_value(activity, "manual"),
                self._get_value(activity, "max_speed"),
                self._get_value(activity, "max_watts"),
                self._get_value(activity, "moving_time"),
                self._get_value(activity, "name"),
                self._get_value(activity, "sport_type"),
                self._get_value(activity, "start_date"),
                self._get_value(activity, "total_elevation_gain")
            ))
        return True

    def insert_lap(self, lap, activity_id):
        with self.connection:
            self.connection.execute('''
                INSERT INTO laps (id, activity_id, athlete_id, average_speed, distance, elapsed_time, end_index, lap_index, max_speed, moving_time, split, start_date, start_index, total_elevation_gain, average_watts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    
            ''', (
                self._get_value(lap, "id"),
                activity_id,
                self._get_value(lap, "athlete_id"),
                self._get_value(lap, "average_speed"),
                self._get_value(lap, "distance"),
                self._get_value(lap, "elapsed_time"),
                self._get_value(lap, "end_index"),
                self._get_value(lap, "lap_index"),
                self._get_value(lap, "max_speed"),
                self._get_value(lap, "moving_time"),
                self._get_value(lap, "split"),
                self._get_value(lap, "start_date"),
                self._get_value(lap, "start_index"),
                self._get_value(lap, "total_elevation_gain"),
                self._get_value(lap, "average_watts")
            ))
        return True

    def insert_athlete(self, athlete):
        with self.connection:
            self.connection.execute('''
                INSERT OR REPLACE INTO athlete (id, city, country, created_at, firstname, lastname, sex, state, measurement_preference, date_preference, email, email_language, username, dateofbirth, sample_race_distance, sample_race_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                athlete.get("id") if isinstance(athlete, dict) else getattr(athlete, "id", None),
                athlete.get("city") if isinstance(athlete, dict) else getattr(athlete, "city", None),
                athlete.get("country") if isinstance(athlete, dict) else getattr(athlete, "country", None),
                athlete.get("created_at") if isinstance(athlete, dict) else getattr(athlete, "created_at", None),
                athlete.get("firstname") if isinstance(athlete, dict) else getattr(athlete, "firstname", None),
                athlete.get("lastname") if isinstance(athlete, dict) else getattr(athlete, "lastname", None),
                athlete.get("sex") if isinstance(athlete, dict) else getattr(athlete, "sex", None),
                athlete.get("state") if isinstance(athlete, dict) else getattr(athlete, "state", None),
                athlete.get("measurement_preference") if isinstance(athlete, dict) else getattr(athlete, "measurement_preference", None),
                athlete.get("date_preference") if isinstance(athlete, dict) else getattr(athlete, "date_preference", None),
                athlete.get("email") if isinstance(athlete, dict) else getattr(athlete, "email", None),
                athlete.get("email_language") if isinstance(athlete, dict) else getattr(athlete, "email_language", None),
                athlete.get("username") if isinstance(athlete, dict) else getattr(athlete, "username", None),
                athlete.get("dateofbirth") if isinstance(athlete, dict) else getattr(athlete, "dateofbirth", None),
                athlete.get("sample_race_distance") if isinstance(athlete, dict) else getattr(athlete, "sample_race_distance", None),
                athlete.get("sample_race_time") if isinstance(athlete, dict) else getattr(athlete, "sample_race_time", None)
            ))
        return True

    def insert_token(self, token, athlete_id=None):
        if athlete_id is None:
            athlete_id = self._get_value(token, "athlete_id")
        with self.connection:
            self.connection.execute('''
                INSERT OR REPLACE INTO token (athlete_id, access_token, refresh_token, expires_at)
                VALUES (?, ?, ?, ?)
            ''', (
                athlete_id,
                self._get_value(token, "access_token"),
                self._get_value(token, "refresh_token"),
                self._get_value(token, "expires_at")
            ))
        return True

    def get_activities_by_athlete_id(self, athlete_id):
        cursor = self.connection.execute('SELECT * FROM activities WHERE athlete_id = ?', (athlete_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_laps_by_activity_id(self, activity_id):
        cursor = self.connection.execute('SELECT * FROM laps WHERE activity_id = ?', (activity_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_athlete_by_id(self, athlete_id):
        cursor = self.connection.execute('SELECT * FROM athlete WHERE id = ?', (athlete_id,))
        return self._row_to_dict(cursor.fetchone())

    def get_athlete(self, athlete_id):
        return self.get_athlete_by_id(athlete_id)
    
    def get_token_by_athlete_id(self, athlete_id):
        cursor = self.connection.execute('SELECT * FROM token WHERE athlete_id = ? ORDER BY expires_at DESC', (athlete_id,))
        return self._row_to_dict(cursor.fetchone())