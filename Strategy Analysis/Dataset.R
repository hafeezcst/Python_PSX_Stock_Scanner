library(readxl)

# Allow the user to select the Excel file
file_path <- file.choose()

# Read the Excel file selected by the user
Dataset <- read_excel(file_path) # nolint

# View the structure of the dataset
str(Dataset)
