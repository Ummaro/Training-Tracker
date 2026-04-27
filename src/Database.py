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
                    name TEXT,
                    type TEXT,
                    distance REAL,
                    moving_time INTEGER,
                    elapsed_time INTEGER,
                    total_elevation_gain REAL,
                    start_date TEXT,
                    start_date_local TEXT,
                    timezone TEXT
            )
        ''')

        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS laps (
                id INTEGER PRIMARY KEY,
                activity_id INTEGER,
                athlete_id INTEGER,
                name TEXT,
                type TEXT,
                distance REAL,
                moving_time INTEGER,
                elapsed_time INTEGER,
                total_elevation_gain REAL,
                start_date TEXT,
                start_date_local TEXT,
                timezone TEXT
            )
        ''')

        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS athlete (
                id INTEGER PRIMARY KEY,
                firstname TEXT,
                lastname TEXT,
                city TEXT,
                state TEXT,
                country TEXT
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
                INSERT INTO activities (id, athlete_id, name, type, distance, moving_time, elapsed_time, total_elevation_gain, start_date, start_date_local, timezone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self._get_value(activity, "id"),
                self._get_value(activity, "athlete_id"),
                self._get_value(activity, "name"),
                self._get_value(activity, "type"),
                self._get_value(activity, "distance"),
                self._get_value(activity, "moving_time"),
                self._get_value(activity, "elapsed_time"),
                self._get_value(activity, "total_elevation_gain"),
                self._get_value(activity, "start_date"),
                self._get_value(activity, "start_date_local"),
                self._get_value(activity, "timezone")
            ))
        return True

    def insert_lap(self, lap, activity_id):
        with self.connection:
            self.connection.execute('''
                INSERT INTO laps (id, activity_id, athlete_id, name, type, distance, moving_time, elapsed_time, total_elevation_gain, start_date, start_date_local, timezone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self._get_value(lap, "id"),
                activity_id,
                self._get_value(lap, "athlete_id"),
                self._get_value(lap, "name"),
                self._get_value(lap, "type"),
                self._get_value(lap, "distance"),
                self._get_value(lap, "moving_time"),
                self._get_value(lap, "elapsed_time"),
                self._get_value(lap, "total_elevation_gain"),
                self._get_value(lap, "start_date"),
                self._get_value(lap, "start_date_local"),
                self._get_value(lap, "timezone")
            ))
        return True

    def insert_athlete(self, athlete):
        with self.connection:
            self.connection.execute('''
                INSERT OR REPLACE INTO athlete (id, firstname, lastname, city, state, country)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self._get_value(athlete, "id"),
                self._get_value(athlete, "firstname"),
                self._get_value(athlete, "lastname"),
                self._get_value(athlete, "city"),
                self._get_value(athlete, "state"),
                self._get_value(athlete, "country")
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