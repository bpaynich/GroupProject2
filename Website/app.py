import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

import googlemaps
import gmaps
import matplotlib.pyplot as plt
import json
import warnings
import gmaps.geojson_geometries
from matplotlib.cm import viridis
from matplotlib.colors import to_hex
from matplotlib.cm import viridis

# Hide warning messages
from ipywidgets.embed import embed_minimal_html
warnings.filterwarnings('ignore')

# Google developer API key
from config import gkey

# Access maps with unique API key
gmaps.configure(api_key=gkey)
gm = googlemaps.Client(key=gkey)
gmaps.configure(api_key=gkey) 

import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, jsonify, render_template, request

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

years_list = []
years_list = list(range(1950,2019))
    
teams_list = []
team_file = ("../Resources/teams.csv")
teams_df = pd.read_csv(team_file)
team_list = teams_df['Teams'].tolist()

#year_selected = 1995
#team_selected = "PHO"

    
@app.route("/info", methods = ['GET','POST'])

def results_page():

    year_selected = request.args.get('year')
    team_selected = request.args.get('team')
    team_year = year_selected
    full_team_name = "Phoenix Suns"
    lat = 33.4457369
    longitude = -112.0712006

    arena_name = "Talking Stick Arena"
    arena_street = "401 E Jefferson" 
    arena_city = "Phoenix"
    arena_state = "Arizona"
    arena_zip = "85201"


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

    return render_template("index.html", full_team_name = full_team_name, team_list = team_list, years_list = years_list, players = players, lat=lat, longitude=longitude, \
        arena_name = arena_name, arena_street = arena_street, arena_city = arena_city, arena_state = arena_state, arena_zip = arena_zip, team_year = team_year )

if __name__ == "__main__":
    app.run(debug=True)
