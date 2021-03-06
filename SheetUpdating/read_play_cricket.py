"""Module containing functions that fetch scorecards from PlayCricket.com, clean them and
 put the data into pandas dataframes"""

import pandas as pd
import re


def clean_batting_df(batting_scorecard):
    """Function that cleans the batting scorecard

    :param batting_scorecard: Warwick's batting scorecard (as a dataframe) obtained from the function get_tables
    """
    # Rename batting scorecard for ease
    df = batting_scorecard

    # Replace any NaN values with 0s
    df = df.fillna(0)

    # Clean the cells in the batsman column
    clean_cells = []
    for i in range(0, df.shape[0]):

        # Identify the clutter
        if df.iat[i, 1] == 0 or df.iat[i, 2] == 0:
            how_out = str(df.iat[i, 1]) + str(df.iat[i, 2])
            how_out = (how_out.replace('0', ''))
            how_out = how_out.replace(' ', '')
        else:
            how_out = df.iat[i, 1] + df.iat[i, 2]
            how_out = (how_out.replace(' ', ''))

        # Remove the clutter
        batsman_cell = ''.join(df.iat[i, 0].split())  # Remove whitespace
        cleaned_cell = batsman_cell.replace(how_out, '').strip()  # Remove how_out

        # Put space before any capital letter to separate the person's first name and last name
        cleaned_cell = re.sub(r"(\w)([A-Z])", r"\1 \2", cleaned_cell)

        # Append the cleaned element
        clean_cells.append(cleaned_cell)

    # Update the batsman column with the cleaned cells
    df = df.assign(BATSMAN=clean_cells)

    # Remove the two redundant columns (the unnamed columns)
    df = df.drop(df.columns[[1, 2]], axis=1)

    # Change the names of the runs and balls columns
    df.rename(columns={'RUNSR': 'RUNS', 'BALLSB': 'BALLS'}, inplace=True)

    return df


def clean_bowling_df(bowling_scorecard):
    """Function that cleans the bowling scorecard

    :param bowling_scorecard: Warwick's bowling scorecard (as a dataframe) obtained from the function get_tables
    """

    # Rename bowling scorecard for ease
    df = bowling_scorecard

    # Replace any NaN values with 0s
    df = df.fillna(0)

    # Change the names of the columns
    df.rename(columns={'OVERSO': 'OVERS', 'MAIDENSM': 'MAIDENS', 'RUNSR': 'RUNS',
                       'WICKETSW': 'WICKETS', 'WIDESWD': 'WIDES', 'NO BALLSNB': 'NO BALLS'}, inplace=True)

    return df


def clean_fielding_df(oppo_batting_scorecard):
    """Function that uses the opposition's batting scorecard to return a dataframe of fielding stats

    :param oppo_batting_scorecard: The opposition's batting scorecard (as a dataframe) obtained from the function
    get_tables
    """

    # Rename oppo_batting_scorecard for ease
    df = oppo_batting_scorecard

    # Return empty dataframe if the opposition batting scorecard is empty
    if df.empty:
        return df
    
    else:
        # Remove unecessary columns
        df.drop(df.columns[[0, 3, 4, 5, 6, 7]], axis=1, inplace=True)

        # Remame two remaining columns
        df.rename(columns={'Unnamed: 1': 'A', 'Unnamed: 2': 'B'}, inplace=True)

        # Replace any NaN values with 0s
        df = df.fillna(0)

        # Delete any lbw rows, not out rows and did not bat rows
        df = df[df.A != 'lbw']
        df = df[df.A != 'not out']
        df = df[df.A != 'did not bat']

        # Delete any rows where the mode of dismissal is bowled.
        for index in df.index:
            if df['A'][index] == 0 and df['B'][index][0] == 'b':
                df.drop([index], inplace=True)

        # Delete any rows where the mode of dismissal is unsure
        for index in df.index:
            unsure_a = str(df['A'][index]).lower()
            unsure_b = str(df['B'][index]).lower()
            
            if 'unsure' in unsure_a or 'unsure' in unsure_b:
                df.drop([index], inplace=True)

        # Get stats on catches, run outs and stumpings and store them in list
        catches = []
        run_outs = []
        stumpings = []
        for index in df.index:
            # Boolean values to determine the method of dismissal
            caught = str(df['A'][index])[0] == 'c'
            stumped = str(df['A'][index])[0:2] == 'st'
            run_out = str(df['A'][index])[0:8] == 'run out'
            c_and_b = str(df['B'][index])[0:6] == 'ct & b'

            # Get the name of the person who got the catch/runout/stumping and add the dismissal to the relevant list
            if c_and_b:
                name = df['B'][index][7:]
                catches.append(name)
            elif caught:
                name = df['A'][index][1:]
                catches.append(name)
            elif run_out:
                name = df['A'][index][7:]
                run_outs.append(name)
            elif stumped:
                name = df['A'][index][2:]
                stumpings.append(name)

        # Get a list of unique fielders without losing old data
        copy_catches = catches.copy()
        copy_run_outs = run_outs.copy()
        copy_stumpings = stumpings.copy()

        catches.extend(run_outs)
        catches.extend(stumpings)
        unique_fielders = list(set(catches))

        # Store fielding stats in dictionary. The dictionary has the names as keys, and a list of length 3 as values. For
        # example, 'Charlie Royle': [2, 1, 0] would mean that Charlie Royle took 2 catches, 1 run out and 0 stumpings
        fielding_stats = {}
        for name in unique_fielders:
            fielding_stats[unique_fielders.index(name)] = [name, copy_catches.count(name),
                                                        copy_run_outs.count(name), copy_stumpings.count(name)]

        # Convert dictionary to dataframe and rename columns (if dataframe is non-empty)
        fielding_df = pd.DataFrame.from_dict(fielding_stats, orient='index')
        if not fielding_df.empty:
            fielding_df.columns = ['Fielder', 'Catches', 'Run-outs', 'Stumpings']
        else:
            print('The fielding stats are empty. Either the stats were not available on Play Cricket, or there were no'
                ' catches, stumpings or run-outs')

        return fielding_df


