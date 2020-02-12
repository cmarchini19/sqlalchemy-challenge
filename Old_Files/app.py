################################################
# Set-up Dependencies
################################################
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table and establish session
Measurements = Base.classes.measurements
Stations = Base.classes.stations
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
	print("Server received request for 'Home' page.")
	return "Welcome to the Surfs Up Weather API!"

@app.route("/welcome")
def welcome ():
	return (
		f"Welcome to the Surf Up API<br>"
		f"Available Routes:<br>"
		f"/api/v1.0/precipitation<br>"
		f"/api/v1.0/stations<br>"
		f"/api/v1.0/tobs<br>"
		f"/api/v1.0/<start><br>"
		f"/api/v1.0<start>/<end><br>"
	)

#Precipitation route
# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     precipitation_data = session.query(Measurement.date,Measurement.prcp).all()
#     last_twelve_months = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
#     date_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=last_twelve_months).order_by(Measurement.date).all()

#     precipitation_dictionary = {date: prcp for date, prcp in precipitation}
#     return jsonify(precipitation_dictionary)

# #################################################
# 
if __name__ == '__main__':
    app.run(debug=True)





