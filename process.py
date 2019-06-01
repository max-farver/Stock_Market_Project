'''
this script contains methods to retrieve a current stock data
and upload it to an SQL database

it also holds methods for retrieving data from that DB
'''
import pandas as pd
import numpy as np
import mysql.connector
from sqlalchemy import create_engine
from alpha_vantage.timeseries import TimeSeries
import configparser

import quandl

quandl.ApiConfig.api_key = ('UfinkxKK8xK2idy3N66A')

import model, app, visuals

ts = TimeSeries(key='1W79PCAA71QM8Q85', output_format='pandas')

config = configparser.ConfigParser()
config.read('config.txt')
USER = config['SQL']['USER']
PASSWORD = config['SQL']['PASSWORD']
HOST = config['SQL']['HOST']
PORT = config['SQL']['PORT']
SCHEMA = config['SQL']['SCHEMA']

engine = create_engine('mysql+mysqlconnector://'+ USER + ':'+ PASSWORD + \
    '@' + HOST + ':'+ PORT + '/' + SCHEMA, echo=False)
# data.to_sql(name='sample_table2', con=engine, if_exists = 'append', index=False)


def preprocess(data):
    pass


'''
This function gets data from the DB and uses it to train new models for the
main stocks chosen.
'''
def process_mains():
    # AMD, _ = ts.get_intraday(symbol='AMD',interval='1min', outputsize='full')
    # NVDA, _ = ts.get_intraday(symbol='NVDA',interval='1min', outputsize='full')
    # DOW, _ = ts.get_intraday(symbol='DOW',interval='1min', outputsize='full')

    data = quandl.get_table(
        'WIKI/PRICES',
        ticker=['AMD', 'NVDA', 'DOW'],
        qopts = { 'columns': ['ticker', 'date', 'adj_close'] },
        date = { 'gte': '2000-1-1' },
        paginate=True
        )

    AMD = data[data['ticker'] == 'AMD']
    NVDA = data[data['ticker'] == 'NVDA']
    DOW = data[data['ticker'] == 'DOW']

    AMD = AMD.set_index('date')
    NVDA = NVDA.set_index('date')
    DOW = DOW.set_index('date')

    # AMD['Symbol'] = 'AMD'
    # NVDA['Symbol'] = 'NVDA'
    # DOW['Symbol'] = 'DOW'

    AMD.to_sql('stocks_info', engine, if_exists='append')
    NVDA.to_sql('stocks_info', engine, if_exists='append')
    DOW.to_sql('stocks_info', engine, if_exists='append')

    # First need to get the last week's data from DB
    conn = engine.connect()
    
    res = conn.execute('SELECT * FROM stock_info WHERE ticker = \'AMD\'')
    AMD = pd.DataFrame(res.fetchall())
    AMD.columns = res.keys()

    res = conn.execute('SELECT * FROM stock_info WHERE ticker = \'NVDA\'')
    AMD = pd.DataFrame(res.fetchall())
    AMD.columns = res.keys()

    res = conn.execute('SELECT * FROM stock_info WHERE ticker = \'DOW\'')
    AMD = pd.DataFrame(res.fetchall())
    AMD.columns = res.keys()

    AMD = preprocess(AMD)
    NVDA = preprocess(NVDA)
    DOW = preprocess(DOW)

    AMD_model, NVDA_model, DOW_model = model.model_mains(AMD, NVDA, DOW)

    AMD_pred = model.predict(AMD_model)
    NVDA_pred = model.predict(NVDA_model)
    DOW_pred = model.predict(DOW_model)

    visuals.render_mains(AMD, NVDA, DOW, AMD_pred, NVDA_pred, DOW_pred)


'''
This function does the same as the previous, but for a single specified
stock.
'''
def process_choice(stock_symbol):
    # If table don't exist, Create.
    if not engine.dialect.has_table(engine, Variable_tableName):
        
        
    
    data, _ = ts.get_intraday(symbol=stock_symbol,interval='1min', outputsize='full')
    data['Symbol'] = stock_symbol
    data.to_sql('stocks_info', engine, if_exists='append')

    data = preprocess(data)
    data_model = model.model_choice(data)
    data_pred = model.predict_choice(data, data_model)
    
    visuals.render_choice(data, data_pred)