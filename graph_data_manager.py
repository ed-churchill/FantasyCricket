from table_data_manager import numbers_to_names, get_sheet_df, generate_league_table_df
import pygal
from pygal.style import DarkGreenBlueStyle, DefaultStyle, DarkStyle

###-------------------------------------------------------------
# Graph data for Home page
###-------------------------------------------------------------

style = DarkStyle

def cumulative(ls):
    value = 0
    new_ls = []
    for x in ls:
        value += x
        new_ls.append(value)
    return new_ls

def count_trailing_zeros(ls):
    count = 0
    for x in ls[::-1]:
        if x  == 0:
            count += 1
    return count

def top_n_league_graph(n, league_df):
    # Get top n teams from league table
    top_n = list(league_df.head(n)["Team Name"])

    # Get the top n teams' weekly points breakdown
    team_list = get_sheet_df("TeamList")

    data = [list(team_points_df(y, team_list).iloc[0]) for y in top_n]
    min_zeros = min([count_trailing_zeros(x) for x in data])
    data = [cumulative(x)[:-min_zeros] for x in data]


    graph = pygal.Line(style=style)
    graph.title = f"Weekly Points Breakdown of current top {n}"
    graph.x_labels = [f"Week {x}" for x in range(1, 11)]
    for team, values in zip(top_n, data):
        graph.add(team, values)
    graph_data = graph.render_data_uri()

    return graph_data

###-------------------------------------------------------------
# Graph data for Teams page
###-------------------------------------------------------------
def team_points_graph(team_name, team_list_df):
    team_points = team_points_df(team_name, team_list_df)
    graph = pygal.Bar(style=DarkGreenBlueStyle)
    graph.title = "Team points"
    graph.x_labels = [f"Week {x}" for x in range(1, 11)]
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



