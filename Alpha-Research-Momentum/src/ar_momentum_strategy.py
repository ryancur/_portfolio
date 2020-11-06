import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pandas._testing import assert_frame_equal

def resample_prices(close_prices, freq='M'):
    """
    Resample close prices for each ticker at a specified frequency.

    Parameters
    ----------
    close_prices : DataFrame
        Close prices for each ticker and date
    freq : str
        Frequency to sample at
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html

    Returns
    -------
    prices_resampled : DataFrame
        Resampled prices for each ticker and date
    """
    return close_prices.resample(freq).last()

def compute_log_returns(prices):
    """
    Compute log returns for each ticker.

    Parameters
    ----------
    prices : DataFrame
        Prices for each ticker and date

    Returns
    -------
    log_returns : DataFrame
        Log returns for each ticker and date
    """
    return np.log(prices) - np.log(prices.shift(1))

def shift_returns(returns, shift_n):
    """
    Generate shifted returns

    Parameters
    ----------
    returns : DataFrame
        Returns for each ticker and date
    shift_n : int
        Number of periods to move, can be positive or negative

    Returns
    -------
    shifted_returns : DataFrame
        Shifted returns for each ticker and date
    """
    return returns.shift(shift_n)

def get_top_n(prev_returns, top_n):
    """
    Select the top performing stocks

    Parameters
    ----------
    prev_returns : DataFrame
        Previous shifted returns for each ticker and date
    top_n : int
        The number of top performing stocks to get

    Returns
    -------
    top_stocks : DataFrame
        Top stocks for each ticker and date marked with a 1
    """
    new_df = pd.DataFrame(0, index=prev_returns.index.values,
                            columns=prev_returns.columns)
    for idx, row in prev_returns.iterrows():
        top = row.nlargest(top_n).index.values.tolist()
        for ticker in new_df.columns:
            if ticker in top:
                new_df.loc[idx, ticker] = 1
    return new_df

def portfolio_returns(df_long, df_short, lookahead_returns, n_stocks):
    """
    Compute expected returns for the portfolio, assuming equal investment in
    each long/short stock.

    Parameters
    ----------
    df_long : DataFrame
        Top stocks for each ticker and date marked with a 1
    df_short : DataFrame
        Bottom stocks for each ticker and date marked with a 1
    lookahead_returns : DataFrame
        Lookahead returns for each ticker and date
    n_stocks: int
        The number number of stocks chosen for each month

    Returns
    -------
    portfolio_returns : DataFrame
        Expected portfolio returns for each ticker and date
    """
    pos_long = lookahead_returns * df_long
    pos_short = lookahead_returns * df_short
    total_returns = (pos_long - pos_short)/n_stocks
    return total_returns

def analyze_alpha(expected_portfolio_returns_by_date):
    """
    Perform a t-test with the null hypothesis being that the expected mean
    return is zero.

    Parameters
    ----------
    expected_portfolio_returns_by_date : Pandas Series
        Expected portfolio returns for each date

    Returns
    -------
    t_value
        T-statistic from t-test
    p_value
        Corresponding p-value
    """
    null_hypothesis = 0.0
    t, p = stats.ttest_1samp(expected_portfolio_returns_by_date,
                                null_hypothesis)
    p = p/2
    return t, p

