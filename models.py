import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('chat.db', check_same_thread=False)
        self.create_user_table()
        self.create_message_table()

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def create_message_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Message" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            username TEXT NOT NULL,
            color TEXT DEFAULT '#000000',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            color TEXT DEFAULT '#3498db',
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(query)


class MessageModel:
    TABLENAME = "Message"

    def __init__(self):
        self.conn = sqlite3.connect('chat.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        query = f"SELECT * FROM {self.TABLENAME} WHERE id = ?"
        result_set = self.conn.execute(query, (_id,)).fetchall()
        if result_set:
            return [{column: row[i] for i, column in enumerate(result_set[0].keys())}
                    for row in result_set][0]
        return None

    def create(self, params):
        query = f"INSERT INTO {self.TABLENAME} (content, username, color) VALUES (?, ?, ?)"
        result = self.conn.execute(query, (
            params.get("content"),
            params.get("username"),
            params.get("color", "#000000")
        ))
        self.conn.commit()
        return self.get_by_id(result.lastrowid)

    def list_messages(self, limit=100):
        query = f"SELECT * FROM {self.TABLENAME} ORDER BY timestamp DESC LIMIT ?"
        result_set = self.conn.execute(query, (limit,)).fetchall()
        result = [{column: row[i] for i, column in enumerate(result_set[0].keys())}
                 for row in result_set] if result_set else []
        return result[::-1]  # Reverse to get chronological order


class UserModel:
    TABLENAME = "User"

    def __init__(self):
        self.conn = sqlite3.connect('chat.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def get_by_username(self, username):
        query = f"SELECT * FROM {self.TABLENAME} WHERE username = ?"
        result_set = self.conn.execute(query, (username,)).fetchall()
        if result_set:
            return [{column: row[i] for i, column in enumerate(result_set[0].keys())}
                    for row in result_set][0]
        return None

    def create_or_update(self, username, color="#3498db"):
        user = self.get_by_username(username)
        if user:
            # Update existing user
            query = f"UPDATE {self.TABLENAME} SET color = ?, last_active = CURRENT_TIMESTAMP WHERE username = ?"
            self.conn.execute(query, (color, username))
        else:
            # Create new user
            query = f"INSERT INTO {self.TABLENAME} (username, color) VALUES (?, ?)"
            self.conn.execute(query, (username, color))
        self.conn.commit()
        return self.get_by_username(username)

    def update_username(self, old_username, new_username):
        # First check if the new username is already taken
        if self.get_by_username(new_username):
            return {"error": "Username already taken"}

        # Get the user's color
        user = self.get_by_username(old_username)
        if not user:
            return {"error": "User not found"}

        # Update username in User table
        query = f"UPDATE {self.TABLENAME} SET username = ? WHERE username = ?"
        self.conn.execute(query, (new_username, old_username))

        # Update username in Message table
        query = f"UPDATE Message SET username = ? WHERE username = ?"
        self.conn.execute(query, (new_username, old_username))
        
        self.conn.commit()
        return self.get_by_username(new_username)

    def update_color(self, username, color):
        # Update color in User table
        query = f"UPDATE {self.TABLENAME} SET color = ? WHERE username = ?"
        self.conn.execute(query, (color, username))

        # Update color in recent messages
        query = f"UPDATE Message SET color = ? WHERE username = ?"
        self.conn.execute(query, (color, username))
        
        self.conn.commit()
        return self.get_by_username(username)
