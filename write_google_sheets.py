"""Module containing functions to write data from Dataframes into Google Sheets"""

import read_play_cricket
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet():
    """Function that returns the Google Sheet 'FantasyCricketPlayerStats'."""

    # Define the scope of the application
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

    # Add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('FantasyCricket-7a5a400ddc86.json', scope)

    # Authorise the client sheet
    client = gspread.authorize(creds)

    # Get the sheet
    sheet = client.open('FantasyCricketPlayerStats')
    return sheet


week_1 = get_sheet().get_worksheet(0)
print(week_1.cell(3, 2))
