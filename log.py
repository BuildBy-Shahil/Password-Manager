import datetime
import os

class Log:
    def __init__(self):
        appdata = os.getenv("APPDATA")
        dir = os.path.join(appdata, "Logs")
        os.makedirs(dir, exist_ok=True)
        self.file = os.path.join(dir, "status.log")
        self.now = ""

    def get_date_time(self):
        self.now = datetime.datetime.now()
        date = self.now.strftime("%Y-%m-%d")
        time = self.now.strftime("%H:%M:%S")
        return date, time

    def log_err(self,err):
        print("Error")
        date, time = self.get_date_time()
        with open(self.file, "a") as file:
            file.write(f"[{date}-{time}] -> {err}")