def get_tables(match_url):
    """Function that returns a tuple of length 3. The first element of the tuple is the batting scorecard as a
    dataframe (ready for editing), the second element is the bowling scorecard as a dataframe (ready for editing). The
    third element is the opposition's batting scorecard (ready for editing), which will be used to get fielding stats.

    :param str match_url: The URL of the scorecard on PlayCricket.com
    """

    # Fetch all the tables on the page and store them in a list of dataframes
    tables = pd.read_html(match_url)

    # Get correct batting and bowling scorecards using user input
    # Case where all relevant tables are on the page
    if len(tables) >= 7:
        
        valid_user_input = False
        while not valid_user_input:
            print(tables[1])
            print("\n Is this Warwick's batting scorecard? This information will be used to get the correct data from the website.\n")
            x = input("Type 'y' or 'n' then press enter.")
            
            if x.strip() == 'y':
                batting_scorecard = tables[1]
                bowling_scorecard = tables[6]
                oppo_batting_scorecard = tables[4]
                valid_user_input = True
            elif x.strip() == 'n':
                batting_scorecard = tables[4]
                bowling_scorecard = tables[3]
                oppo_batting_scorecard = tables[1]
                valid_user_input = True
            else:
                print("\n Your input was invalid. Remember to type in 'y' or 'n'. Please try again!\n")

    # Case where there are some tables missing on the page. Prompt user for input to find each of the relevant tables
    else:
        # Get rid of the unecessary first table and any empty dataframes
        tables.pop(0)
        non_empty_tables = []
        for table in tables:
            if not table.empty:
                non_empty_tables.append(table)

        # Inform user of missing data
        print("\nThere was some data missing on the webpage so I need your help to find the correct scorecards\n")

        # Find batting scorecard
        found_batting_scorecard = False
        for index, table in enumerate(non_empty_tables):
            print(table)
            print("\nIs this Warwick's batting scorecard? This information will be used to get the correct data from the website.\n")
            x = input("Type 'y' or 'n' and then press enter.")
            
            if x.strip() == 'y':
                found_batting_scorecard = True
                batting_scorecard = non_empty_tables[index]
                batting_scorecard_index = index
                break
            else:
                print("\n")
        
        # Remove batting scorecard from list since it's already been found.
        non_empty_tables.pop(batting_scorecard_index)
        
        # Inform user in the case that the batting scorecard could not be found
        if not found_batting_scorecard:
            print("\nI was unable to find the batting scorecard. Rerun the program and check you didn't miss it or input the data manually to the spreadsheet.\n")

        # Find bowling scorecard
        found_bowling_scorecard = False
        for index, table in enumerate(non_empty_tables):
            print(table)
            print("\nIs this Warwick's bowling scorecard? This information will be used to get the correct data from the website.\n")
            x = input("Type 'y' or 'n' and then press enter.")
            if x.strip() == 'y':
                found_bowling_scorecard = True
                bowling_scorecard = non_empty_tables[index]
                break
            else:
                print("\n")

        # Inform user in the case that the bowling scorecard could not be found
        if not found_bowling_scorecard:
            print("I was unable to find the bowling scorecard. Rerun the program and check you didn't miss it")

        print("\nThe fielding stats were not found since the opposition's batting scorecard was not found on the page. Please enter them manually to the spreadsheet")
        oppo_batting_scorecard = pd.DataFrame()

    return batting_scorecard, bowling_scorecard, oppo_batting_scorecard


def clean_scorecards(match_url):
    """Function that returns a tuple of length 3. The first element of the tuple is the cleaned batting scorecard as a
    dataframe, the second element is a cleaned bowling scorecard as a dataframe. The 3rd elemeent is a dataframe
    containing the mode of dismissal for each wicket

    :param str match_url: The URL of the scorecard on PlayCricket.com
    """

    # Get the unclean scorecards
    dirty_batting, dirty_bowling, dirty_oppo_batting = get_tables(match_url)

    # Clean the batting and bowling scorecards
    df_bat = clean_batting_df(dirty_batting)
    df_bowl = clean_bowling_df(dirty_bowling)
    df_field = clean_fielding_df(dirty_oppo_batting)

    return df_bat, df_bowl, df_field