def preprocess_data(ticker_list, values='Adj Close', relative_path=''):
    """
    Aggregate multiple csv files of OHLC data into a table where each ticker is
    the column header and the values are the sort_by input.
    Assumes:
        Historical data has the columns: Date, Open, High, Low, Close,
            Adj Close, Volume.
        Data is stored as ticker.csv --> AAPL.csv

    Parameters
    ----------
    ticker_list : List
        List of ticker symbols. ['AAPL', 'FB', 'GOOG']
    values : String
        Column name of the values in the returned dataframe. Default is
        'Adj Close'.
    relative_path : String
        Relative path to where the data is stored. Default is local folder.
        If the data is in another folder, format example: '../data/'

    Returns
    -------
    prices: DataFrame
        dataframe with ticker symbols as column names, date as index and
        values as row values.

    """
    column_names = {'Date': 'date', 'Open': 'open', 'High': 'high',
                    'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close',
                    'Volume': 'volume'}
    df = pd.DataFrame([])
    values_column = '_'.join(values.lower().split())
    for ticker in ticker_list:
        try:
            df_ticker = pd.read_csv(f"{relative_path}{ticker}.csv",
                                    parse_dates=['Date'], index_col=False)
            df_ticker.rename(columns=column_names, inplace=True)
            df_ticker['ticker'] = ticker
            df = df.append(df_ticker, ignore_index=True)
        except:
            print(f"{ticker} not in files.")
            continue
    try:
        prices = df.reset_index().pivot(index='date', columns='ticker',
                                    values=values_column)
    except:
        return None
    return prices

def test_preprocess_data():
    """
    Test function for preprocess_data function
    """
    test_status_list = []
    test_counter = 0
    total_tests = 3
    df_1 = preprocess_data(['AAPL'], values='Adj Close',
                            relative_path='../data/')
    df_2 = preprocess_data(['AAPL'], values='Adj Close',
                            relative_path='../data/')
    df_3 = preprocess_data(['AMD'], values='Adj Close',
                            relative_path='../data/')

    # test 1 - dataframes equal
    try:
        assert_frame_equal(df_1, df_2)
        test_status_list.append('Test 1 Passed.')
    except AssertionError:
        test_status_list.append('Test 1 Failed.')
    test_counter += 1

    # test 2 - dataframes not equal
    try:
        assert_frame_equal(df_1, df_3)
        test_status_list.append('Test 2 Failed.')
    except AssertionError:
        test_status_list.append('Test 2 Passed.')
    test_counter += 1

    # test 3 - ticker not in files
    try:
        assert (preprocess_data(['ABC'], values='Adj Close',
                                relative_path='../data/') == None)
        test_status_list.append('Test 3 Passed.')
    except AssertionError:
        test_status_list.append('Test 3 Failed.')
    test_counter += 1

    print(f"{test_counter}/{total_tests} Tests Passed.")
    if test_counter != total_tests:
        for test in test_status_list:
            print(test)


