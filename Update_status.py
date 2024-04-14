import os
import datetime

def update_directory_timestamp():
    current_directory = os.getcwd()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update opening timestamp
    with open(os.path.join(current_directory, 'timestamp.txt'), 'a') as file:
        file.write(f"Opened at: {timestamp}\n")
    
    # Perform operations in the current directory
    
    # Update closing timestamp
    with open(os.path.join(current_directory, 'timestamp.txt'), 'a') as file:
        file.write(f"Closed at: {timestamp}\n")

    # Call the function to update the directory timestamp
    update_directory_timestamp()
    # Get the status of the current directory
    status = os.stat(current_directory)

    # Extract the relevant information
    last_opened = datetime.datetime.fromtimestamp(status.st_atime).strftime("%Y-%m-%d %H:%M:%S")
    last_modified = datetime.datetime.fromtimestamp(status.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    last_saved = datetime.datetime.fromtimestamp(status.st_ctime).strftime("%Y-%m-%d %H:%M:%S")

    # Update the status parameters in the timestamp file
    with open(os.path.join(current_directory, 'timestamp.txt'), 'a') as file:
        file.write(f"Last opened: {last_opened}\n")
        file.write(f"Last modified: {last_modified}\n")
        file.write(f"Last saved: {last_saved}\n")