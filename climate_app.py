################################################
# Set-up Dependencies
################################################
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table and establish session
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")

# Home page route
def home():
	return (
		f"Welcome to the Surf Up API<br>"
		f"Available Routes:<br>"
		f"/api/v1.0/precipitation<br>"
		f"/api/v1.0/stations<br>"
		f"/api/v1.0/tobs<br>"
		f"/api/v1.0/start<br>"
		f"/api/v1.0/start/end<br>"
	)

#Precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    prcp_data = session.query(Measurement.date,Measurement.prcp).all()

    all_prcp = []
    for date, prcp in prcp_data:
        prcp_data_dict = {}
        prcp_data_dict["date"] = date
        prcp_data_dict["prcp"] = prcp
        all_prcp.append(prcp_data_dict)
    return jsonify(all_prcp)

#Stations route
@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Station.name).all()

    all_stations = []
    for name in station_data:
        station_data_dict = {}
        station_data_dict["name"] = name
        all_stations.append(station_data_dict)
    return jsonify (all_stations)

# #Temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    last_twelve_months = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    temp_data = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= last_twelve_months).all()

    all_temps = []
    for tobs in temp_data:
        temp_data_dict = {}
        temp_data_dict["date"] = date
        temp_data_dict["tobs"] = tobs
        all_temps.append(temp_data_dict)
    return jsonify (all_temps)

# @app.route("/api/v1.0/tobs")




# <Start> route



# #################################################
if __name__ == '__main__':
    app.run(debug=True)

