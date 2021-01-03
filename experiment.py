"""File to experiment with and learn the basics of using Google Sheets API with python"""

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope of the application
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('FantasyCricket-7a5a400ddc86.json', scope)

# Authorise the client sheet
client = gspread.authorize(creds)

# Get the spreadsheet
sheet = client.open("FantasyCricket")

# Get the first sheet on the spreadsheet
first_sheet = sheet.get_worksheet(0)

# Print number of columns in this sheet
print("The column count is " + str(first_sheet.row_count))

# Print some particular spreadsheet values
print(first_sheet.cell(2, 2))

# Get all the data in the sheet (in a json string) and view it
records_data = first_sheet.get_all_records()
# print(records_data)

# Convert json string to pandas dataframe
records_df = pd.DataFrame.from_dict(records_data)

# Get the relevant part of the dataframe
records_df = records_df[['Player Number', 'Player Name', 'Category', 'Squad', 'Price (M)']]
print(records_df.head())
