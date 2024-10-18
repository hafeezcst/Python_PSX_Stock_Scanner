import time
def get_analysis_type():
    analysis_type = input("Select analysis type (M for Monthly, W for Weekly, D for Daily, H for Hourly, press Enter for default D): ").upper()
    
    if not analysis_type:
        time.sleep(2)
        analysis_type = "D"
        print(f"Selected analysis type: {analysis_type}")

    if analysis_type not in ["M", "W", "D", "4H","H"]:
        raise ValueError("Invalid analysis type. Please select M, W, D, 4H or H.")
    
    return analysis_type