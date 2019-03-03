import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, jsonify, render_template

# Database Setup
#################################################
engine = create_engine("mysql://root:Batman!99@localhost:3306/season_stats_db")

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")

def load_page():
    year_list = []
    year_list = list(range(1950,2019))
    
    teams_list = []
    team_file = ("../Resources/teams.csv")
    teams_df = pd.read_csv(team_file)
    team_list = teams_df['Teams'].tolist() 
  
    return render_template("index.html", team_list = team_list, year_list = year_list)
@app.route("/results")

def results_page():

    year_selected = 1977
    team_selected = "TOT"

    player_results = []
    player_results = engine.execute(f'''
        SELECT * FROM season_stats_table WHERE tm = "{team_selected}" AND Year = "{year_selected}"
        ''').fetchall()
    player_results_df = pd.DataFrame(player_results)

    player_results_df  = player_results_df.rename(columns={player_results_df.columns[2]: "Year", \
                                        player_results_df.columns[3]: "Player", \
                                        player_results_df.columns[4]: "Position", \
                                        player_results_df.columns[5]: "Age", \
                                        player_results_df.columns[6]: "Tm", \
                                        player_results_df.columns[7]: "G", \
                                        player_results_df.columns[8]: "GS", \
                                        player_results_df.columns[9]: "MP", \
                                        player_results_df.columns[10]: "PER", \
                                        player_results_df.columns[11]: "TS%", \
                                        player_results_df.columns[12]: "3PAr", \
                                        player_results_df.columns[13]: "FTr", \
                                        player_results_df.columns[14]: "STL", \
                                        player_results_df.columns[15]: "BLK", \
                                        player_results_df.columns[16]: "TOV", \
                                        player_results_df.columns[17]: "PF", \
                                        player_results_df.columns[18]: "PTS"})

    year_list       = player_results_df['Year'].tolist()
    player_list     = player_results_df['Player'].tolist()
    position_list   = player_results_df['Position'].tolist()
    age_list     = player_results_df['Age'].tolist()
    tm_list       = player_results_df['Tm'].tolist()
    g_list     = player_results_df['G'].tolist()
    gs_list   = player_results_df['GS'].tolist()
    mp_list     = player_results_df['MP'].tolist()
    per_list       = player_results_df['PER'].tolist()
    ts_list     = player_results_df['TS%'].tolist()
    par_list   = player_results_df['3PAr'].tolist()
    ftr_list     = player_results_df['FTr'].tolist()
    stl_list       = player_results_df['STL'].tolist()
    blk_list     = player_results_df['BLK'].tolist()
    tov_list   = player_results_df['TOV'].tolist()
    pf_list     = player_results_df['PF'].tolist()
    pts_list     = player_results_df['PTS'].tolist()

    players = list(zip(year_list, player_list, position_list, age_list, tm_list, g_list, \
                    gs_list, mp_list, per_list, ts_list, par_list, ftr_list, stl_list, blk_list, tov_list, pf_list, pts_list))

    years_list = []
    years_list = list(range(1950,2019))
    
    teams_list = []
    team_file = ("../Resources/teams.csv")
    teams_df = pd.read_csv(team_file)
    team_list = teams_df['Teams'].tolist() 
  
    return render_template("index.html", team_list = team_list, years_list = years_list, players = players )

if __name__ == "__main__":
    app.run(debug=True)
