
import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
stations = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    print("List all available api routes.")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()
    all_prcp = {}
    for date, prcp in results:
        all_prcp["date"] = date
        all_prcp["prcp"] = prcp

    return jsonify(all_prcp)

@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
    results = session.query(stations.station).all()

    session.close()
    all_stations = {}
    for station in results:
        all_stations["station"] = station

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    lastDayStation = dt.date(2017, 8, 23)
    lastYearStation = lastDayStation - dt.timedelta(days = 365)
    results = session.query(measurement.station, measurement.date, measurement.tobs).filter(measurement.station=="USC00519281", measurement.date >= lastYearStation).all()

    session.close()
    all_tobs = {}
    for station, date, tobs in results:
        all_tobs["station"] = station
        all_tobs["date"] = date
        all_tobs["tobs"] = tobs
    

    return jsonify(all_tobs)

@app.route("/api/v1.0/start")
def start():
    session = Session(engine)
    lastDayStation = dt.date(2017, 8, 23)
    # lastYearStation = lastDayStation - dt.timedelta(days = 365)
    results = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= lastDayStation).all()

    session.close()

    agg_start = list(np.ravel(results))

    return jsonify(agg_start)

@app.route("/api/v1.0/start/end")
def end():
    session = Session(engine)
    
    lastDayStation = dt.date(2017, 8, 23)
    lastYearStation = lastDayStation - dt.timedelta(days = 365)
    results = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.station=="USC00519281", measurement.date >= lastYearStation).all()

    session.close()
    start_end = list(np.ravel(results))

    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug=True)

