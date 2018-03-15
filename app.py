import os
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, MetaData
import sqlite3
import json


#################################################
# Database Setup
#################################################

# Create Engine
engine = create_engine("sqlite:///housing_data.sqlite")
# Create Base
Base = declarative_base()

class Facts_table(Base):
    
    __tablename__ = 'housing_data'

    id = Column(Integer, primary_key=True)
    state = Column(String(50))
    female_salary = Column(Float)
    male_salary = Column(Float)
    combined_salary = Column(Float)
    median_home_price = Column(Float)
    name = Column(String(50))
    latitude = Column(Float)
    longtitude = Column(Float)
    ratio_total = Column(Float)
    ratio_male = Column(Float)
    ratio_female = Column(Float)
    density = Column(Float)
    unemployment = Column(Float)

    def __repr__(self):
        return f"id={self.id}, name={self.state}"


# Use `create_all` to create the tables
Base.metadata.create_all(engine)

# Verify that the table names exist in the database
engine.table_names()

# Use Pandas to Bulk insert each CSV file into their appropriate table
def populate_table(engine, table, csvfile):
    """Populates a table from a Pandas DataFrame."""
    # connect to the database
    conn = engine.connect()
    
    # Load the CSV file into a pandas dataframe 
    df_of_data_to_insert = pd.read_csv(csvfile)
    
    # Orient='records' creates a list of data to write
    # http://pandas-docs.github.io/pandas-docs-travis/io.html#orient-options
    data = df_of_data_to_insert.to_dict(orient='records')

    # Optional: Delete all rows in the table 
    conn.execute(table.delete())

    # Insert the dataframe into the database in one bulk insert
    conn.execute(table.insert(), data)

# Call the function to insert the data for each table
populate_table(engine, Facts_table.__table__, 'final_data.csv')

# Create a SQL connection to our SQLite database
con = sqlite3.connect("housing_data.sqlite")

# The result of a "cursor.execute" can be iterated over by row
df = pd.read_sql_query("SELECT * from housing_data", con)

# Be sure to close the connection
con.close()


# Load GeoJsonFile
path = 'finaldata.geojson'

with open(path) as data_file:
    df = json.load(data_file)
#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify, render_template
app = Flask(__name__, static_url_path='/static')


#Create routes
@app.route("/")
def index():
    """Return the homepage."""
    return render_template('index.html')

@app.route('/finaldata')
def finaldata():
    return jsonify(df)

# # List of states
# @app.route('/states')
# def states():
#     states_list = df[['state']]
#     states_list_ravel = list(np.ravel(states_list))
#     return jsonify(states_list_ravel)

# #List of male salaries
# @app.route('/male')
# def male():
#     male_list = df[['male_salary']]
#     male_list_ravel = list(np.ravel(male_list))
#     return jsonify(male_list_ravel)

# #List of female salaries
# @app.route('/female')
# def female():
#     female_list = df[['female_salary']]
#     female_list_ravel = list(np.ravel(female_list))
#     return jsonify(female_list_ravel)

# #List of combined salaries
# @app.route('/combined')
# def combined():
#     combined_list = df[['combined_salary']]
#     combined_list_ravel = list(np.ravel(combined_list))
#     return jsonify(combined_list_ravel)

# #List of Median home prices
# @app.route('/medianhomeprice')
# def medianhomeprice():
#     medianhomeprice_list = df[['median_home_price']]
#     medianhomeprice_list_ravel = list(np.ravel(medianhomeprice_list))
#     return jsonify(medianhomeprice_list_ravel)

# #List of latitudes
# @app.route('/latitude')
# def latitude():
#     latitude_list = df[['latitude']]
#     latitude_list_ravel = list(np.ravel(latitude_list))
#     return jsonify(latitude_list_ravel)

# #List of longtitudes
# @app.route('/longtitude')
# def longtitude():
#     longtitude_list = df[['longtitude']]
#     longtitude_list_ravel = list(np.ravel(longtitude_list))
#     return jsonify(longtitude_list_ravel)    

if __name__ == "__main__":
    app.run(debug=True)
