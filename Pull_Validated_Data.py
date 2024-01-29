from datetime import datetime


# returns a dictionary of all the scans that have had their data verified as accurate
def pull_validated_data(workbook):

    validated_scans_by_row_num = {}
    for sheet_name in workbook.sheetnames:
        if sheet_name.startswith("TABLET"):
            sheet = workbook[sheet_name]

            # Iterate through rows of each sheet and assign variables
            for row_num in range(1, sheet.max_row + 1):
                customer_number = sheet[f"A{row_num}"].value
                timestamp = sheet[f"B{row_num}"].value
                tablet_number = sheet[f"D{row_num}"].value
                tablet_location = sheet["H2"].value

                # Data validation
                if not isinstance(customer_number, str) or not customer_number.startswith("CN-"):
                    continue
                if not isinstance(timestamp, datetime):
                    continue
                if not isinstance(tablet_number, int):
                    continue

                # Initialize a new customer row list i if that CN has not been added to the dictionary yet
                if customer_number not in validated_scans_by_row_num:
                    validated_scans_by_row_num[customer_number] = []

                # Add current row to customer's list
                validated_scans_by_row_num[customer_number].append([customer_number, timestamp, tablet_number,
                                                                    tablet_location])
    # print(validated_scans_by_row_num)
    return validated_scans_by_row_num
