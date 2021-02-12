from flask import render_template_string, render_template
import pandas as pd
import os

###---------------------------------------------------------------------
# Utility functions
###---------------------------------------------------------------------

def numbers_to_names(numbers):
    """Returns a list of the names of players with the given numbers
    
    :param numbers The list of Player Numbers to get the names of"""

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

def names_to_numbers(names):
    """Returns a list of the numbers of players with the given names
    
    :param numbers The list of Player names to get the numbers of"""
    
    # Get total stats spreadsheet
    total_stats = get_sheet_df('TotalStats')

    # Get relevant columns
    nums_and_names = total_stats[['Player Number', 'Player Name']]
    player_names = list(nums_and_names['Player Name'])

    # Get player number, or throw exception if the number is out of range
    def name_to_number(name):
        if name in player_names:
            player_num = player_names.index(name) + 1
            return player_num
        else:
            raise Exception(f"The player {name} was not found. Check the player name matches one on the sheet")
    
    return [name_to_number(name) for name in names]

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

    # Get the sheet as a dataframe
    df = get_sheet_df(sheet)

    # Generate table of dataframe
    return generate_table(df)

def generate_table(df, link_columns=[]):
    """Generates a html table of the given dataframe
    
    :param df The dataframe to generate a html table from
    :param link_columns A list where each element is a tuple of the form (column name, prefix). The column name is the name of the column whose elements we want to be links.
    The prefix is the page name that would naturally come before the link (e.g If the column name was 'Team Name', the corresponding prefix would be 'teams'. If the column
    name was 'Player Name', the corresponding prefix would be 'players"""

    # Get table headings from dataframe
    headings = list(df.columns)
    
    # Get index (in the list headings) of the column names that we want to link
    link_columns_indices = [headings.index(x) for x, y in link_columns]

    # Ger prefixes of the column names that we want to link
    link_columns_prefixes = [y for x, y in link_columns]
    
    return render_template("table-template.html", df=df, headings=headings, link_column_indices=link_columns_indices, link_columns_prefixes=link_columns_prefixes)


def team_to_owner(team_name, team_list_df):
    """Returns the team owner corresponding to the given team_name in the 'TeamList' spreadsheet
    
    :param team_name The team name to get the owner of
    :param team_list_df The dataframe containing the data needed (in this case we will have team_list_df = get_sheet_df('TeamList')"""

    # Get Team Names and Team Owners and strip the items
    names = list(team_list_df['Team Name'])
    names = [x.strip() for x in names]
    owners = list(team_list_df['Team Owner'])
    owners = [x.strip() for x in owners]

    # Find owner, or throw exception if team name was not found
    if team_name in names:
        return owners[names.index(team_name)]
    else:
        raise Exception(f"Couldn't find {team_name} in the list of team names")

def name_to_picks(player_name, team_list_df):
    """Returns a list of tuples, each of the form (team_name, team_owner), where each tuple corresponds to a team that picked the given player
    
    :param player_name The player to get the picks of
    :param team_list_df The dataframe containing the data needed (in this case we will have team_list_df = get_sheet_df('TeamList')"""

    # Get team rosters
    team_rosters = team_list_df.drop(['Week 1 Points', 'Week 2 Points', 'Week 3 Points', 'Week 4 Points', 'Week 5 Points', 'Week 6 Points',
                                    'Week 7 Points', 'Week 8 Points', 'Week 9 Points', 'Week 10 Points', 'Total Points'], axis=1)

    picks = []                 
    for i, row in team_rosters.iterrows():
        # Get team roster
        roster = list(row)[3:]
        roster = numbers_to_names(roster)
        print(roster)

        # Check if the player is in the team
        if player_name in roster:
            picks.append((row['Team Name'], row['Team Owner']))
            
    return picks

    


###-------------------------------------------------------------
# Tables for Home page
###-------------------------------------------------------------

