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

  
player_results = []
player_results = engine.execute(f'''
    SELECT * FROM season_stats_table WHERE tm = "{team_selected}" AND Year = "{year_selected}"
    ''').fetchall()

player_results_df = pd.DataFrame(player_results)

player_results_df.to_html(header="true", table_id="player_table")





@app.route("/")

def load_page():
    
    dates_list = []
    dates_list = list(range(1950,2019))
    
    teams_list = []
    team_file = ("../Resources/teams.csv")
    teams_df = pd.read_csv(team_file)
    teams_list = teams_df['Teams'].tolist() 
    
    year_selected = 1976
    team_selected = "TOT"
  
    return render_template("index.html", list = dates_list, list = teams_list)

if __name__ == "__main__":
    app.run(debug=True)
