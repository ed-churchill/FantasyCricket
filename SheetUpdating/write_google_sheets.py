"""Module containing functions to write data from Dataframes into Google Sheets"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet():
    """Function that returns the Google Sheet 'FantasyCricketPlayerStats'."""

    # Define the scope of the application
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

    # Add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)

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

    # Get the relevant sheet instance and list of names on sheet
    sheet = get_sheet().get_worksheet(week_number - 1)
    sheet_names = sheet.col_values(2)[2:]

    # Get the winning team from the user. This will be used to add bonus winning points if Warwick won
    warwick_win = input('Did Warwick win? (This will be used to give bonus points if they won). Type "y" or "n" and '
                        'then press enter')

    # Get the MOTM and update the sheet with it
    motm = man_of_the_match(sheet_names)
    motm_index = name_to_index(motm, sheet_names)
    sheet.update_cell(motm_index, 23, 1)

    # Get the list of names from the batting Dataframe
    batsman_list = list(bat_df['BATSMAN'])

    # For loop to update each player's batting stats
    for name in batsman_list:

        # Get the index of this name in the sheet
        name_row_index = name_to_index(name, sheet_names)

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

        print(name + "'s batting stats have been successfully updated \n")

        # Update the spreasheet if Warwick won for bonus points
        if warwick_win.strip() == 'y':
            sheet.update_cell(name_row_index, 24, 1)
        else:
            sheet.update_cell(name_row_index, 24, 0)

    # Get list of names from bowling dataframe
    bowler_list = list(bowl_df['BOWLER'])

    # For loop to update each player's bowling stats
    for name in bowler_list:

        # Get the index of the name in the sheet
        name_row_index = name_to_index(name, sheet_names)

        # Get bowling stats from dataframe
        bowler_index = bowler_list.index(name)

        # Get overs, balls, wickets, runs against and maidens
        overs = bowl_df.at[bowler_index, 'OVERS']
        balls = overs_to_balls(overs)
        wickets = int(bowl_df.at[bowler_index, 'WICKETS'])
        runs_against = int(bowl_df.at[bowler_index, 'RUNS'])
        maidens = int(bowl_df.at[bowler_index, 'MAIDENS'])

        # Calculate 3fers/4fers, 5fers, and 6+fers
        if wickets >= 6:
            six_plus = 1
            five = 0
            three_four = 0
        elif wickets == 5:
            six_plus = 0
            five = 1
            three_four = 0
        elif 3 <= wickets <= 4:
            six_plus = 0
            five = 0
            three_four = 1
        else:
            six_plus = 0
            five = 0
            three_four = 0

        # Create list of bowling stats and update the spreadsheet.
        bowling_stats = [float(overs), balls, wickets, runs_against, maidens, three_four, five, six_plus]
        bowling_cells = sheet.range(name_row_index, 12, name_row_index, 19)
        for i, val in enumerate(bowling_stats):
            bowling_cells[i].value = val
        sheet.update_cells(bowling_cells)

        print(name + "'s bowling stats have been successfully updated \n")

    # Case where fielding dataframe is empty
    if field_df.empty:
        print('There were no fielding stats to update. Either the stats were not available on Play Cricket, '
              'or there were no catches, stumpings or run-outs')

    # Case where fielding dataframe is non-empty
    else:
        # Get list of names from fielding dataframe
        fielder_list = list(field_df['Fielder'])

        # For loop to update each player's fielding stats
        for name in fielder_list:

            # Get the index of the name in the sheet.
            name_row_index = name_to_index(name, sheet_names)

            # Get fielding stats from dataframe
            fielder_index = fielder_list.index(name)

            # Get catches, run outs and stumpings
            catches = int(field_df.at[fielder_index, 'Catches'])
            run_outs = int(field_df.at[fielder_index, 'Run-outs'])
            stumpings = int(field_df.at[fielder_index, 'Stumpings'])

            # Create list of fielding stats and update the spreadsheet
            fielding_stats = [catches, run_outs, stumpings]
            fielding_cells = sheet.range(name_row_index, 20, name_row_index, 22)
            for i, val in enumerate(fielding_stats):
                fielding_cells[i].value = val
            sheet.update_cells(fielding_cells)

            print(name + "'s fielding stats have been successfully updated \n")


def overs_to_balls(overs):
    """Function that returns the number of balls given a number of overs
    :param overs The number of overs as a decinml to be converted
    """

    overs_string = str(overs)

    # Case where there is no decimal
    if '.' not in overs_string:
        return 6 * int(overs_string)

    # Find decimal part of overs
    decimal = int(overs_string[-1])

    # Find whole part of overs
    whole_overs = int(overs_string[:-2])

    # Calculate number of balls
    balls = (6 * whole_overs) + decimal
    return balls


def name_to_index(name, sheet_names):
    """Function that checks if a given name is in a given list of names from the Google Sheet. Returns
    the index of the name in the sheet if it is found, prompts user input otherwise until the names match.
    :param name The name to check against the list of names in the sheet
    :param sheet_names The list of names of the FantasyCricketPlayerStats Sheet"""

    # Case where names match
    if name in sheet_names:
        # Row index of the name in the sheet
        name_row_index = sheet_names.index(name) + 3
        return name_row_index

    # Case where names don't match
    else:
        valid_name = False
        while not valid_name:
            # Prompt user input
            print('The name "' + name + '" was not found on the sheet.')
            user_input = input('Please type the correct name, as it appears in the sheet.').strip()

            # Check if user input is valid. If it is, update the sheet
            if user_input in sheet_names:
                name_row_index = sheet_names.index(user_input) + 3
                return name_row_index
            else:
                print("Your input was not found on the sheet. Please try again \n")


def man_of_the_match(sheet_names):
    """Function that requests user input for man of the match and returns the name of the person on the sheet who
     is man of the match for a particular game

     :param sheet_names The list of names on the spreadhseet to check the user input against"""

    valid_name = False
    while not valid_name:
        print('Please type in the Man of the Match, as their name appears on the spreadsheet. \n')
        user_input = input().strip()
        if user_input in sheet_names:
            return user_input
        else:
            print('The name "' + user_input + '"' + ' was not found in the sheet. Please try again')

