import sqlite3

class Database:
    def __init__(self, path: str) -> None:
        """
        Initial database with users data
        """
        self.connection = sqlite3.connect(path)

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        user_id TEXT NOT NULL,
        party TEXT NOT NULL DEFAULT "",
        organization TEXT NOT NULL DEFAULT ""
        );
        """)

        self.connection.commit()

    def about_user(self, user_id: str) -> list:
        """
        This function returns you user's data
        """
        self.cursor.execute(
            f"SELECT user_id, party, organization FROM users WHERE user_id = '{user_id}'")
        return self.cursor.fetchall()

    def new_user(self, user_id: str, group: str = "", org = "") -> None:
        """
        This function creates new user without stated group by default
        """
        self.cursor.execute(
            f"INSERT INTO users (user_id, party, organization) VALUES ('{user_id}', '{group}', '{org}')")
        self.connection.commit()

    def update_info(self, user_id: str, **args) -> None:
        for name, value in args.items():
            self.cursor.execute(
                f"UPDATE users SET {name} = '{value}' WHERE user_id = '{user_id}'")
        self.connection.commit()
