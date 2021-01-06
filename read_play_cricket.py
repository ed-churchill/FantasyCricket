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
    for i in range(0, 11):

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


def get_tables(match_url):
    """Function that returns a tuple of length 2. The first element of the tuple is the batting scorecard as a
    dataframe (ready for editing), the second element is the bowling scorecard as a dataframe.

    :param str match_url: The URL of the scorecard on PlayCricket.com
    """

    # Fetch all the tables on the page and store them in a list of dataframes
    tables = pd.read_html(match_url)

    # Get correct batting and bowling scorecards using user input
    print(tables[1])
    x = input("Is this Warwick's batting scorecard? (type 'y' or 'n' then press enter)")
    if x == 'y':
        batting_scorecard = tables[1]
        bowling_scorecard = tables[6]
    else:
        batting_scorecard = tables[4]
        bowling_scorecard = tables[3]

    return batting_scorecard, bowling_scorecard


def clean_scorecards(match_url):
    """Function that returns a tuple of length 2. The first element of the tuple is the cleaned batting scorecard as a
    dataframe, the second element is a cleaned bowling scorecard as a dataframe

    :param str match_url: The URL of the scorecard on PlayCricket.com
    """

    # Get the unclean scorecards
    dirty_batting, dirty_bowling = get_tables(match_url)

    # Clean the scorecards
    df_bat = clean_batting_df(dirty_batting)
    df_bowl = clean_bowling_df(dirty_bowling)

    return df_bat, df_bowl

