from flask import Flask, render_template
from table_data_manager import generate_table_sheet, generate_league_table_df, generate_team_roster_table, generate_dream_team_table, get_sheet_df, generate_table, team_to_owner, generate_picks_table, name_to_picks, generate_points_calculator_table, generate_teams_table, generate_players_table
from graph_manager import team_points_df, team_points_stacked_bar_graph, team_points_stacked_line_graph, top_n_league_graph, role_pie_chart, mvp_radar_graph, team_roster_radar_graph, player_points_df, player_points_bar_graph, player_points_line_graph, player_points_radar_graph, team_players_breakdown_df

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)


# -------------------------------------------------------------------------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

# -------------------------------------------------------------------------------
@app.route("/")
def home():
    # Dataframes
    table_df = generate_league_table_df()
    total_stats_df = get_sheet_df('TotalStats')
    
    # Generate tables
    league_table = generate_table(table_df, link_columns=[("Team Name", "teams")])
    dream_team = generate_dream_team_table(total_stats_df)
    
    # Generate graphs
    tracker_graph = top_n_league_graph(5, table_df)
    pie_chart = role_pie_chart(total_stats_df)
    radar_graph = mvp_radar_graph(total_stats_df)

    return render_template("index.html", league_table=league_table, dream_team=dream_team, tracker_graph=tracker_graph, role_pie_chart=pie_chart, mvp_radar_graph=radar_graph)


@app.route("/about")
def about():
    
    # Generate the points calculator table
    points_table = generate_points_calculator_table()

    return render_template("about.html", points_table=points_table)


@app.route("/dream-teams")
def dream_teams():
    
    # Generate current dream team table
    total_stats = get_sheet_df("TotalStats")
    current_team = generate_dream_team_table(total_stats)

    # Get a list of the weeks that we will generate the dream team tables for
    week_names = []
    week_nums = []
    for i in range(0, 10):
        # Get sheet for the week
        sheet_name = f'Week{i+1}'
        week_df = get_sheet_df(sheet_name)

        # Check degeneracy
        if generate_dream_team_table(week_df) == "":
            continue
        else:
            week_names.append(f"Week{i+1}")
            week_nums.append(i+1)
    
    # Generate tables and store in a list
    weekly_teams = []
    for week_name in week_names:
        weekly_teams.append(generate_dream_team_table(get_sheet_df(week_name)))

    return render_template("dream-teams.html", current_team=current_team, week_nums=week_nums, weekly_teams=weekly_teams)


@app.route("/teams")
def teams():
    
    # Get TeamList dataframe
    team_list = get_sheet_df('TeamList')

    # Generate table of all the teams
    teams_table = generate_teams_table(team_list)
    
    return render_template("teams.html", teams_table=teams_table)

@app.route("/teams/<name>")
def team_stats(name):
    # Remove dash in team name for display purposes
    team_name = name.replace('-', ' ')

    # Get the TeamList and TotalStats sheets as dataframes
    team_list = get_sheet_df("TeamList")
    total_stats = get_sheet_df("TotalStats")

    # Get the team owner
    team_owner = team_to_owner(team_name, team_list)

    # Generate the team roster table
    team_roster = generate_team_roster_table(team_name, team_list)

    # Generate the weekly points bar graph for the team
    breakdown_df = team_players_breakdown_df(team_name, team_list)
    bar_graph = team_points_stacked_bar_graph(team_name, breakdown_df)

    # Generate the weekly points cumulative line graph for the team
    line_graph = team_points_stacked_line_graph(team_name, breakdown_df)

    # Generate the team roster radar graph
    radar_graph = team_roster_radar_graph(team_name, team_list, total_stats)


    return render_template("team-stats.html", team_name=team_name, team_owner=team_owner, 
                            team_roster=team_roster, bar_graph=bar_graph, 
                            line_graph=line_graph, radar_graph=radar_graph)


@app.route("/players")
def players():

    # Get PlayerList Sheet
    player_list = get_sheet_df('PlayerList')

    # Generate player list table
    players_table = generate_players_table(player_list)

    return render_template("players.html", players_table=players_table)

@app.route("/players/<name>")
def player_stats(name):
    # Remove dash in player name for display purposes
    player_name = name.replace('-', ' ')

    # Get the TeamList sheet as a dataframe
    team_list = get_sheet_df('TeamList')

    # Get the weekly sheets and TotalStats sheet as dataframes
    weekly_dfs = [get_sheet_df('Week1'), get_sheet_df('Week2'), get_sheet_df('Week3'), get_sheet_df('Week4'),
                get_sheet_df('Week5'), get_sheet_df('Week6'), get_sheet_df('Week7'), get_sheet_df('Week8'), get_sheet_df('Week9'),
                get_sheet_df('Week10'), get_sheet_df('TotalStats')]

    # Get the player points dataframes
    player_points = player_points_df(player_name, weekly_dfs)

    # Generate the player points bar graph
    bar_graph = player_points_bar_graph(player_name, player_points)

    # Generate the player points cumulative line graph
    line_graph = player_points_line_graph(player_name, player_points)

    # Generate the player points radar graph
    radar_graph = player_points_radar_graph(player_name, player_points)

    # Generate the picks table and get the total picks
    picks_table = generate_picks_table(player_name, team_list)
    total_picks = name_to_picks(player_name, team_list)[1]

    return render_template("player-stats.html", player_name=player_name, 
                            bar_graph=bar_graph, line_graph=line_graph,
                            total_picks=total_picks, radar_graph=radar_graph, picks_table=picks_table)


def initialize():
    # check if the data folder is empty
    if not os.listdir("data"):
        print("Downloading sheets from google sheets")
        sheet_names = ["Week1", "Week2", "Week3", "Week4", "Week5", "Week6", "Week7",
                    "Week8", "Week9", "Week10", "TotalStats", "TeamList"]

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

        # Add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)

        # Authorise the client sheet
        client = gspread.authorize(creds)

        # Get the stats spreadsheets
        sheet = client.open("FantasyCricketPlayerStats")

        for i, sheet_name in enumerate(sheet_names):
            spreadsheet = sheet.get_worksheet(i)
            sheet_range = 'A2:AD200' if sheet_name != "TeamList" else 'A1:AD200'
            records_data = spreadsheet.get(sheet_range)
            df = pd.DataFrame.from_dict(records_data)
            df.columns = [x.strip() for x in df.iloc[0]]
            df = df[1:]
            df.to_csv(os.path.join('data', f'{sheet_name}.csv'), index=False)
        
        # Get the FantasyCricketTeamSelection spreadsheet
        team_selection_sheet = client.open('FantasyCricketTeamSelection')
        player_list = team_selection_sheet.get_worksheet(0)

        # Trim the FantasyCricketTeamSelection spreadsheet
        sheet_range = 'B2:E200'
        records_data = player_list.get(sheet_range)

        # Convert sheet to csv
        df = pd.DataFrame.from_dict(records_data)
        df.columns = ['Player Name', 'Squad', 'Role', 'Price (M)']
        df.to_csv(os.path.join('data', 'PlayerList.csv'), index=False)

        print("Sheet downloading completed")




if __name__ == "__main__":
    initialize()
    app.run(debug=True)
