from flask import Flask, render_template

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

#-------------------------------------------------------------------------------
# Define the scope of the application
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)

# Authorise the client sheet
client = gspread.authorize(creds)

# Get the spreadsheet
sheet = client.open("FantasyCricketPlayerStats")

# Store sheets in dictionary
data = {}
sheet_names = ["Week1", "Week2", "Week3", "Week4", "Week5", "Week6", "Week7",
               "Week8", "Week9", "Week10", "TotalStats", "TeamList"]

for i, sheet_name in enumerate(sheet_names):
    spreadsheet = sheet.get_worksheet(i)
    records_data = spreadsheet.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    data[sheet_name] = records_df

#-------------------------------------------------------------------------------
@app.route("/")
def home():
    table_data = [("Ed", 20, "Warwick"), 
    ("Alan", 20, "LSE"), 
    ("Kacper", 20, "Imperial"), 
    ("Bronson", 21, "Essex"), 
    ("James", 21, "Oxford"), 
    ("Michael", 20, "Bristol")]
    return render_template("index.html", users=table_data, value=value)

@app.route("/info")
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True)
