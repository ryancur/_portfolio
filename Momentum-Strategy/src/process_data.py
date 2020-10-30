import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    pd.set_option('max_columns', 100)

    ### TEST CODE ###
    '''
    input(s): list of file names
    output(s): dataframe with date as the index, ticker symbol as the column
        header, and adjusted close price as the values in the rows
    assumptions:
        - historical stock data from Yahoo Finance
        - stock data columns: Date, Open, High, Low, Close, Adj Close, Volume
    pseudocode:
        ...
    '''

    # column names stored in dictionary
    column_names = {'Date': 'date', 'Open': 'open', 'High': 'high',
                    'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close',
                    'Volume': 'volume'}

    ticker_symbols = ['AAPL', 'AMD', 'AMZN', 'CSCO', 'FB', 'GOOG', 'IBM', 'INTC',
                        'NFLX', 'NVDA', 'ORCL', 'SNAP', 'SQ', 'TEAM', 'TSLA']

    df = pd.DataFrame([])

    for ticker in ticker_symbols:
        df_ticker = pd.read_csv(f"../data/{ticker}.csv", parse_dates=['Date'], index_col=False)
        df_ticker.rename(columns=column_names, inplace=True)
        df_ticker['ticker'] = ticker
        df = df.append(df_ticker, ignore_index=True)

    # use a pivot table to get ticker symbols as columns
    close = df.reset_index().pivot(index='date', columns='ticker', values='adj_close')

    # read in data
    # df_aapl = pd.read_csv(f'../data/AAPL.csv', parse_dates=['Date'], index_col=False)
    # df_amd = pd.read_csv('../data/AMD.csv', parse_dates=['Date'], index_col=False) #test dataframe

    # rename column names for dataframe
    # df_amd.rename(columns=column_names, inplace=True)
    # df_aapl.rename(columns=column_names, inplace=True)

    # set date column as index - this might go somewhere else
    #df_amd.set_index('date', inplace=True)

    # add ticker symbol - this will need to be based on the filename or something
    # df_amd['ticker'] = 'AMD'
    # df_aapl['ticker'] = 'AAPL'

    # append the aapl prices to the amd dataframe - test
    # df = df_amd.append(df_aapl, ignore_index=True)
