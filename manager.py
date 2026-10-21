import os
import sqlite3
from log import Log

class Manager:
    def __init__(self):
        self.logger = Log()
        try:
            appdata = os.getenv("APPDATA")
            path = os.path.join(appdata, "Pass manager")
            os.makedirs(path, exist_ok=True)
            file = os.path.join(path, "password.db")

            self.conn = sqlite3.connect(file)
            self.curr = self.conn.cursor()

            self.curr.execute("""CREATE TABLE IF NOT EXISTS password (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                site Text NOT NULL,
                                user_email Text NOT NULL,
                                password Text NOT NULL
                                 )""")

        except sqlite3.Error as e:
            self.logger.log_err(f"Table creation failed: {e}")

    def store_data(self, data):
        try:
            query = """INSERT INTO password(site, user_email, password) VALUES (?, ?, ?)"""
            self.curr.execute(query, [data[0], data[1], data[2]])
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.log_err(f"Database Insert failed. Error: {type(e).__name__}")

    def fetch_data(self):
        self.curr.execute("""SELECT * FROM password""")
        data = self.curr.fetchall()
        return data

    def fetch_data_by_sitename(self, sitename: str):
        if sitename.strip():
            self.curr.execute("""SELECT * FROM password WHERE site LIKE ?""", [f"%{sitename}%"])
        else:
            pass
        data = self.curr.fetchall()
        return data

    def fetch_by_user_email(self, u_e:str):
        if u_e.strip():
            self.curr.execute("""SELECT * FROM password WHERE user_email LIKE ?""", [f"%{u_e}%"])
        else:
            pass
        data = self.curr.fetchall()
        return data

    def get_password(self, id_: int):
        self.curr.execute("""SELECT password FROM password WHERE id = ?""", [id_])
        data = self.curr.fetchone()
        return data

    def get_by_id(self, id_:int):
        self.curr.execute("""SELECT * FROM password WHERE id = ?""", [id_])
        data = self.curr.fetchone()
        return data

    def delete_data(self, id_:int):
        try:
            self.curr.execute("""DELETE FROM password WHERE id = ?""", [id_])
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.log_err(f"Database deletion failed for entry ID: {id_}. Error {type(e).__name__}")

    def update_data(self, site, user, password, id_:int):
        try:
            self.curr.execute("""UPDATE password SET site = ?, user_email = ?, password = ? WHERE id = ?""", [site, user, password, id_])
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.log_err(f"Database update failed for entry ID: {id_}. Error {type(e).__name__}")
