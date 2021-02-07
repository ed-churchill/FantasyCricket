from flask import render_template_string, render_template
import pandas as pd
import os

def numbers_to_names(numbers):
    """Returns a list of the names of players in the given number order
    
    :param numbers The list of Player Numbers to get the names of
    :param total_stats The dataframe of the TotalStats spreadsheet (obtain this """

    # Get total stats spreadsheet
    total_stats = get_sheet_df('TotalStats')

    # Get relevant columns
    nums_and_names = total_stats[['Player Number', 'Player Name']]

    # Get player name, or throw exception if the number is out of range
    def number_to_name(number):
        if number in list(nums_and_names['Player Number']):
            player_name = nums_and_names['Player Name'].iloc[number - 1]
            return player_name
        else:
            raise Exception(f"A Player with number {number} was not found. Check the player number matches one on the sheet")

    return [number_to_name(x) for x in numbers]

def get_sheet_df(sheet):
    """Returns the given sheet as a dataframe
    
    :param sheet The name of the sheet to be converted (name of the csv file without the extension '.csv')"""
    
    sheet_path = os.path.join("data", f"{sheet}.csv")
    if os.path.exists(sheet_path):
        df = pd.read_csv(sheet_path)
        return df
    else:
        raise Exception(f"Oopsie, {sheet} doesn't exist")

def generate_table_sheet(sheet):
    """Genereates a html table of the given sheet
    
    :param sheet The name of the sheet to be converted (name of the csv file without the extension '.csv')"""

    df = get_sheet_df(sheet)
    return generate_table(df)

def generate_table(df):
    """Generates a html table of the given dataframe
    
    :param df The dataframe to generate a html table from"""
    
    headings = list(df.columns)
    return render_template("table-template.html", df=df, headings=headings)

###-------------------------------------------------------------
# Tables for Home page
###-------------------------------------------------------------

def generate_league_table():
    """Generates a html table of the current Fantasy Cricket League Table."""

    # Get TeanList Sheet as dataframe
    team_list = get_sheet_df("TeamList")
    
    # Trim the data to get Team name, team owner, and team total points
    team_list.drop(['Batsman 1', 'Batsman 2', 'Batsman 3', 'Batsman 4', 'All-Rounder 1', 'All-Rounder 2', 'All-Rounder 3',
                    'Wicket-keeper', 'Bowler 1', 'Bowler 2' , 'Bowler 3', 'Week 1 Points', 'Week 2 Points', 'Week 3 Points', 
                    'Week 4 Points', 'Week 5 Points', 'Week 6 Points', 'Week 7 Points', 'Week 8 Points', 'Week 9 Points', 'Week 10 Points'], axis=1, inplace=True)
    
    # Sort table in descending order of points
    league_table = team_list.sort_values(by=['Total Points'], ascending=False)
    return generate_table(league_table)


###-------------------------------------------------------------
# Tables for Dream Team page
###-------------------------------------------------------------


###-------------------------------------------------------------
# Tables for Teams page
###-------------------------------------------------------------

def generate_team_roster_table(team_name):
    """Generates a html table of a given team's roster
    
    :param team_name The team name to get the roster of"""

    # Get TeamList as dataframe
    team_list = get_sheet_df("TeamList")

    # Get relevant row of dataframe for team, or throw exception if team name was not found
    team_names = list(team_list['Team Name'])

    # Trim the data to only get the players, not the points
    team_list.drop(['Team Name', 'Team Owner', 'Week 1 Points', 'Week 2 Points', 'Week 3 Points', 'Week 4 Points', 
                    'Week 5 Points', 'Week 6 Points', 'Week 7 Points', 'Week 8 Points', 'Week 9 Points',
                     'Week 10 Points', 'Total Points'], axis=1, inplace=True)

    # Get the relevant row of the dataframe, otherwise throw an exception if the team is not found
    if team_name in team_names:
        row_index = team_names.index(team_name)
        team_roster = team_list.iloc[[row_index]]

        # Transpose for presentation
        team_roster = team_roster.T

        # Convert numbers to list of player names
        numbers = list(team_roster[0])
        player_names = numbers_to_names(numbers)

        team_roster[0] = team_roster.index.values
        team_roster[1] = player_names
        team_roster.columns = ["Role", "Player Name"]
        return generate_table(team_roster)
    else:
        raise Exception(f"Couldn't find '{team_name}' on the TeamList")

    # Transpose the data for storage on the website
    # return generate_table(team_roster)
    




###-------------------------------------------------------------
# Tables for Player Breakdowns page
###-------------------------------------------------------------


if __name__ == "__main__":
    generate_team_roster_table('Test2 CC')
