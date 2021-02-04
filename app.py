from flask import Flask, render_template

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

#-------------------------------------------------------------------------------
# # Define the scope of the application
# Store sheets in dictionary
data = {}
sheet_names = ["Week1", "Week2", "Week3", "Week4", "Week5", "Week6", "Week7",
               "Week8", "Week9", "Week10", "TotalStats", "TeamList"]

# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
#         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

# # Add credentials to the account
# creds = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)

# # Authorise the client sheet
# client = gspread.authorize(creds)

# # Get the spreadsheet
# sheet = client.open("FantasyCricketPlayerStats")


# for i, sheet_name in enumerate(sheet_names):
#     spreadsheet = sheet.get_worksheet(i)
#     records_data = spreadsheet.get('A2:AC200')
#     df = pd.DataFrame.from_dict(records_data)
#     # df.to_csv(os.path.join('data', f'{sheet_name}.csv'))
#     data[sheet_name] = df

for i, sheet_name in enumerate(sheet_names):
    df = pd.read_csv(os.path.join('data', f"{sheet_name}.csv"))
    df.columns = df.iloc[0]
    df = df[1:]
    del df[0]
    data[sheet_name] = df

#-------------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dream-team")
def dream_team():
    return render_template("dream-team.html")

@app.route("/teams")
def teams():
    return render_template("teams.html")

@app.route("/player-breakdowns")
def player_breakdowns():
    return render_template("player-breakdowns.html")



if __name__ == "__main__":
    app.run(debug=True)
