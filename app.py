from flask import Flask, render_template
from table_data_manager import generate_table_sheet, generate_league_table_df, generate_team_roster_table, generate_dream_team_table, get_sheet_df, generate_table
from graph_manager import team_points_df, top_n_league_graph, team_points_graph, role_pie_chart, mvp_radar_graph

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)


# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
@app.route("/")
def home():
    # Dataframes
    table_df = generate_league_table_df()
    total_stats_df = get_sheet_df('TotalStats')
    
    # Generate tables
    table = generate_table(table_df, link_columns=[("Team Name", "teams"), ("Team Owner", "players")])
    
    # Generate graphs
    graph = top_n_league_graph(5, table_df)
    pie_chart = role_pie_chart(total_stats_df)
    radar_graph = mvp_radar_graph(total_stats_df)

    return render_template("index.html", league_table=table, league_graph=graph, role_pie_chart=pie_chart, mvp_radar_graph=radar_graph)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dream-team")
def dream_team():
    dream_team = generate_dream_team_table()
    return render_template("dream-team.html", dream_team=dream_team)


@app.route("/teams")
def teams():
    return render_template("teams.html")

@app.route("/teams/<name>")
def team_stats(name):
    team_name = name.replace('-', ' ')

    team_list = get_sheet_df("TeamList")
    team_roster = generate_team_roster_table(team_name, team_list)

    graph = team_points_graph(team_name, team_list)

    return render_template("team-stats.html", team_roster=team_roster, graph=graph)


@app.route("/players")
def player_breakdowns():
    return render_template("players.html")

@app.route("/players/<name>")
def player_stats(name):
    name = name.replace('-', ' ')

# TODO: create a player stats page
    return render_template("player-stats.html")


@app.before_first_request
def initialize():
    # # Define the scope of the application
    # Store sheets in dictionary

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

        # Get the spreadsheet
        sheet = client.open("FantasyCricketPlayerStats")

        for i, sheet_name in enumerate(sheet_names):
            spreadsheet = sheet.get_worksheet(i)
            sheet_range = 'A2:AD200' if sheet_name != "TeamList" else 'A1:AD200'
            records_data = spreadsheet.get(sheet_range)
            df = pd.DataFrame.from_dict(records_data)
            df.columns = [x.strip() for x in df.iloc[0]]
            df = df[1:]
            df.to_csv(os.path.join('data', f'{sheet_name}.csv'), index=False)
        
        print("Sheet downloading completed")




if __name__ == "__main__":
    app.run(debug=True)
