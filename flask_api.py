# Import all necessary modules and create Flask app

from flask import Flask, jsonify, render_template
import pandas as pd
import datetime as dt

# create app
app = Flask(__name__)

# set up sqlalchemy engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///hawaii.sqlite')

# set up sqlalchemy base
from sqlalchemy.ext.automap import automap_base
Base = automap_base()
Base.prepare(engine, reflect=True)

# map classes
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create and map Routes

@app.route('/')
def welcome():
    return ('Welcome to the Hawaii Weather API!<br/>'
    '<br/>'
    'Available Pages:<br/>'
    '<br/>'
    '/api/v1.0/precipitation<br/>'
    '/api/v1.0/stations<br/>'
    '/api/v1.0/tobs<br/>'
    '/api/v1.0/yyyy-mm-dd<br/>'
    '/api/v1.0/yyyy-mm-dd/yyyy-mm-dd')


# dates and precipitation observations from the last year in the dataset
@app.route('/api/v1.0/precipitation')

def prev_yr_precip():
    prev_yr_start = (dt.date(2017,8,23) - dt.timedelta(days=365)).isoformat()
    query = (f'SELECT date, prcp FROM measurement \
             WHERE date > "{prev_yr_start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));

# json list of stations from the dataset.
@app.route('/api/v1.0/stations')
def station_list():
    query = 'SELECT station, name FROM station'
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));

# json list of Temperature Observations (tobs) for the previous year
@app.route('/api/v1.0/tobs')
def prev_yr_temps():
    prev_yr_start = (dt.date(2017,8,23) - dt.timedelta(days=365)).isoformat()
    query = (f'SELECT date, tobs FROM measurement \
             WHERE date > "{prev_yr_start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));

# json list of the min temp, avg temp, max temp in date range

@app.route('/api/v1.0/<start>')

# one variant where only start date given
def temps_startOnly(start):
    query = (f'SELECT AVG(tobs) AS "Average Temperature", MIN(tobs) \
             AS "Minimum Temperature", MAX(tobs) AS "Maximum Temperature" \
             FROM measurement WHERE date >= "{start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));

# one variant where both start and end date given
@app.route('/api/v1.0/<start>/<end>')
def temps_startAndEnd(start, end):
    query = (f'SELECT AVG(tobs) AS "Avg Temp", MIN(tobs) \
             AS "Min Temp", MAX(tobs) AS "Max Temp" \
             FROM measurement WHERE date >= "{start}" AND date <= "{end}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));  

# define temp
if __name__ == '__main__':
    app.run(debug=True)