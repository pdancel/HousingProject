
# coding: utf-8

# In[23]:


# Imports
### END SOLUTION
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
### END SOLUTION


# In[24]:


# Create Engine
### BEGIN SOLUTION
engine = create_engine("sqlite:///test.sqlite")
### END SOLUTION


# In[25]:


Base = declarative_base()


# In[26]:


class Facts_table(Base):
    
    __tablename__ = 'facts_table'

    id = Column(Integer, primary_key=True)
    state = Column(String(50))
    female_salary = Column(Float)
    male_salary = Column(Float)
    combined_salary = Column(Float)
    median_home_price = Column(Float)
    latitude = Column(Float)
    longtitude = Column(Float)
    
    def __repr__(self):
        return f"id={self.id}, name={self.state}"


# In[27]:


# Use `create_all` to create the tables
### BEGIN SOLUTION
Base.metadata.create_all(engine)
### END SOLUTION


# In[28]:


# Verify that the table names exist in the database
### BEGIN SOLUTION
engine.table_names()
### END SOLUTION


# In[29]:


# Use Pandas to Bulk insert each CSV file into their appropriate table
### BEGIN SOLUTION
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


# In[30]:


# Call the function to insert the data for each table
populate_table(engine, Facts_table.__table__, 'test.csv')
#populate_table(engine, facts_table.__table__, 'FACT_TABLE.csv')


# In[31]:


import sqlite3


# In[32]:


# Create a SQL connection to our SQLite database
con = sqlite3.connect("test.sqlite")

# The result of a "cursor.execute" can be iterated over by row
df = pd.read_sql_query("SELECT * from facts_table", con)

# Be sure to close the connection
con.close()


# In[33]:


df.head()

