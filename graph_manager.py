from table_data_manager import numbers_to_names, get_sheet_df, generate_league_table_df
import pygal
from pygal.style import DarkGreenBlueStyle, DefaultStyle, DarkStyle

# DarkStyle class which will be used for all graphs
style = DarkStyle

###-------------------------------------------------------------
# Utility functions
###-------------------------------------------------------------

def cumulative(ls):
    """Given a list of numerical values, returns the corresponding cumulative list
    
    :param ls The numerical list to get the corresponding cumulative list of"""
    
    # Initialise new list
    value = 0
    new_ls = []

    # Calculate cumulative values
    for x in ls:
        value += x
        new_ls.append(value)
    return new_ls

def count_trailing_zeros(ls):
    """Returns the number of trailing zeros in a numerical list. e.g [1,2,3,4,0,0,0] would return 3
    
    :param ls The numerical list to count the number of trailing zeros of"""
    
    # Initialise counter
    count = 0

    # Count the trailing zeros
    for x in ls[::-1]:
        if x == 0:
            count += 1
    return count


###-------------------------------------------------------------
# Graph data for Home page
###-------------------------------------------------------------

def top_n_league_graph(n, league_df):
    """Returns a line graph with n lines. The graph gives the cumulative weekly points breakdown of the current top n teams in the league table
    
    :param n The number of lines the graph will have, corresponding to the current top n teams
    :param league_df The current league table as a dataframe (obtained from table_data_manager.generate_league_table_df)"""

    # Get top n teams from league table
    top_n = list(league_df.head(n)["Team Name"])

    # Get the top n teams' weekly points breakdown as a dataframe
    team_list = get_sheet_df("TeamList")

    # Remove unecessary trailing zeros and transform data to cumulative data
    data = [list(team_points_df(y, team_list).iloc[0]) for y in top_n]
    min_zeros = min([count_trailing_zeros(x) for x in data])
    data = [cumulative(x)[:-min_zeros] for x in data]

    # Style the graph 
    graph = pygal.Line(style=style)
    graph.title = f"Weekly total points of current top {n} teams in the league"
    graph.x_labels = [f"Week {x}" for x in range(1, 11)]
    
    # Add the data to the graph
    for team, values in zip(top_n, data):
        graph.add(team, values)
    
    # Render the graph
    graph_data = graph.render_data_uri()
    return graph_data

###-------------------------------------------------------------
# Graph data for Teams page
###-------------------------------------------------------------
def team_points_graph(team_name, team_list_df):
    """Returns a bar graph giving the weekly breakdown of points for a specific team
    
    :param team_name The team name to generate the graph of
    :param team_list_df The dataframe containing the data needed (in this case we will have team_list_df = get_sheet_df('TeamList')"""
    
    # Get the dataframe containing the graph data
    team_points = team_points_df(team_name, team_list_df)

    # Style the graph
    graph = pygal.Bar(style=style)
    graph.title = f"{team_name} Weekly Points"
    graph.x_labels = [f"Week {x}" for x in range(1, 11)]

    # Add the data and render the graph
    graph.add("Points", team_points.iloc[0])
    graph_data = graph.render_data_uri()
    return graph_data

def team_points_df(team_name, team_list_df):
    """Returns a dataframe giving a weekly breakdown of a team's total points
    
    :param team_name The team name to get the weekly points breakdown of
    :param team_list_df The dataframe containing the data needed (in this case we will have team_list_df = get_sheet_df('TeamList')"""

    # Get team names as a list
    team_names = list(team_list_df['Team Name'])
    
    # Trim the data to get the weekly points only
    team_list = team_list_df.drop(['Team Name', 'Team Owner', 'Batsman 1', 'Batsman 2', 'Batsman 3', 'Batsman 4', 'All-Rounder 1','All-Rounder 2', 'All-Rounder 3', 
                    'Wicket-keeper', 'Bowler 1', 'Bowler 2', 'Bowler 3', 'Total Points'], axis=1)

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
    # team_list_df = get_sheet_df('TeamList')
    # print(team_points_df('Test1 CC', team_list_df))
    pass