if __name__ == '__main__':
    pd.set_option('max_columns', 100)

    ## Research Setup - TODO: Change per hypothesis and datasets used
    freq_dict = {'D': ['Daily', 252], 'W': ['Weekly', 52], 'M': ['Monthly', 12],
                'Q': ['Quarterly', 4], 'A': ['Annually', 1]}

    dataset_base_freq = 'D'
    frequency = 'M'
    plot_ticker = 'AAPL'

    ticker_symbols = ['AAPL', 'AMD', 'AMZN', 'CSCO', 'FB', 'GOOG', 'IBM',
                    'INTC', 'NFLX', 'NVDA', 'ORCL', 'SNAP', 'SQ', 'TEAM',
                    'TSLA']

    base_freq = freq_dict[dataset_base_freq][0]
    plt_time_interval = freq_dict[frequency][0]
    ar_multiple = freq_dict[frequency][1]

    ## STEP 0: Import datasets from CSV files and aggregate into a dataframe
    prices = preprocess_data(ticker_symbols, values='Adj Close',
                            relative_path='../data/')

    start_date = prices.index.min()
    end_date = prices.index.max()

    ## STEP 1: visualize stock data
    plt.figure()
    plt.plot(prices[plot_ticker])
    plt.title(f"{plot_ticker} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.tight_layout()
    plt.show()

    ## STEP 2: resample data
    if frequency == dataset_base_freq:
        resamp_prices = prices
    else:
        resamp_prices = resample_prices(prices, frequency)

    plt.figure()
    plt.plot(prices[plot_ticker], color='blue', alpha=0.5, label='Close')
    plt.plot(resamp_prices[plot_ticker], color='navy', alpha=0.6,
                label=f'{plt_time_interval} Close')
    plt.title(f"{plot_ticker} Stock - Close Vs {plt_time_interval} Close")
    plt.xlabel("Date")
    plt.ylabel(f"Price ($)")
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

    ## STEP 3: generate log returns
    returns = compute_log_returns(resamp_prices)

    plt.figure()
    plt.plot(returns[plot_ticker])
    plt.hlines(y=0, xmin=returns.index.min(), xmax=returns.index.max(),
                color='black', linestyles='--', lw=1)
    plt.title(f"{plot_ticker} {plt_time_interval} Log Returns")
    plt.xlabel("Date")
    plt.ylabel(f"{plt_time_interval} Returns")
    plt.tight_layout()
    plt.show()

    ## STEP 4: view previous timestep and next timestep returns
    prev_returns = shift_returns(returns, 1)
    lookahead_returns = shift_returns(returns, -1)

    plt.figure()
    plt.plot(prev_returns.loc[:, plot_ticker], color='blue', alpha=0.5,
                label='Shifted Returns')
    plt.plot(returns.loc[:, plot_ticker], color='gray', alpha=0.5,
                label='Returns')
    plt.hlines(y=0, xmin=returns.index.min(), xmax=returns.index.max(),
                color='black', linestyles='--', lw=1)
    plt.title(f"Previous Returns of {plot_ticker} Stock")
    plt.xlabel("Date")
    plt.ylabel(f"{plt_time_interval} Returns")
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.plot(lookahead_returns.loc[:, plot_ticker], color='blue', alpha=0.5,
                label='Shifted Returns')
    plt.plot(returns.loc[:, plot_ticker], color='gray', alpha=0.5,
                label='Returns')
    plt.hlines(y=0, xmin=returns.index.min(), xmax=returns.index.max(),
                color='black', linestyles='--', lw=1)
    plt.title(f"Lookahead Returns of {plot_ticker} Stock")
    plt.xlabel("Date")
    plt.ylabel(f"{plt_time_interval} Returns")
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

    ## STEP 5: get the top n stocks and visualize
    top_bottom_n = 2
    df_long = get_top_n(prev_returns, top_bottom_n)
    df_short = get_top_n(-1*prev_returns, top_bottom_n)
    print('Longed Stocks\n', df_long)
    print('Shorted Stocks\n', df_short)

    ## STEP 6: get portfolio returns and visualize
    expected_portfolio_returns = portfolio_returns(df_long, df_short,
                                    lookahead_returns, 2*top_bottom_n)

    plt.figure()
    plt.plot(expected_portfolio_returns.T.sum())
    plt.hlines(y=0, xmin=returns.index.min(), xmax=returns.index.max(),
                color='black', linestyles='--', lw=1)
    plt.title(f"Expected Portfolio Returns")
    plt.xlabel("Date")
    plt.ylabel("Returns")
    plt.tight_layout()
    plt.show()

    ## STEP 7: annualized rate of return
    expected_portfolio_returns_by_date = expected_portfolio_returns.T.sum().dropna()
    portfolio_ret_mean = expected_portfolio_returns_by_date.mean()
    portfolio_ret_ste = expected_portfolio_returns_by_date.sem()
    portfolio_ret_annual_rate = (np.exp(portfolio_ret_mean * ar_multiple) - 1) * 100

    print(f"""
    Research Information:
        Dataset Start Date:             {start_date}
        Dataset End Date:               {end_date}
        Dataset Base Time Interval:     {base_freq}
        Resampled Time Interval:        {plt_time_interval}
        Asset Sample:
            {ticker_symbols}
    """)

    print(f"""
    Expected Portfolio Returns by Date:
        Mean:                       {portfolio_ret_mean:.6f}
        Standard Error:             {portfolio_ret_ste:.6f}
        Annualized Rate of Return:  {portfolio_ret_annual_rate:.2f}%
    """)

    # t-value and p-value for alpha
    t_value, p_value = analyze_alpha(expected_portfolio_returns_by_date)
    print(f"""
    Alpha analysis:
        t-value:        {t_value:.3f}
        p-value:        {p_value:.6f}
    """)
