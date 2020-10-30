import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pandas._testing import assert_frame_equal

def resample_prices(close_prices, freq='M'):
    """
    Resample close prices for each ticker at specified frequency.

    Parameters
    ----------
    close_prices : DataFrame
        Close prices for each ticker and date
    freq : str
        Frequency to sample at
        http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases

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

def get_top_n_better(prev_returns, top_n):
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
    return (prev_returns.rank(axis=1, ascending=False) <= top_n).astype(int)

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
    total_tests = 5
    df_1 = preprocess_data(['AAPL'], values='Adj Close', relative_path='../data/')
    df_2 = preprocess_data(['AAPL'], values='Adj Close', relative_path='../data/')
    df_3 = preprocess_data(['AMD'], values='Adj Close', relative_path='../data/')

    # test 1 - dataframes equal
    assert_frame_equal(df_1, df_2)
    test_counter += 1
    test_status_list.append('Test 1 Passed.')

    # test 2 - dataframes not equal
    try:
        assert_frame_equal(df_1, df_3)
        test_status_list.append('Test 2 Failed.')
    except AssertionError:
        test_counter += 1
        test_status_list.append('Test 2 Passed.')

    # test 3 - ticker not in files
    assert (preprocess_data(['ABC'], values='Adj Close',
                            relative_path='../data/') == None)
    # test 4 - relative path

    # test 5 - values column

    # print(f"{test_counter}/{total_tests} Tests Passed.")
    # if test_counter != total_tests:
    #     for test in test_status_list:
    #         print(test)
    pass


if __name__ == '__main__':
    pd.set_option('max_columns', 100)

    ticker_symbols = ['AAPL', 'AMD', 'AMZN', 'CSCO', 'FB', 'GOOG', 'IBM', 'INTC',
                         'NFLX', 'NVDA', 'ORCL', 'SNAP', 'SQ', 'TEAM', 'TSLA']

    prices = preprocess_data(ticker_symbols, values='Adj Close', relative_path='../data/')


    # ### TEST CODE ###
    # column_names = {'Date': 'date', 'Open': 'open', 'High': 'high',
    #                 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close',
    #                 'Volume': 'volume'}
    #
    # ticker_symbols = ['AAPL', 'AMD', 'AMZN', 'CSCO', 'FB', 'GOOG', 'IBM', 'INTC',
    #                     'NFLX', 'NVDA', 'ORCL', 'SNAP', 'SQ', 'TEAM', 'TSLA']
    #
    # df = pd.DataFrame([])
    #
    # for ticker in ticker_symbols:
    #     df_ticker = pd.read_csv(f"../data/{ticker}.csv", parse_dates=['Date'], index_col=False)
    #     df_ticker.rename(columns=column_names, inplace=True)
    #     df_ticker['ticker'] = ticker
    #     df = df.append(df_ticker, ignore_index=True)
    #
    # prices = df.reset_index().pivot(index='date', columns='ticker', values='adj_close')
    #
    # STEP 1: visualize stock data
    plt.figure()
    plot_ticker = 'AAPL'
    plt.plot(prices[plot_ticker])
    plt.title(f"{plot_ticker} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.tight_layout()
    plt.show()

    # STEP 2: resample data

    # STEP 3: generate log returns
    daily_close_returns = compute_log_returns(prices)

    plot_ticker = 'AAPL'
    plt_time_interval = "Daily"
    plt.figure()
    plt.plot(daily_close_returns[plot_ticker])
    plt.title(f"{plot_ticker} {plt_time_interval} Log Returns")
    plt.xlabel("Date")
    plt.ylabel(f"{plt_time_interval} Returns")
    plt.tight_layout()
    plt.show()

    # STEP 4: view previous month's and next month's returns
    prev_returns = shift_returns(daily_close_returns, 1)
    lookahead_returns = shift_returns(daily_close_returns, -1)

    plot_ticker = 'AAPL'
    plt_time_interval = "Daily"
    plt.figure()
    plt.plot(prev_returns.loc[:, plot_ticker], color='blue', alpha=0.5, label='previous')
    plt.plot(daily_close_returns.loc[:, plot_ticker], color='orange', alpha=0.5, label='actual')
    plt.title(f"Previous Returns of {plot_ticker} Stock")
    plt.xlabel("Date")
    plt.ylabel(f"{plt_time_interval} Returns")
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

    plot_ticker = 'AAPL'
    plt_time_interval = "Daily"
    plt.figure()
    plt.plot(lookahead_returns.loc[:, plot_ticker], color='black', alpha=0.5, label='lookahead')
    plt.plot(daily_close_returns.loc[:, plot_ticker], color='orange', alpha=0.5, label='actual')
    plt.title(f"Lookahead Returns of {plot_ticker} Stock")
    plt.xlabel("Date")
    plt.ylabel(f"{plt_time_interval} Returns")
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

    # STEP 5: get the top n stocks and visualize
    top_bottom_n = 2
    df_long = get_top_n(prev_returns, top_bottom_n)
    df_short = get_top_n(-1*prev_returns, top_bottom_n)
    # print('Longed Stocks', df_long)
    # print('Shorted Stocks', df_short)

    # STEP 6: get portfolio returns and visualize
    expected_portfolio_returns = portfolio_returns(df_long, df_short, lookahead_returns, 2*top_bottom_n)


    plt.figure()
    plt.plot(expected_portfolio_returns.T.sum())
    plt.title(f"Portfolio Returns")
    plt.xlabel("Date")
    plt.ylabel("Returns")
    plt.tight_layout()
    plt.show()

    # STEP 7: annualized rate of return
    expected_portfolio_returns_by_date = expected_portfolio_returns.T.sum().dropna()
    portfolio_ret_mean = expected_portfolio_returns_by_date.mean()
    portfolio_ret_ste = expected_portfolio_returns_by_date.sem()
    portfolio_ret_annual_rate = (np.exp(portfolio_ret_mean * 12) - 1) * 100

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

    ###########################################################################

    ### TEST CODE ###
    # # specify filename and location
    # filename = None
    #
    # # load the data
    # df = pd.read_csv(filename, parse_dates=['date'], index_col=False)
    #
    # # pivot the data
    # close = df.reset_index().pivot(index='date', columns='ticker', values='adj_close')
    #
    # # visualize stock
    # apple_ticker = 'AAPL'
    # project_helper.plot_stock(close[apple_ticker], '{} Stock'.format(apple_ticker))
    #
    # # resample the data and then visualize
    # monthly_close = resample_prices(close)
    # project_helper.plot_resampled_prices(
    #     monthly_close.loc[:, apple_ticker],
    #     close.loc[:, apple_ticker],
    #     '{} Stock - Close Vs Monthly Close'.format(apple_ticker))
    #
    # # generate log returns
    # monthly_close_returns = compute_log_returns(monthly_close)
    # project_helper.plot_returns(
    #     monthly_close_returns.loc[:, apple_ticker],
    #     'Log Returns of {} Stock (Monthly)'.format(apple_ticker))
    #
    # # view previous month's and next month's returns
    # prev_returns = shift_returns(monthly_close_returns, 1)
    # lookahead_returns = shift_returns(monthly_close_returns, -1)
    #
    # project_helper.plot_shifted_returns(
    #     prev_returns.loc[:, apple_ticker],
    #     monthly_close_returns.loc[:, apple_ticker],
    #     'Previous Returns of {} Stock'.format(apple_ticker))
    # project_helper.plot_shifted_returns(
    #     lookahead_returns.loc[:, apple_ticker],
    #     monthly_close_returns.loc[:, apple_ticker],
    #     'Lookahead Returns of {} Stock'.format(apple_ticker))

    # # view get top n data
    # top_bottom_n = 50
    # df_long = get_top_n(prev_returns, top_bottom_n)
    # df_short = get_top_n(-1*prev_returns, top_bottom_n)
    # project_helper.print_top(df_long, 'Longed Stocks')
    # project_helper.print_top(df_short, 'Shorted Stocks')

    # # view portfolio returns data
    # expected_portfolio_returns = portfolio_returns(df_long, df_short, lookahead_returns, 2*top_bottom_n)
    # project_helper.plot_returns(expected_portfolio_returns.T.sum(), 'Portfolio Returns')

    # # annualized rate of return
    # expected_portfolio_returns_by_date = expected_portfolio_returns.T.sum().dropna()
    # portfolio_ret_mean = expected_portfolio_returns_by_date.mean()
    # portfolio_ret_ste = expected_portfolio_returns_by_date.sem()
    # portfolio_ret_annual_rate = (np.exp(portfolio_ret_mean * 12) - 1) * 100
    #
    # print("""
    # Mean:                       {:.6f}
    # Standard Error:             {:.6f}
    # Annualized Rate of Return:  {:.2f}%
    # """.format(portfolio_ret_mean, portfolio_ret_ste, portfolio_ret_annual_rate))
    #
    # # Run the analyze alpha function to get a t-value and p-value
    # t_value, p_value = analyze_alpha(expected_portfolio_returns_by_date)
    # print("""
    # Alpha analysis:
    #  t-value:        {:.3f}
    #  p-value:        {:.6f}
    # """.format(t_value, p_value))

    '''
    Answer the Questions:

    What p-value did you observe?
    What does that indicate about your signal?

    p-value: 0.073359

    This indicates that although the signal is not statistically significant at
    the 0.05 level, it is statistically significant at the 0.1 level. This
    means that this signal has the potential to generate returns greater than
    the mean return of the market.

    '''
