'''
this script contains methods to retrieve a current stock data
and upload it to an SQL database

it also holds methods for retrieving data from that DB
'''
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from alpha_vantage.timeseries import TimeSeries

engine = create_engine('mysql+mysqlconnector://[user]:[pass]@[host]:[port]/[schema]', echo=False)
# data.to_sql(name='sample_table2', con=engine, if_exists = 'append', index=False)

'''
This function gets data from the DB and uses it to train new models for the
main stocks chosen.
'''
def retrieve_mains():
    pass


'''
This function does the same as the previous, but for a single specified
stock.
'''
def retrieve_choice(stock_name):
    pass