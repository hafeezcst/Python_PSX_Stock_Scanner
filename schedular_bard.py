import schedule
import time
import subprocess
import datetime
import logging
import watchdog.observers
from watchdog.events import FileSystemEventHandler

logging.basicConfig(filename='scheduling_log.txt', level=logging.INFO)

def run_exe():
    logging.info("Exe execution started")
    try:
        subprocess.run(r"C:\Users\Administrator\Documents\StockScanner\PythonTechnicalScanner_STRONG_BUY_1H_KMI100.exe", check=True)  # Replace with your exe path
    except Exception as e:
        logging.error(f"Error running exe: {e}")
        # Consider additional actions, like sending notifications
    logging.info("Exe execution finished")

def check_time_and_day():
    try:
        current_time = datetime.datetime.now().time()
        current_weekday = datetime.datetime.now().weekday()
        return 7 <= current_time.hour < 15 and 0 <= current_weekday <= 4
    except Exception as e:
        logging.error(f"Error checking time and day: {e}")
        return False

schedule.every().hour.do(run_exe, condition=check_time_and_day)

class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Script has been modified, restart it
            subprocess.run(["python", "your_script_name.py"])  # Replace with your script name

observer = watchdog.observers.Observer()
observer.schedule(MyEventHandler(), path=".", recursive=False)
observer.start()

while True:
    schedule.run_pending()
    time.sleep(1)
