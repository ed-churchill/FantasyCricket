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

    # Get the list of names in the sheet
    sheet_names = sheet.col_values(2)[2:]

    # Get the list of names from the batting Dataframe
    batsman_list = list(bat_df['BATSMAN'])

    # For loop to update each player's batting stats
    for name in batsman_list:

        # Case where names match
        if name in sheet_names:
            # Row index of the name in the sheet
            name_row_index = sheet_names.index(name) + 3

        # Case where names don't match
        else:
            valid_name = False
            while not valid_name:
                # Prompt user input
                print('The name "' + name + '" was not found on the sheet.')
                user_input = input('Please type the correct name, as it appears in the sheet.').strip()

                # Check if user input is valid. If it is, update the sheet
                if user_input in sheet_names:
                    valid_name = True
                    name_row_index = sheet_names.index(user_input) + 3
                else:
                    print("Your input was not found on the sheet. Please try again \n")

        # Get batting stats from dataframe
        batsman_index = batsman_list.index(name)

        # Get runs, fours and sixes
        runs = int(bat_df.at[batsman_index, 'RUNS'])
        fours = int(bat_df.at[batsman_index, '4s'])
        sixes = int(bat_df.at[batsman_index, '6s'])

        # Calculate milestones/ducks
        if runs >= 200:
            double_hundreds = 1
            hundred_and_fifties = 0
            hundreds = 0
            fifties = 0
            ducks = 0
        elif 150 <= runs < 200:
            double_hundreds = 0
            hundred_and_fifties = 1
            hundreds = 0
            fifties = 0
            ducks = 0
        elif 100 <= runs < 150:
            double_hundreds = 0
            hundred_and_fifties = 0
            hundreds = 1
            fifties = 0
            ducks = 0
        elif 50 <= runs < 100:
            double_hundreds = 0
            hundred_and_fifties = 0
            hundreds = 0
            fifties = 1
            ducks = 0
        else:
            double_hundreds = 0
            hundred_and_fifties = 0
            hundreds = 0
            fifties = 0
            ducks = 0

        # Create list of batting stats and update the spreadsheet
        batting_stats = [1, runs, fours, sixes, fifties, hundreds, hundred_and_fifties, double_hundreds, ducks]
        batting_cells = sheet.range(name_row_index, 3, name_row_index, 11)
        for i, val in enumerate(batting_stats):
            batting_cells[i].value = val
        sheet.update_cells(batting_cells)

        print(name + "'s stats have been successfully updated \n")


batting_df, bowling_df, fielding_df = read_play_cricket.clean_scorecards(
    "https://uniofwarwick.play-cricket.com/website/results/4055612")
update_stats(batting_df, bowling_df, fielding_df, 1)
