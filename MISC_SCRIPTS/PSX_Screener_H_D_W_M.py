import subprocess

# Define the paths to your Python scripts
script_paths = [
    'PythonTechnicalScanner_STRONG_BUY_1H_KMI100.py',
    'PythonTechnicalScanner_STRONG_BUY_D_KMI100.py',
    'PythonTechnicalScanner_STRONG_BUY_W_KMI100.py',
    'PythonTechnicalScanner_STRONG_BUY_M_KMI100.py',
]

# Iterate through the script paths and execute each script
for script_path in script_paths:
    try:
        # Execute the Python script
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script '{script_path}': {e}")
