import numpy as np
import pymysql
pymysql.install_as_MySQLdb()

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
engine = create_engine("mysql://sql3281240:3uMQwePUij@sql3.freemysqlhosting.net:3306/sql3281240")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
test_table = Base.classes.test_table

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
  print('tryit out!!!')
  return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
