# Import the modules
import schedule
import time
import subprocess
import os
import schedule
from schedule import Job
import os
import sys

# Define the function to run the exe file
def run_exe():
    # Replace the path with your exe file path
    subprocess.run(r"C:\Users\Administrator\Documents\StockScanner\PythonTechnicalScanner_STRONG_BUY_1H_KMI100.exe")

# Schedule the function to run every hour from 07:00 AM to 03:00 PM on weekdays
pid = os.spawnl(os.P_DETACH, sys.executable, *sys.argv)

if pid > 0:
    # Exit the parent process
    exit(0)

# Loop until the program is terminated
while True:
    # Run the pending tasks
    schedule.run_pending()
    # Wait for one second
    time.sleep(1)