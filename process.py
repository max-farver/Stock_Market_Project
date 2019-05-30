'''
this script contains methods to retrieve a current stock data
and upload it to an SQL database

it also holds methods for retrieving data from that DB
'''
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from alpha_vantage.timeseries import TimeSeries
import configparser

ts = TimeSeries(key='1W79PCAA71QM8Q85', output_format='pandas')

USER = configparser.get('SQL', 'USER')
PASSWORD = configparser.get('SQL', 'PASSWORD')
HOST = configparser.get('SQL', 'HOST')
PORT = configparser.get('SQL', 'PORT')
SCHEMA = configparser.get('SQL', 'SCHEMA')

engine = create_engine('mysql+mysqlconnector://'+ USER + ':'+ PASSWORD + \
    '@' + HOST + ':'+ PORT + '/' + SCHEMA, echo=False)
# data.to_sql(name='sample_table2', con=engine, if_exists = 'append', index=False)

'''
This function gets data from the DB and uses it to train new models for the
main stocks chosen.
'''
def process_mains():
    AMD, _ = ts.get_intraday(symbol='AMD',interval='1min', outputsize='full')
    NVDA, _ = ts.get_intraday(symbol='NVDA',interval='1min', outputsize='full')
    DOW, _ = ts.get_intraday(symbol='DOW',interval='1min', outputsize='full')

    AMD['Symbol'] = 'AMD'
    NVDA['Symbol'] = 'NVDA'
    DOW['Symbol'] = 'DOW'

    AMD.to_sql('stocks_info', engine)
    NVDA.to_sql('stocks_info', engine)
    DOW.to_sql('stocks_info', engine)


'''
This function does the same as the previous, but for a single specified
stock.
'''
def process_choice(stock_name):
    pass