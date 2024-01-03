
import openpyxl

def convert_excel_to_lists(file_path):
    # Load the Workbook
    wb = openpyxl.load_workbook(file_path)

    # Initialize empty lists for data
    KMIALL, KMI100, KMI30, MYLIST, QSE,CUSTUM = [], [], [], [], [], []

    # Loop through each sheet
    for sheet_name in ("KMIALL", "KMI100", "KMI30", "MYLIST", "QSE","CUSTUM"):
        sheet = wb[sheet_name]

        # Assuming data starts at row 2 and column 1 (adjust if needed)
        for row in sheet.iter_rows(min_row=2):
            symbol = row[0].value  # Assuming symbols are in the first column

            # Append symbol to corresponding list
            if sheet_name == "KMIALL":
                KMIALL.append(symbol)
            elif sheet_name == "KMI100":
                KMI100.append(symbol)
            elif sheet_name == "KMI30":
                KMI30.append(symbol)
            elif sheet_name == "MYLIST":
                MYLIST.append(symbol)
            elif sheet_name == "QSE":
                QSE.append(symbol)
            elif sheet_name == "CUSTUM":
                CUSTUM.append(symbol)

    # (Optional) Close the workbook
    wb.close()

    # Return the extracted lists
    return KMIALL, KMI100, KMI30, MYLIST, QSE, CUSTUM

# Call the function and assign the lists to variables
KMIALL, KMI100, KMI30, MYLIST, QSE, CUSTUM = convert_excel_to_lists("PSXSymbols.xlsx")