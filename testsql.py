import sqlite3
import pandas as pd
# Connect to the SQLite database
# If the database does not exist, it will be created
conn = sqlite3.connect('data.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get all data from the table
cursor.execute("SELECT * FROM all_symbols")

# Fetch all the rows
data_rows = cursor.fetchall()

# Get the column names from the table info
column_names = [info_row[0] for info_row in cursor.description]

# Convert the rows into a pandas DataFrame
df = pd.DataFrame(data_rows, columns=column_names)

# Print the DataFrame
print(df)

# Close the connection
conn.close()