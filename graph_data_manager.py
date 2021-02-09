from table_data_manager import numbers_to_names, get_sheet_df

###-------------------------------------------------------------
# Graph data for Home page
###-------------------------------------------------------------

###-------------------------------------------------------------
# Graph data for Teams page
###-------------------------------------------------------------

def team_points_df(team_name):
    """Returns a dataframe giving a weekly breakdown of a team's total points
    
    :param team_name The team name to get the weekly points breakdown for"""

    # Get TeamList as dataframe
    team_list = get_sheet_df("TeamList")

    # Get team names as a list
    team_names = list(team_list['Team Name'])

    # Trim the data to get the weekly points only
    team_list.drop(['Team Name', 'Team Owner', 'Batsman 1', 'Batsman 2', 'Batsman 3', 'Batsman 4', 'All-Rounder 1','All-Rounder 2', 'All-Rounder 3', 
                    'Wicket-keeper', 'Bowler 1', 'Bowler 2', 'Bowler 3', 'Total Points'], axis=1, inplace=True)

    # Get the correct row of the dataframe, otherwise throw an exception if the team was not found
    if team_name in team_names:
        # Get correct row
        row_index = team_names.index(team_name)
        team_points_breakdown = team_list.iloc[[row_index]]

        # Rename columns for graph presentation
        team_points_breakdown.columns = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10']
        return team_points_breakdown

    else:
        raise Exception(f"Couldn't find '{team_name}' on the TeamList")



###-------------------------------------------------------------
# Graph data for Player Breakdowns page
###-------------------------------------------------------------


if __name__ == "__main__":
    team_points_df('Test1 CC')



