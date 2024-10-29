import sqlite3
import json
import os

class Database:
    def __init__(self, db_name='users.db', json_file='users.json'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.json_file = json_file
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                email TEXT,
                                password TEXT,
                                phone TEXT)''')
        self.conn.commit()

    def add_user(self, username, email, password, phone):
        self.cursor.execute("INSERT INTO users (username, email, password, phone) VALUES (?, ?, ?, ?)",
                            (username, email, password, phone))
        self.conn.commit()
        self.save_to_json(username, email, password, phone)

    def user_exists(self, username, email):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ? OR email = ?", (username, email))
        return self.cursor.fetchone()[0] > 0    

    def save_to_json(self, username, email, password, phone):
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "phone": phone
        }

        # Check if the JSON file exists
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as json_file:
                json.dump([], json_file)  # Create an empty list if the file does not exist

        # Append the new user data to the JSON file
        with open(self.json_file, 'r+') as json_file:
            data = json.load(json_file)
            data.append(user_data)
            json_file.seek(0)  # Move to the start of the file before writing
            json.dump(data, json_file, indent=4)  # Write the updated data with indentation
            
    def validate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None  # Returns True if user exists, otherwise False        

    def close(self):
        self.conn.close()
