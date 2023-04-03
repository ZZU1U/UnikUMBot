from aiogram import Dispatcher
import sqlite3

class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)

        self.cursor = self.connection.cursor()
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        user_id TEXT NOT NULL,
        party TEXT NOT NULL
        );
        """)

        self.connection.commit()
    
    def about_user(self, user_id):
        self.cursor.execute(f"SELECT user_id, party FROM users WHERE user_id = '{user_id}'")
        return self.cursor.fetchall()
    
    def new_user(self, user_id, group=""):
        self.cursor.execute(f"INSERT INTO users (user_id, party) VALUES ('{user_id}', '{group}')")
        self.connection.commit()
    
    def update_info(self, user_id, **args):
        for name, value in args.items():
            self.cursor.execute(f"UPDATE users SET {name} = '{value}' WHERE user_id = '{user_id}'")
        self.connection.commit()


database = Database('database.db')

TOKEN = "6051725809:AAGVinByBrRgEo37-6J1EHx5sm7ZlNbdh-g"

dp = Dispatcher()