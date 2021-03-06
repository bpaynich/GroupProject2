import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

import googlemaps
import gmaps
import json
import warnings
import gmaps.geojson_geometries

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
team_file = ("../Resources/ab_map.csv")
teams_df = pd.read_csv(team_file)
team_list = teams_df['abbreviations'].tolist()

@app.route("/", methods = ['GET','POST'])

def query():
    years_list = []
    years_list = list(range(1950,2017))
        
    teams_list = []
    team_file = ("../Resources/ab_map.csv")
    teams_df = pd.read_csv(team_file)
    team_list = teams_df['abbreviations'].tolist()

    if request.method == 'POST':
        year = request.form.get('year')
        team = request.form.get('team')

    return render_template("index.html", team_list = team_list, years_list = years_list)


@app.route("/info", methods = ['GET','POST'])

def results_page():

    year_selected = request.args.get('year')
    team_selected = request.args.get('team')
    team_year = year_selected

    player_results = []
    player_results = engine.execute(f'''
        select s.Year, s.Player, s.Pos, s.Age, s.Tm, s.G, s.GS, s.MP, s.PER, s.TS, s.PAr, s.FTr, s.STL, s.BLK, s.TOV, s.PF, s.PTS, a.TeamName 
        from season_stats_table AS s INNER JOIN abv_map_table as a ON s.Tm = a.abbreviations 
        WHERE tm = "{team_selected}" and Year = "{year_selected}"
        ''').fetchall()
    player_results_df = pd.DataFrame(player_results)

    player_results_df  = player_results_df.rename(columns={player_results_df.columns[0]: "Year", \
                                        player_results_df.columns[1]: "Player", \
                                        player_results_df.columns[2]: "Position", \
                                        player_results_df.columns[3]: "Age", \
                                        player_results_df.columns[4]: "Tm", \
                                        player_results_df.columns[5]: "G", \
                                        player_results_df.columns[6]: "GS", \
                                        player_results_df.columns[7]: "MP", \
                                        player_results_df.columns[8]: "PER", \
                                        player_results_df.columns[9]: "TS", \
                                        player_results_df.columns[10]: "PAr", \
                                        player_results_df.columns[11]: "FTr", \
                                        player_results_df.columns[12]: "STL", \
                                        player_results_df.columns[13]: "BLK", \
                                        player_results_df.columns[14]: "TOV", \
                                        player_results_df.columns[15]: "PF", \
                                        player_results_df.columns[16]: "PTS", \
                                        player_results_df.columns[17]: "TeamName"})

    year_list       = player_results_df['Year'].tolist()
    player_list     = player_results_df['Player'].tolist()
    position_list   = player_results_df['Position'].tolist()
    age_list     = player_results_df['Age'].tolist()
    tm_list       = player_results_df['Tm'].tolist()
    g_list     = player_results_df['G'].tolist()
    gs_list   = player_results_df['GS'].tolist()
    mp_list     = player_results_df['MP'].tolist()
    per_list       = player_results_df['PER'].tolist()
    ts_list     = player_results_df['TS'].tolist()
    par_list   = player_results_df['PAr'].tolist()
    ftr_list     = player_results_df['FTr'].tolist()
    stl_list       = player_results_df['STL'].tolist()
    blk_list     = player_results_df['BLK'].tolist()
    tov_list   = player_results_df['TOV'].tolist()
    pf_list     = player_results_df['PF'].tolist()
    pts_list     = player_results_df['PTS'].tolist()
    full_team_name_list     = player_results_df['TeamName'].tolist()
    players = list(zip(year_list, player_list, position_list, age_list, tm_list, g_list, \
                    gs_list, mp_list, per_list, ts_list, par_list, ftr_list, stl_list, blk_list, tov_list, pf_list, pts_list))
    full_team_name = full_team_name_list[0]

    # Labels for address, team names, coordinates
    #full_team_name = "Phoenix Suns"
    lat = 33.4457369
    longitude = -112.0712006
    arena_name   = "Talking Stick Arena"
    arena_street = "401 E Jefferson" 
    arena_city   = "Phoenix"
    arena_state  = "Arizona"
    arena_zip    = "85201"

    players = list(zip(year_list, player_list, position_list, age_list, tm_list, g_list, \
                    gs_list, mp_list, per_list, ts_list, par_list, ftr_list, stl_list, blk_list, tov_list, pf_list, pts_list))

    return render_template("index.html", full_team_name = full_team_name, team_list = team_list, years_list = years_list, players = players, lat=lat, longitude=longitude, \
        arena_name = arena_name, arena_street = arena_street, arena_city = arena_city, arena_state = arena_state, arena_zip = arena_zip, team_year = team_year )

if __name__ == "__main__":
    app.run(debug=True)