def generate_league_table_df():
    """Generates a dataframe of the current Fantasy Cricket League Table."""

    # Get TeanList Sheet as dataframe
    team_list = get_sheet_df("TeamList")
    
    # Trim the data to get Team name, team owner, and team total points
    team_list.drop(['Batsman 1', 'Batsman 2', 'Batsman 3', 'Batsman 4', 'All-Rounder 1', 'All-Rounder 2', 'All-Rounder 3',
                    'Wicket-keeper', 'Bowler 1', 'Bowler 2' , 'Bowler 3', 'Week 1 Points', 'Week 2 Points', 'Week 3 Points', 
                    'Week 4 Points', 'Week 5 Points', 'Week 6 Points', 'Week 7 Points', 'Week 8 Points', 'Week 9 Points', 'Week 10 Points'], axis=1, inplace=True)
    
    # Sort table in descending order of points
    league_table = team_list.sort_values(by=['Total Points'], ascending=False)
    return league_table


###-------------------------------------------------------------
# Tables for Dream Team page
###-------------------------------------------------------------

def generate_dream_team_table():
    """Generates a html table fo the current Fantasy Cricket Dream Team"""

    # Get TotalStats sheet as a dataframe
    total_stats = get_sheet_df("TotalStats")

    # Discard unecessary columns so we're left with Player Name, Player Role and TOTAL
    total_stats.drop(['Player Number', 'GAMES', 'RUNS', '4s', '6s', '50s', '100s', '150s', '200s', 'DUCKS', 'OVERS',
                        'BALLS', 'WICKETS', 'RUNS AGAINST', 'MAIDENS', '3fers/4fers', '5fers', '6+fers',
                        'CATCHES', 'RUN-OUTS', 'STUMPINGS', 'MOTM', 'WINS', 'BATTING', 'BOWLING', 'FIELDING', 'BONUS'], axis=1, inplace=True)

    # Split dataframe into 4 different dataframes, one for each role
    all_rounders = total_stats[total_stats['Player Role'] == 'All-Rounder']
    batsmen = total_stats[total_stats['Player Role'] == 'Batsman']
    bowlers = total_stats[total_stats['Player Role'] == 'Bowler']
    wicket_keepers = total_stats[total_stats['Player Role'] == 'Wicket-keeper']

    # Sort the dataframe for each role in desceding order of total points
    all_rounders = all_rounders.sort_values(by=['TOTAL'], ascending=False)
    batsmen = batsmen.sort_values(by=['TOTAL'], ascending=False)
    bowlers = bowlers.sort_values(by=['TOTAL'], ascending=False)
    wicket_keepers = wicket_keepers.sort_values(by=['TOTAL'], ascending=False)

    # Get the dream team
    dream_team = pd.concat([batsmen.head(4), all_rounders.head(3), wicket_keepers.head(1), bowlers.head(3)])

    return generate_table(dream_team)


###-------------------------------------------------------------
# Tables for Team-stats page
###-------------------------------------------------------------

def generate_team_roster_table(team_name, team_list_df):
    """Generates a html table of a given team's roster
    
    :param team_name The team name to get the roster of
    :param team_list_df The dataframe containing the data needed (in this case we will have team_list_df = get_sheet_df('TeamList')"""

    # Get team names as a list
    team_names = list(team_list_df['Team Name'])

    # Trim the data to only get the players, not the points
    team_list = team_list_df.drop(['Team Name', 'Team Owner', 'Week 1 Points', 'Week 2 Points', 'Week 3 Points', 'Week 4 Points', 
                    'Week 5 Points', 'Week 6 Points', 'Week 7 Points', 'Week 8 Points', 'Week 9 Points',
                     'Week 10 Points', 'Total Points'], axis=1)

    # Get the relevant row of the dataframe, otherwise throw an exception if the team is not found
    if team_name in team_names:
        row_index = team_names.index(team_name)
        team_roster = team_list.iloc[[row_index]]

        # Transpose for presentation
        team_roster = team_roster.T

        # Convert numbers to list of player names
        team_roster.columns = [0]
        numbers = list(team_roster[0])
        player_names = numbers_to_names(numbers)

        team_roster[0] = team_roster.index.values
        team_roster[1] = player_names
        team_roster.columns = ["Role", "Player Name"]
        return generate_table(team_roster)
    else:
        raise Exception(f"Couldn't find '{team_name}' on the TeamList")


if __name__ == "__main__":
    team_list = get_sheet_df("TeamList")
    print(name_to_picks('Nathan Sharpe', team_list))