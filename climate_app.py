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
def precipitation():
    precipdict = {}
    response = session.query(Measurement.date,Measurement.prcp).all()
    for record in response:
        recdict = {record.date: record.prcp}
        precipdict.update(recdict)
    session.close()
    return jsonify(precipdict)



    # precipitation_data = session.query(Measurement.date, Measurement.prcp).all()
    # last_twelve_months = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    # date_query = session.query(Measurement.date, Measurement.prcp).\
    #     filter(Measurement.date>=last_twelve_months).\
    #     order_by(Measurement.date).all()

    # prcp_dictionary = {}
    # for prcp in response:
    #     prcpdict = {prcp.date: prcp.prcp}
    #     prcpdata.update(prcpdict)
    # return jsonify(prcp_dictionary)

#Stations route
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.name).all()
    station_list = list(np.ravel(stations))
    return jsonify (station_list)

#Temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    tempdict = {}
    # get latest date
    latestdate = session.query(func.max(Measurement.date)).first()
    for date in latestdate:
        daten = dt.datetime.strptime(date,'%Y-%m-%d').date()
    # find what one year before the latest date is
    oneyearbefore = daten - dt.timedelta(days=365)
    # query data for the data from the last year
    response = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= oneyearbefore).all()
    for record in response:
        recdict = {record.date: record.tobs}
        tempdict.update(recdict)
    session.close()
    return jsonify(tempdict)


# @app.route("/api/v1.0/tobs")




# <Start> route

# @app.route("/api/v1.0/<start>")
# def tstart(start):
#     # check date format for start date
#     try:
#         dt.datetime.strptime(start, '%Y-%m-%d')
#     except ValueError:
#         return (f"Incorrect start date format, should be YYYY-MM-DD<br/>"
#                 f"If you are not looking for a dated endpoint, check your spelling"), 404
#     # get database query and return
#     response = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).first()
#     respdict = {'TMIN':response[0],
#                 'TAVG':response[1],
#                 'TMAX':response[2]}
#     session.close()
#     return jsonify(respdict)



# #################################################
# 
if __name__ == '__main__':
    app.run(debug=True)

