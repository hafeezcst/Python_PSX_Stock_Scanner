import pandas as pd
import datetime
import os
import openpyxl

def read_csv_file(file_path):
    try:
        return pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print(f"Error: Empty data in the file: {file_path}")
        raise
    except pd.errors.ParserError:
        print(f"Error: Unable to parse CSV file. Check the file format in {file_path}")
        raise
# Create a style function to highlight negative values
def highlight_negative(value):
    color = 'red' if value < 0 else 'black'
    return f'color: {color}'

# Specify file paths

file1_path = "fipi-sector.csv"
file2_path = "lipi-sector.csv"
# Read CSV files into DataFrames
df1 = read_csv_file(file1_path)
df2 = read_csv_file(file2_path)

# Concatenate DataFrames, preserving order
merged_df = pd.concat([df1, df2], ignore_index=True).drop_duplicates()

# Get the date as input from the user
user_date_input = input("Enter the date (format: MM/DD/YYYY): ")

# Validate the date format
try:
    date_object = datetime.datetime.strptime(user_date_input, "%m/%d/%Y")
except ValueError:
    print("Invalid date format. Please use MM/DD/YYYY.")
    raise

# Add the "Date" column with the specified date
merged_df["Date"] = user_date_input

# Reorder the columns with "Date" as the first column
column_order = ["Date"] + [col for col in merged_df.columns if col not in ["Date"]]
merged_df = merged_df[column_order]


# Check if the old file exists
# Change the file extension to XLSX
old_file_path = "merged_file_with_date.xlsx"
old_file_exists = os.path.exists(old_file_path)

if old_file_exists:
    # Ask the user whether to append or overwrite the existing file
    user_choice = input(f"The file {old_file_path} already exists. Do you want to (A)ppend or (O)verwrite? ").upper()

    if user_choice == "A":
        # Read the existing merged file
        old_merged_df = pd.read_excel(old_file_path, engine="openpyxl")
        # Combine new and existing data
        combined_df = pd.concat([old_merged_df, merged_df], ignore_index=True)

        # Use to_excel() to save as XLSX
        combined_df.to_excel(old_file_path, index=False,float_format="%.2f")

        print(f"Data appended to {old_file_path} with the specified date: {user_date_input}")
    elif user_choice == "O":
        # Save the new merged data, overwriting the existing file
        merged_df.to_excel(old_file_path, index=False,float_format="%.2f")
        print(f"Data overwritten in {old_file_path} with the specified date: {user_date_input}")
    else:
        print("Invalid choice. Exiting.")
else:
    # Save the new merged data to the XLSX file
    merged_df.to_excel(old_file_path, index=False,float_format="%.2f")
    print(f"Data saved to {old_file_path} with the specified date: {user_date_input}")
    