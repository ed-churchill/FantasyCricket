"""File to experiment with and learn the basics of using Google Sheets API with python"""

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope of the application
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)

# Authorise the client sheet
client = gspread.authorize(creds)

# Get the spreadsheet
sheet = client.open("FantasyCricketPlayerStats")

# Get the first sheet on the spreadsheet
total_stats_sheet = sheet.get_worksheet(10)

# Print some particular spreadsheet values
print(total_stats_sheet.cell(3, 4).value)

# Get all the data in the sheet (in a json string) and view it
records_data = first_sheet.get_all_records()
# print(records_data)

# Convert json string to pandas dataframe
records_df = pd.DataFrame.from_dict(records_data)

# Get the relevant part of the dataframe
records_df = records_df[['Player Number', 'Player Name', 'Category', 'Squad', 'Price (M)']]
print(records_df.head())
