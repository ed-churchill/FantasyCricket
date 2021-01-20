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


def update_stats(bat_df, bowl_df, field_df, week_number):
    """Function that updates the sheet of a particular week

    :param bat_df The cleaned batting dataframe, obtained from the function read_play_cricket.clean_scorecards()
    :param bowl_df The cleaned bowling dataframe, obtained from the function read_play_cricket.clean_scorecards()
    :param field_df The cleaned fielding dataframe, obtained from the function read_play_cricket.clean_scorecards()
    :param week_number The Week Number of the sheet to be updated.
    """

    # Get the relevant sheet instance
    sheet = get_sheet().get_worksheet(week_number - 1)

    # Update batting stats (and add one to games played of each batsman in the game)
    for index in bat_df.index:

        # Get name from dataframe
        name = bat_df['BATSMAN'][index]

        name_found = False

        # Find the name in the first column of the spreasheet. If it's not found, prompt the user to manually type the
        # name in.
        sheet_row_count = sheet.row_count
        for row in range(3, sheet_row_count + 3):
            name_on_sheet = sheet.cell(row, 2).value

            # Case where name is found
            if name == name_on_sheet:
                name_found = True

                # Add one to games played
                current_games = sheet.cell(row, 3).value
                if current_games == '':
                    current_games = 0
                else:
                    current_games = int(current_games)
                sheet.update_cell(row, 3, current_games + 1)

                # Update runs
                # Update 4s
                # Update 6s
                # Update 50s
                # Update 100s
                # Update 150s
                # Update 200s
                # Update Ducks

        # Case where name is not found (so name_found is still false)
        if not name_found:
            print(name + " was not found and the sheet wasn't updated")

        # THERE ARE TOO MANY API REQUESTS PER SECOND. TO FIX THIS, I NEED TO GET THE LIST OF NAMES AS A LIST AND STORE
        # IT IN A VARIABLE AS A LIST, INSTEAD OF REQUESTING THE VALUE ON EVERY FOR LOOP ITERATION.


batting_df, bowling_df, fielding_df = read_play_cricket.clean_scorecards("https://uniofwarwick.play-cricket.com/website/results/4055612")
update_stats(batting_df, bowling_df, fielding_df, 1)

