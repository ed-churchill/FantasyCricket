import read_play_cricket
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope of the application
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('FantasyCricket-7a5a400ddc86.json', scope)

# Authorise the client sheet
client = gspread.authorize(creds)