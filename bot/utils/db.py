import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path="bot.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    language_code TEXT,
                    first_seen TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content_type TEXT,
                    text TEXT,
                    json_data TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            conn.commit()

    def log_user(self, user):
        with self.get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO users (user_id, username, full_name, language_code, first_seen)
                VALUES (?, ?, ?, ?, ?)
            """, (user.id, user.username, user.full_name, user.language_code, datetime.now()))
            conn.commit()

    def log_message(self, message):
        self.log_user(message.from_user)
        with self.get_connection() as conn:
            content_type = message.content_type
            text = message.text or message.caption or ""
            try:
                json_data = message.model_dump_json()
            except Exception:
                # Fallback if model_dump_json fails due to non-serializable types
                try:
                    import json
                    # Use model_dump to get a dict, then serialize manually
                    # exclude_none=True can help, and we can handle unknown types
                    data_dict = message.model_dump(exclude_none=True)
                    def custom_serializer(obj):
                        return str(obj)
                    json_data = json.dumps(data_dict, default=custom_serializer)
                except Exception as e:
                    json_data = json.dumps({"error": f"Failed to serialize message: {str(e)}"})
            
            cursor = conn.execute("""
                INSERT INTO messages (user_id, content_type, text, json_data, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (message.from_user.id, content_type, text, json_data, datetime.now()))
            conn.commit()
            return cursor.lastrowid

    def get_stats(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            return {"user_count": user_count}

    def get_recent_messages(self, limit=10):
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT m.id, u.full_name, m.text, m.timestamp 
                FROM messages m 
                JOIN users u ON m.user_id = u.user_id 
                ORDER BY m.timestamp DESC 
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def get_message_details(self, msg_id):
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT m.id, u.full_name, u.username, u.user_id, m.content_type, m.timestamp, m.text 
                FROM messages m 
                JOIN users u ON m.user_id = u.user_id 
                WHERE m.id = ?
            """, (msg_id,))
            return cursor.fetchone()

db = Database()
