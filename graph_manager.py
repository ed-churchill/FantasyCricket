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

def role_pie_chart(total_stats_df):
    """Returns a pie chart with 4 sectors: Batsmen, Bowlers, All-Rounders, Wicket-Keepers
    
    :param total_stats_df The dataframe containing the data needed (in this case we will have total_stats_df = get_sheet_df('TotalStats') """

    # Get the Player Role column
    player_roles = total_stats_df['Player Role']

    # Count occurences of each role
    count_role_df = list(player_roles.value_counts())
    bowler_count = count_role_df[0]
    batsman_count = count_role_df[1]
    all_rounder_count = count_role_df[2]
    keeper_count = count_role_df[3]

    # Generate the pie chart
    pie_chart = pygal.Pie(style=style)
    pie_chart.title = "Role Count"
    pie_chart.add('Bowlers', bowler_count)
    pie_chart.add('Batsmen', batsman_count)
    pie_chart.add('All-Rounders', all_rounder_count)
    pie_chart.add('Wicket-Keepers', keeper_count)

    # Render pie chart
    pie_data = pie_chart.render_data_uri()
    return pie_data
    
def mvp_radar_graph(total_stats_df):
    """Returns a radar graph for the MVP (person with the most total points). The radar graph breaks down their points by batting, bowling, fielding and bonus
    
    param total_stats_df The dataframe containing the data needed (in this case we will have total_stats_df = get_sheet_df('TotalStats')"""

    # Discard unecessary columns so we're left with Player Name, Player Role and their points in each category (and total points)
    total_stats = total_stats_df.drop(['Player Number', 'GAMES', 'RUNS', '4s', '6s', '50s', '100s', '150s', '200s', 'DUCKS', 'OVERS',
                        'BALLS', 'WICKETS', 'RUNS AGAINST', 'MAIDENS', '3fers/4fers', '5fers', '6+fers',
                        'CATCHES', 'RUN-OUTS', 'STUMPINGS', 'MOTM', 'WINS'], axis=1)
    

    # Sort data in decreasing order of total points and get the person with highest total points
    total_stats.sort_values(by=['TOTAL'], ascending=False, inplace=True)
    mvp_stats = list(total_stats.iloc[0])
    
    # Generate the radar chart
    mvp_name = mvp_stats[0]
    radar_chart = pygal.Radar(style=style)
    radar_chart.title = f"MVP {mvp_name}'s' points by category."
    radar_chart.x_labels = ['Batting Points', 'Bowling Points', 'Fielding Points', 'Bonus Points']
    radar_chart.add(mvp_name, mvp_stats[2:6])

    # Render the radar chart
    radar_graph_data = radar_chart.render_data_uri()
    return radar_graph_data


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
    graph = pygal.Line(style=style, margin=35)
    graph.title = f"Current Top {n} Tracker"
    graph.y_title = "Total Points"
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
    total_stats_df = get_sheet_df('TotalStats')
    mvp_radar_graph(total_stats_df)

    



