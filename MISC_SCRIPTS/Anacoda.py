import pandas as pd

# Assuming your Excel file is named 'PSX_Symbol_urllink.xlsx' with a sheet named 'Sheet1'
excel_file_path = 'PSX_Symbol_urllink.xlsx'
sheet_name = 'ScreenerResults'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path, sheet_name)

# Create a new column to store the extracted hyperlinks
df['Extracted Hyperlink'] = ""

# Iterate through each row and column to extract and store hyperlinks
for index, row in df.iterrows():
    for column in df.columns:
        cell_value = row[column]
        
        # Check if the cell contains a hyperlink
        if isinstance(cell_value, str) and "http" in cell_value:
            # Extract the hyperlink
            hyperlink = cell_value.split('"')[1]
            
            # Store the extracted hyperlink in the new column
            df.at[index, 'Extracted Hyperlink'] = hyperlink

# Save the updated DataFrame with the new column to a new Excel file
output_excel_path = 'output_file.xlsx'
df.to_excel(output_excel_path, index=False)


