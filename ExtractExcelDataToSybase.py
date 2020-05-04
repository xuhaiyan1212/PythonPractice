import uuid
import glob
import os
import shutil
import pyodbc
import pandas as pd
import xlrd


TOLOAD_DIR = "E:\Python\PycharmProjects\AutomationTools\Excel\Reports\ToLoad\\"
TEMP_DIR = "E:\Python\PycharmProjects\AutomationTools\Excel\Reports\Temp\\"
LOADED_DIR = r"E:\Python\PycharmProjects\AutomationTools\Excel\Reports\Loaded\\"


def extract_excel_to_sybase(files, batch_id):
    print("Files will be loaded:{}".format(";".join(files)))

    for file in files:
        # create Connection and Cursor objects
        conn = pyodbc.connect(
            r'DRIVER={SQL Server};SERVER=DESKTOP-OIOAB85\SQLEXPRESS;DATABASE=MyPractise;Trusted_Connection=yes')
        cursor = conn.cursor()

        # read data
        data = pd.read_excel(TEMP_DIR + batch_id + "_" + file)

        # rename columns
        data = data.rename(columns={'Lease Number': 'Lease_Number',
                                    'Start Date': 'Start_Date',
                                    'Report Status': 'Report_Status',
                                    'Status Date': 'Status_Date',
                                    'Current Status': 'Current_Status'
                                    })

        # export
        data.to_excel('Daily Flash.xlsx', index=False)

        # Open the workbook and define the worksheet
        book = xlrd.open_workbook("Daily Flash.xlsx")
        sheet = book.sheet_by_name("Sheet1")

        query = """
        INSERT INTO [ZZZ] (
            Lease_Number,
            Start_Date,
            Report_Status,
            Status_Date,
            Current_Status
        ) VALUES (?, ?, ?, ?, ?)"""

        # grab existing row count in the database for validation later
        cursor.execute("SELECT count(*) FROM ZZZ")
        before_import = cursor.fetchone()

        for r in range(1, sheet.nrows):
            Lease_Number = sheet.cell(r, 0).value
            Start_Date = sheet.cell(r, 1).value
            Report_Status = sheet.cell(r, 2).value
            Status_Date = sheet.cell(r, 3).value
            Current_Status = sheet.cell(r, 4).value

            # Assign values from each row
            values = (Lease_Number, Start_Date, Report_Status, Status_Date, Current_Status)

            # Execute sql Query
            cursor.execute(query, values)

        # Commit the transaction
        conn.commit()

        # If you want to check if all rows are imported
        cursor.execute("SELECT count(*) FROM ZZZ")
        result = cursor.fetchone()

        print((result[0] - before_import[0]) == len(data.index))  # should be True

        # Close the database connection
        conn.close()


def main():
    #Generate batch ID
    batch_id = str(uuid.uuid1())
    print("Batch ID:{}".format(batch_id))

    #Go through ToLoad dir, rename them and copy it temp dir
    toload_files = [os.path.basename(file) for file in glob.glob(TOLOAD_DIR + "*.xlsx", recursive=False)]

    for file in toload_files:
        shutil.move(TOLOAD_DIR + file, TEMP_DIR + batch_id + "_" + file)

    #Extract files in Temp dir and feed to database
    extract_excel_to_sybase(toload_files, batch_id)

if __name__ == '__main__':
    main()
