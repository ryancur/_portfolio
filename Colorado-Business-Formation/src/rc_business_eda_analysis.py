'''
Author: Ryan Curry
Project: Go Code Colorado
'''

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import datetime as dt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression


def basic_eda(dataframe):
    """Takes a pandas dataframe as input and prints descriptive stats"""
    print("HEAD:\n", dataframe.head())
    print("TAIL:\n", dataframe.tail())
    print("SAMPLE:\n", dataframe.sample(10))
    print("SHAPE:\n", dataframe.shape)
    print("DTYPES:\n", dataframe.dtypes)
    print("INFO:\n", dataframe.info())
    print("DESCRIBE:\n", dataframe.describe())
    print("NULL VALUES:\n", dataframe.isnull().sum())

def missing_info_plot(dataframe):
    """Plots a missingno plot of a dataframe and saves it to a png file"""
    msno.matrix(dataframe)
    plt.savefig('../images/eda_missing_info.png')
    plt.show()

def filter(dataframe, column_name, row_value):
    '''
    Returns a new dataframe filtered by a single column name and single row value.

    Parameters:
    dataframe (dataframe): pandas dataframe
    column_name (string): name of column containing row value
    row_value: the desired row value to filter by

    Returns:
    dataframe: pandas dataframe filtered by specified column
    '''
    new_df = dataframe.loc[dataframe[column_name] == row_value]
    return new_df

def counts(dataframe, group_col, count_col, sort_col):
    '''
    Returns a sorted dataframe with counts of values within a column.

    Parameters:
    dataframe (dataframe): pandas dataframe
    group_col (string): name of column to group by
    count_col (string): column to count by
    sort_col (string): column to sort by

    Returns:
    dataframe: sorted pandas dataframe by count
    '''
    group = dataframe.groupby(group_col)[[count_col]].count()
    sorted_group = group.sort_values(sort_col, ascending=False).reset_index()
    sorted_group.columns=[group_col, 'total']
    return sorted_group

def extract_year(dataframe, new_col_name, datetime_col):
    '''
    Creates a new column with the year extracted from a datetime column

    Parameters:
    dataframe (dataframe): pandas dataframe
    new_col_name (string): name of the new column to be created
    datetime_col (string): name of datetime column

    Returns:
    existing dataframe with an added column containing the year
    '''
    dataframe[new_col_name] = dataframe[datetime_col].map(lambda x: x.year)
    return dataframe

def extract_year_month(dataframe, new_col_name, datetime_col):
    '''
    Creates a new column with the year and month extracted from a datetime column

    Parameters:
    dataframe (dataframe): pandas dataframe
    new_col_name (string): name of the new column to be created
    datetime_col (string): name of datetime column

    Returns:
    existing dataframe with an added column containing the year and month
    '''
    dataframe[new_col_name] = dataframe[datetime_col].dt.to_period('M')
    return dataframe

def percentage(dataframe, numerator, denominator, new_col_name, decimal_places=2):
    '''
    Creates a new column with percentage of total based on the count of another column

    Parameters:
    dataframe (series/dataframe): pandas series or dataframe
    numerator (string): pandas series containing the values for the numerator
    denominator (float/int): a number to divide each numerator by
    new_col_name (string): name of the new column (i.e. percent_total)
    decimal_places (int): the number of decimal places (default = 2)

    Returns:
    dataframe with a new percentage column added to the end
    '''
    dataframe[new_col_name] = (dataframe[numerator] / denominator)*100
    dataframe[new_col_name] = np.round(dataframe[new_col_name], decimals=decimal_places)
    return dataframe

def per_x_residents(dataframe, new_col_name, numerator, denominator, num_residents=1000, decimal_places=2):
    '''
    Creates a new column with a number of items per a specified number of residents

    Parameters:
    dataframe (dataframe): pandas dataframe
    new_col_name (string): name of new column
    numerator (string): pandas series containing the values for the numerator (values must be float or int)
    denominator (string): pandas series containing the values for the denominator (values must be float or int)
    num_residents (int): the number of residents you would like to account for (default = 1000)

    Returns:
    dataframe with a new column with the number of items per the number of residents
    '''
    dataframe[new_col_name] = dataframe[numerator] / (dataframe[denominator]/num_residents)
    dataframe[new_col_name] = np.round(dataframe[new_col_name], decimals=decimal_places)
    return dataframe

def linear_regression(dataframe, X, y, title, xlabel, ylabel, y_min=False, y_max=False):
    '''
    Runs a linear regression and then plots it.

    Parameters:
    dataframe (dataframe): pandas dataframe
    X (string): name of the column with the X values
    y (string): name of the column with the y values
    title (string): title of the plot
    xlabel (string): label of the X axis
    ylabel (string): label of the y axis

    Returns:
    saves a png file to the images folder (make sure there is an images folder)
    displays a scatter plot of the data with the linear regression line
    '''
    X = dataframe[[X]]
    y = dataframe[[y]]
    lr = LinearRegression()
    lr.fit(X, y)
    y_predict = lr.predict(X)
    r_squared = lr.score(X, y)
    print("R-squared: ", r_squared)
    new_title = title.replace(' ', '')
    plt.scatter(X, y, alpha=0.4)
    plt.plot(X, y_predict)
    if y_max:
        plt.ylim(y_min, y_max)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    try:
        plt.savefig('../images/{}.png'.format(new_title))
    except:
        print("Pathway does not exist")
    plt.show()

def simple_line_plot(dataframe, x_col, y_col, x_label, y_label, title, label_vert=False, color='blue', y_min=False, y_max=False):
    '''
    Creates a simple line plot and saves as png file to images folder

    Parameters:
    dataframe (dataframe): pandas dataframe
    x_col (string): name of dataframe column with x values
    y_col (string): name of dataframe column with y values
    x_label (string): name of x axis label
    y_label (string): name of y axis label
    title (string): title of chart
    color (string): color of the line (default = blue)
    label_vert (string): default False - put 'vertical' if rotation desired

    Returns:
    saves a png file to the images folder (make sure there is an images folder)
    displays the line plot
    '''
    x = dataframe[x_col]
    y = dataframe[y_col]
    labels = dataframe[x_col].unique()
    new_title = title.replace(' ', '')
    plt.plot(x, y, color=color, marker='o', linewidth=2, markersize=8, alpha=0.5)
    if y_max:
        plt.ylim(y_min, y_max)
    plt.xticks(x, labels, rotation=label_vert)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    try:
        plt.savefig('../images/{}.png'.format(new_title))
    except:
        print("Pathway does not exist")
    plt.show()

def bar_chart(dataframe, x_col, y_col, x_label, y_label, title, label_vert=False, y_min=False, y_max=False):
    '''
    Creates a bar chart and saves as png file to images folder

    Parameters:
    dataframe (dataframe): pandas dataframe
    x_col (string): name of dataframe column with x values
    y_col (string): name of dataframe column with y values
    x_label (string): name of x axis label
    y_label (string): name of y axis label
    title (string): title of chart
    label_vert (string): default False - put 'vertical' if rotation desired

    Returns:
    saves a png file to the images folder (make sure there is an images folder)
    displays the bar chart
    '''
    x = dataframe[x_col]
    y = dataframe[y_col]
    labels = dataframe[x_col].unique()
    new_title = title.replace(' ', '')
    plt.bar(x, y, align='center', alpha=0.5)
    if y_max:
        plt.ylim(y_min, y_max)
    plt.xticks(x, labels, rotation=label_vert)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    try:
        plt.savefig('../images/{}.png'.format(new_title))
    except:
        print("Pathway does not exist")
    plt.show()

def pie_chart(data, labels, title, explode=None):
    '''
    Creates a pie chart and saves as png file to images folder

    Parameters:
    data (array): array of values for slice sizes
    labels (list): list of labels for each piece of the pie
    explode (array): tuple of numbers specifying which slice to break away from pie
    title (string): title of the pie chart

    Returns:
    saves a png file to the images folder (make sure there is an images folder)
    displays a pie chart
    '''
    new_title = title.replace(' ', '')
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, explode=explode, autopct='%1.1f%%', shadow=False, startangle=90)
    ax.set_title(title)
    ax.axis('equal')
    try:
        plt.savefig('../images/{}.png'.format(new_title))
    except:
        print("Pathway does not exist")
    plt.show()

def plot_timeseries_decompose(title, time_series, trend, seasonal, residual, file_name):
    '''
    Creates a plot showing a time series decomposition analysis including trend,
    seasonal, and residual information

    Parameters:
    title (string): title of the plot
    time_series (pandas series): series needs to have datetime index and one column of data
    trend (pandas series): trend data from seasonal_decompose.trend
    seasonal (pandas series): seasonal data from seasonal_decompose.seasonal
    residual (pandas series): residual data from seasonal_decompose.resid
    file_name (string): name of the image for saving

    Returns:
    saves a png file with image of the plot to the images folder
    '''
    plt.subplot(411)
    plt.title(title)
    plt.plot(time_series, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()
    try:
        plt.savefig('../images/{}.png'.format(file_name))
    except:
        print("Pathway does not exist")
    plt.show()

if __name__ == '__main__':

    pd.set_option('display.max_columns', 100)
    df_business_all = pd.read_csv('../data/clean/co_business_all.csv')
    df_business_metro = pd.read_csv('../data/clean/co_cities_all.csv')
    df_population = pd.read_csv('../data/raw/county-componentsChange_data.csv', sep='\t')
    gdp_pc_col_springs = pd.read_csv('../data/raw/RPCGDP_Colorado-Springs-CO.csv')
    gdp_pc_boulder = pd.read_csv('../data/raw/RPCGDP_Boulder-CO.csv')
    gdp_pc_denver = pd.read_csv('../data/raw/RPCGDP_Denver-Aurora-Lakewood-CO.csv')
    gdp_pc_fort_col = pd.read_csv('../data/raw/RPCGDP_Fort-Collins-CO.csv')
    gdp_pc_grand_junc = pd.read_csv('../data/raw/RPCGDP_Grand-Junction-CO.csv')
    gdp_pc_greeley = pd.read_csv('../data/raw/RPCGDP_Greeley-CO.csv')
    gdp_pc_pueblo = pd.read_csv('../data/raw/RPCGDP_Pueblo-CO.csv')
    colorado_gdp = pd.read_csv('../data/raw/co_gdp.csv', header=None).transpose()
    co_gdp_per_capita = pd.read_csv('../data/raw/co_real_per_capita_gdp.csv', header=None).transpose()

    #perform basic eda on the dataframe
    #basic_eda(df_business)


    '''Clean and prep the data'''
    #create a copy of the dataframe to work on
    df_bus_all = df_business_all.copy()
    df_bus_metro = df_business_metro.copy()
    df_pop = df_population.copy()

    #drop columns
    df_pop = df_pop[['YEAR', 'Population']]

    #rename columns
    df_pop.columns = ['year', 'population']
    colorado_gdp.columns = ['year', 'gdp_millions']
    co_gdp_per_capita.columns = ['year', 'gdp_per_capita']

    #remove characters
    df_pop['population'] = df_pop['population'].str.replace(',', '')

    #change data types
    colorado_gdp['year'] = colorado_gdp['year'].astype(int)
    df_pop['population'] = df_pop['population'].astype(int)

    #change entity formation date column to datetime format
    df_bus_all['entityformdate'] = pd.to_datetime(df_bus_all['entityformdate'])
    df_bus_metro['entityformdate'] = pd.to_datetime(df_bus_metro['entityformdate'])

    #add a year column to the dataframe
    df_bus_all = extract_year(df_bus_all, 'year', 'entityformdate')
    df_bus_metro = extract_year(df_bus_metro, 'year', 'entityformdate')

    #add a year-month column to the dataframe
    df_bus_all = extract_year_month(df_bus_all, 'month', 'entityformdate')
    df_bus_metro = extract_year_month(df_bus_metro, 'month', 'entityformdate')

    #add population per year
    df_bus_all = pd.merge(df_bus_all, df_pop, on='year')

    #add gdp per year
    df_bus_all = pd.merge(df_bus_all, colorado_gdp, on='year')
    df_bus_all = pd.merge(df_bus_all, co_gdp_per_capita, on='year')


    '''State Data Summary Analysis 2001-2017'''

    total_num_business = df_bus_all['entityid'].count()
    print('Total Number of Businesses Formed: ', total_num_business)

    status_breakdown = counts(df_bus_all, 'entitystatus', 'entityid', 'entityid')
    status_breakdown = percentage(status_breakdown, 'total', total_num_business, 'percent_total', 2)
    print('Status of Businesses Formed: \n ', status_breakdown)
    pie_chart(status_breakdown['percent_total'][0:4], status_breakdown['entitystatus'][0:4], 'Top 4 Entity Status of All Businesses Formed 2001-2017')

    count_per_year = counts(df_bus_all, 'year', 'entityid', 'year')
    count_per_year = percentage(count_per_year, 'total', total_num_business, 'percent_total', 2)
    count_per_year = pd.merge(count_per_year, df_pop, on='year', how='left')
    count_per_year = per_x_residents(count_per_year, 'bus_formed_per_1000_residents', 'total', 'population', 1000, 2)
    print('Number of Businesses Formed Per Year: \n ', count_per_year)
    simple_line_plot(count_per_year, 'year', 'bus_formed_per_1000_residents', 'Year', 'Number of Businesses (per 1000 residents)', 'Businesses Formed Per 1000 Residents in Colorado 2001-2017', label_vert='vertical')
    simple_line_plot(count_per_year, 'year', 'population', 'Year', 'Population', 'Population Per Year in Colorado 2001-2017 Zoomed', label_vert='vertical')
    simple_line_plot(count_per_year, 'year', 'population', 'Year', 'Population', 'Population Per Year in Colorado 2001-2017', label_vert='vertical', y_min=0, y_max=6000000)
    simple_line_plot(count_per_year, 'year', 'total', 'Year', 'Number of Businesses Formed', 'Number of Businesses Formed Per Year in Colorado 2001-2017', label_vert='vertical', y_min=0, y_max=110000)

    count_entity_type = counts(df_bus_all, 'entitytype', 'entityid', 'entityid')
    count_entity_type = percentage(count_entity_type, 'total', total_num_business, 'percent_total', 2)
    print('Number of Businesses Formed by Type: \n ', count_entity_type)
    pie_chart(count_entity_type['percent_total'][0:3], count_entity_type['entitytype'][0:3], 'Top 3 Entity Types of All Businesses Formed 2001-2017')

    df_co_gdp = count_per_year.copy()
    df_co_gdp = pd.merge(df_co_gdp, colorado_gdp, on='year', how='left')
    df_co_gdp = pd.merge(df_co_gdp, co_gdp_per_capita, on='year', how='left')
    df_co_gdp = df_co_gdp[['year', 'population', 'gdp_millions', 'gdp_per_capita']]
    df_co_gdp.columns = ['year', 'population', 'gdp_millions', 'real_gdp_per_capita']


    '''State Data Analysis'''

    # number of businesses formed per year - linear regression
    linear_regression(count_per_year, 'year', 'total', 'State Number of Businesses Formed Per Year', 'Year', 'Number of Businesses', y_min=0, y_max=110000)
    linear_regression(count_per_year, 'year', 'population', 'State Population Per Year', 'Year', 'Population', y_min=4000000, y_max=6000000)
    linear_regression(count_per_year, 'year', 'bus_formed_per_1000_residents', 'State Businesses Formed Per 1000 Residents', 'Year', 'Number of Businesses Per 1000 Residents')

    #state gdp
    simple_line_plot(df_co_gdp, 'year', 'gdp_millions', 'Year', 'State GDP (millions)', 'State GDP 2001-2017 in Current Dollars', label_vert='vertical', y_min=100000, y_max=400000)
    linear_regression(df_co_gdp, 'year', 'gdp_millions', 'State GDP 2001-2017 Linear Regression in Current Dollars', 'Year', 'State GDP (millions)', y_min=100000, y_max=400000)

    # real gdp per capita
    #linear_regression(df_co_gdp, 'year', 'real_gdp_per_capita', 'State Real GDP Per Capita 2001-2017 Zoomed', 'Year', 'Real GDP Per Capita (chained 2012 dollars)')
    linear_regression(df_co_gdp, 'year', 'real_gdp_per_capita', 'State Real GDP Per Capita 2001-2017 Linear Regression', 'Year', 'Real GDP Per Capita (chained 2012 dollars)', y_min=20000, y_max=72000)
    simple_line_plot(df_co_gdp, 'year', 'real_gdp_per_capita', 'Year', 'Real GDP Per Capita (chained 2012 dollars)', 'State Real GDP Per Capita 2001-2017', label_vert='vertical', y_min=20000, y_max=72000)


    '''Create new dataframes for each metro area'''

    df_denver = filter(df_bus_metro, 'metro_area', 'Denver')
    df_col_springs = filter(df_bus_metro, 'metro_area', 'Colorado Springs')
    df_greeley = filter(df_bus_metro, 'metro_area', 'Greeley')
    df_pueblo = filter(df_bus_metro, 'metro_area', 'Pueblo')
    df_fort_col = filter(df_bus_metro, 'metro_area', 'Fort Collins')
    df_boulder = filter(df_bus_metro, 'metro_area', 'Boulder')
    df_grand_junc = filter(df_bus_metro, 'metro_area', 'Grand Junction')

    '''Denver Metro Area'''

    #prep gdp data
    gdp_pc_denver['DATE'] = pd.to_datetime(gdp_pc_denver['DATE'])
    denver_gdp_pc = extract_year(gdp_pc_denver, 'year', 'DATE')

    #drop columns
    denver_gdp_pc.drop(['DATE'], inplace=True, axis=1)

    #clean column names
    denver_gdp_pc.columns = ['real_per_capita_gdp', 'year']

    total_bus_denver = df_denver['entityid'].count()
    print('Total Number of Businesses Formed in Denver: ', total_bus_denver)

    status_denver = counts(df_denver, 'entitystatus', 'entityid', 'entityid')
    status_denver = percentage(status_denver, 'total', total_bus_denver, 'percent_total', 2)
    print('Status of Businesses Formed in Denver: \n ', status_denver)
    pie_chart(status_denver['percent_total'][0:4], status_denver['entitystatus'][0:4], 'Top 4 Entity Status of Denver Businesses Formed 2001-2017')

    count_denver = counts(df_denver, 'year', 'entityid', 'year')
    count_denver = percentage(count_denver, 'total', total_bus_denver, 'percent_total', 2)
    print('Number of Businesses Formed Per Year in Denver: \n ', count_denver)
    simple_line_plot(count_denver, 'year', 'total', 'Year', 'Number of Businesses Formed', 'Number of Businesses Formed Per Year in Denver 2001-2017', label_vert='vertical', y_min=0, y_max=60000)

    entity_type_denver = counts(df_denver, 'entitytype', 'entityid', 'entityid')
    entity_type_denver = percentage(entity_type_denver, 'total', total_bus_denver, 'percent_total', 2)
    print('Number of Businesses Formed by Type in Denver: \n ', entity_type_denver)
    pie_chart(entity_type_denver['percent_total'][0:3], entity_type_denver['entitytype'][0:3], 'Top 3 Entity Types of Denver Businesses Formed 2001-2017')

    df_gdp_denver = count_denver.copy()
    df_gdp_denver = pd.merge(df_gdp_denver, denver_gdp_pc, on='year', how='left')

    # number of businesses formed per year - linear regression
    linear_regression(count_denver, 'year', 'total', 'Denver Number of Businesses Formed Per Year', 'Year', 'Number of Businesses', y_min=0, y_max=60000)

    # real gdp per capita
    linear_regression(df_gdp_denver, 'year', 'real_per_capita_gdp', 'Denver Real GDP Per Capita 2001-2017', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', y_min=0, y_max=72000)
    simple_line_plot(df_gdp_denver, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Denver Real GDP Per Capita 2001-2017', label_vert='vertical', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_denver, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Denver Real GDP Per Capita 2001-2017 Zoomed', label_vert='vertical')


    '''Colorado Springs Metro Area'''

    #prep gdp data
    gdp_pc_col_springs['DATE'] = pd.to_datetime(gdp_pc_col_springs['DATE'])
    col_springs_gdp_pc = extract_year(gdp_pc_col_springs, 'year', 'DATE')

    #drop columns
    col_springs_gdp_pc.drop(['DATE'], inplace=True, axis=1)

    #clean column names
    col_springs_gdp_pc.columns = ['real_per_capita_gdp', 'year']

    total_bus_col_springs = df_col_springs['entityid'].count()
    print('Total Number of Businesses Formed in Colorado Springs: ', total_bus_col_springs)

    status_col_springs = counts(df_col_springs, 'entitystatus', 'entityid', 'entityid')
    status_col_springs = percentage(status_col_springs, 'total', total_bus_col_springs, 'percent_total', 2)
    print('Status of Businesses Formed in Colorado Springs: \n ', status_col_springs)
    pie_chart(status_col_springs['percent_total'][0:4], status_col_springs['entitystatus'][0:4], 'Top 4 Entity Status of Colorado Springs Businesses Formed 2001-2017')

    count_col_springs = counts(df_col_springs, 'year', 'entityid', 'year')
    count_col_springs = percentage(count_col_springs, 'total', total_bus_col_springs, 'percent_total', 2)
    print('Number of Businesses Formed Per Year in Colorado Springs: \n ', count_col_springs)
    simple_line_plot(count_col_springs, 'year', 'total', 'Year', 'Number of Businesses Formed', 'Number of Businesses Formed Per Year in Colorado Springs 2001-2017', label_vert='vertical', y_min=0, y_max=15000)

    entity_type_col_springs = counts(df_col_springs, 'entitytype', 'entityid', 'entityid')
    entity_type_col_springs = percentage(entity_type_col_springs, 'total', total_bus_col_springs, 'percent_total', 2)
    print('Number of Businesses Formed by Type in Colorado Springs: \n ', entity_type_col_springs)
    pie_chart(entity_type_col_springs['percent_total'][0:3], entity_type_col_springs['entitytype'][0:3], 'Top 3 Entity Types of Colorado Springs Businesses Formed 2001-2017')

    df_gdp_col_springs = count_col_springs.copy()
    df_gdp_col_springs = pd.merge(df_gdp_col_springs, col_springs_gdp_pc, on='year', how='left')

    # number of businesses formed per year - linear regression
    linear_regression(count_col_springs, 'year', 'total', 'Colorado Springs Number of Businesses Formed Per Year', 'Year', 'Number of Businesses', y_min=0, y_max=15000)

    # real gdp per capita
    linear_regression(df_gdp_col_springs, 'year', 'real_per_capita_gdp', 'Colorado Springs Real GDP Per Capita 2001-2017', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', y_min=0, y_max=72000)
    simple_line_plot(df_gdp_col_springs, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Colorado Springs Real GDP Per Capita 2001-2017', label_vert='vertical', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_col_springs, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Colorado Springs Real GDP Per Capita 2001-2017 Zoomed', label_vert='vertical')


    '''Greeley Metro Area'''

    #prep gdp data
    gdp_pc_greeley['DATE'] = pd.to_datetime(gdp_pc_greeley['DATE'])
    greeley_gdp_pc = extract_year(gdp_pc_greeley, 'year', 'DATE')

    #drop columns
    greeley_gdp_pc.drop(['DATE'], inplace=True, axis=1)

    #clean column names
    greeley_gdp_pc.columns = ['real_per_capita_gdp', 'year']

    total_bus_greeley = df_greeley['entityid'].count()
    print('Total Number of Businesses Formed in Greeley: ', total_bus_greeley)

    status_greeley = counts(df_greeley, 'entitystatus', 'entityid', 'entityid')
    status_greeley = percentage(status_greeley, 'total', total_bus_greeley, 'percent_total', 2)
    print('Status of Businesses Formed in Greeley: \n ', status_greeley)
    pie_chart(status_greeley['percent_total'][0:4], status_greeley['entitystatus'][0:4], 'Top 4 Entity Status of Greeley Businesses Formed 2001-2017')

    count_greeley = counts(df_greeley, 'year', 'entityid', 'year')
    count_greeley = percentage(count_greeley, 'total', total_bus_greeley, 'percent_total', 2)
    print('Number of Businesses Formed Per Year in Greeley: \n ', count_greeley)
    simple_line_plot(count_greeley, 'year', 'total', 'Year', 'Number of Businesses Formed', 'Number of Businesses Formed Per Year in Greeley 2001-2017', label_vert='vertical', y_min=0, y_max=5000)

    entity_type_greeley = counts(df_greeley, 'entitytype', 'entityid', 'entityid')
    entity_type_greeley = percentage(entity_type_greeley, 'total', total_bus_greeley, 'percent_total', 2)
    print('Number of Businesses Formed by Type in Greeley: \n ', entity_type_greeley)
    pie_chart(entity_type_greeley['percent_total'][0:3], entity_type_greeley['entitytype'][0:3], 'Top 3 Entity Types of Greeley Businesses Formed 2001-2017')

    df_gdp_greeley = count_greeley.copy()
    df_gdp_greeley = pd.merge(df_gdp_greeley, greeley_gdp_pc, on='year', how='left')

    # number of businesses formed per year - linear regression
    linear_regression(count_greeley, 'year', 'total', 'Greeley Number of Businesses Formed Per Year', 'Year', 'Number of Businesses', y_min=0, y_max=5000)

    # real gdp per capita
    linear_regression(df_gdp_greeley, 'year', 'real_per_capita_gdp', 'Greeley Real GDP Per Capita 2001-2017', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_greeley, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Greeley Real GDP Per Capita 2001-2017', label_vert='vertical', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_greeley, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Greeley Real GDP Per Capita 2001-2017 Zoomed', label_vert='vertical')


    '''Pueblo Metro Area'''

    #prep gdp data
    gdp_pc_pueblo['DATE'] = pd.to_datetime(gdp_pc_pueblo['DATE'])
    pueblo_gdp_pc = extract_year(gdp_pc_pueblo, 'year', 'DATE')

    #drop columns
    pueblo_gdp_pc.drop(['DATE'], inplace=True, axis=1)

    #clean column names
    pueblo_gdp_pc.columns = ['real_per_capita_gdp', 'year']

    total_bus_pueblo = df_pueblo['entityid'].count()
    print('Total Number of Businesses Formed in Pueblo: ', total_bus_pueblo)

    status_pueblo = counts(df_pueblo, 'entitystatus', 'entityid', 'entityid')
    status_pueblo = percentage(status_pueblo, 'total', total_bus_pueblo, 'percent_total', 2)
    print('Status of Businesses Formed in Pueblo: \n ', status_pueblo)
    pie_chart(status_pueblo['percent_total'][0:4], status_pueblo['entitystatus'][0:4], 'Top 4 Entity Status of Pueblo Businesses Formed 2001-2017')

    count_pueblo = counts(df_pueblo, 'year', 'entityid', 'year')
    count_pueblo = percentage(count_pueblo, 'total', total_bus_pueblo, 'percent_total', 2)
    print('Number of Businesses Formed Per Year in Pueblo: \n ', count_pueblo)
    simple_line_plot(count_pueblo, 'year', 'total', 'Year', 'Number of Businesses Formed', 'Number of Businesses Formed Per Year in Pueblo 2001-2017', label_vert='vertical', y_min=0, y_max=2000)

    entity_type_pueblo = counts(df_pueblo, 'entitytype', 'entityid', 'entityid')
    entity_type_pueblo = percentage(entity_type_pueblo, 'total', total_bus_pueblo, 'percent_total', 2)
    print('Number of Businesses Formed by Type in Pueblo: \n ', entity_type_pueblo)
    pie_chart(entity_type_pueblo['percent_total'][0:3], entity_type_pueblo['entitytype'][0:3], 'Top 3 Entity Types of Pueblo Businesses Formed 2001-2017')

    df_gdp_pueblo = count_pueblo.copy()
    df_gdp_pueblo = pd.merge(df_gdp_pueblo, pueblo_gdp_pc, on='year', how='left')

    # number of businesses formed per year - linear regression
    linear_regression(count_pueblo, 'year', 'total', 'Pueblo Number of Businesses Formed Per Year', 'Year', 'Number of Businesses', y_min=0, y_max=2000)

    # real gdp per capita
    linear_regression(df_gdp_pueblo, 'year', 'real_per_capita_gdp', 'Pueblo Real GDP Per Capita 2001-2017', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_pueblo, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Pueblo Real GDP Per Capita 2001-2017', label_vert='vertical', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_pueblo, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Pueblo Real GDP Per Capita 2001-2017 Zoomed', label_vert='vertical')


    '''Fort Collins Metro Area'''

    #prep gdp data
    gdp_pc_fort_col['DATE'] = pd.to_datetime(gdp_pc_fort_col['DATE'])
    fort_col_gdp_pc = extract_year(gdp_pc_fort_col, 'year', 'DATE')

    #drop columns
    fort_col_gdp_pc.drop(['DATE'], inplace=True, axis=1)

    #clean column names
    fort_col_gdp_pc.columns = ['real_per_capita_gdp', 'year']

    total_bus_fort_col = df_fort_col['entityid'].count()
    print('Total Number of Businesses Formed in Fort Collins: ', total_bus_fort_col)

    status_fort_col = counts(df_fort_col, 'entitystatus', 'entityid', 'entityid')
    status_fort_col = percentage(status_fort_col, 'total', total_bus_fort_col, 'percent_total', 2)
    print('Status of Businesses Formed in Fort Collins: \n ', status_fort_col)
    pie_chart(status_fort_col['percent_total'][0:4], status_fort_col['entitystatus'][0:4], 'Top 4 Entity Status of Fort Collins Businesses Formed 2001-2017')

    count_fort_col = counts(df_fort_col, 'year', 'entityid', 'year')
    count_fort_col = percentage(count_fort_col, 'total', total_bus_fort_col, 'percent_total', 2)
    print('Number of Businesses Formed Per Year in Fort Collins: \n ', count_fort_col)
    simple_line_plot(count_fort_col, 'year', 'total', 'Year', 'Number of Businesses Formed', 'Number of Businesses Formed Per Year in Fort Collins 2001-2017', label_vert='vertical', y_min=0, y_max=6000)

    entity_type_fort_col = counts(df_fort_col, 'entitytype', 'entityid', 'entityid')
    entity_type_fort_col = percentage(entity_type_fort_col, 'total', total_bus_fort_col, 'percent_total', 2)
    print('Number of Businesses Formed by Type in Fort Collins: \n ', entity_type_fort_col)
    pie_chart(entity_type_fort_col['percent_total'][0:3], entity_type_fort_col['entitytype'][0:3], 'Top 3 Entity Types of Fort Collins Businesses Formed 2001-2017')

    df_gdp_fort_col = count_fort_col.copy()
    df_gdp_fort_col = pd.merge(df_gdp_fort_col, fort_col_gdp_pc, on='year', how='left')

    # number of businesses formed per year - linear regression
    linear_regression(count_fort_col, 'year', 'total', 'Fort Collins Number of Businesses Formed Per Year', 'Year', 'Number of Businesses', y_min=0, y_max=6000)

    # real gdp per capita
    linear_regression(df_gdp_fort_col, 'year', 'real_per_capita_gdp', 'Fort Collins Real GDP Per Capita 2001-2017', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_fort_col, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Fort Collins Real GDP Per Capita 2001-2017', label_vert='vertical', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_fort_col, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Fort Collins Real GDP Per Capita 2001-2017 Zoomed', label_vert='vertical')


    '''Boulder Metro Area'''

    #prep gdp data
    gdp_pc_boulder['DATE'] = pd.to_datetime(gdp_pc_boulder['DATE'])
    boulder_gdp_pc = extract_year(gdp_pc_boulder, 'year', 'DATE')

    #drop columns
    boulder_gdp_pc.drop(['DATE'], inplace=True, axis=1)

    #clean column names
    boulder_gdp_pc.columns = ['real_per_capita_gdp', 'year']

    total_bus_boulder = df_boulder['entityid'].count()
    print('Total Number of Businesses Formed in Boulder: ', total_bus_boulder)

    status_boulder = counts(df_boulder, 'entitystatus', 'entityid', 'entityid')
    status_boulder = percentage(status_boulder, 'total', total_bus_boulder, 'percent_total', 2)
    print('Status of Businesses Formed in Boulder: \n ', status_boulder)
    pie_chart(status_boulder['percent_total'][0:4], status_boulder['entitystatus'][0:4], 'Top 4 Entity Status of Boulder Businesses Formed 2001-2017')

    count_boulder = counts(df_boulder, 'year', 'entityid', 'year')
    count_boulder = percentage(count_boulder, 'total', total_bus_boulder, 'percent_total', 2)
    print('Number of Businesses Formed Per Year in Boulder: \n ', count_boulder)
    simple_line_plot(count_boulder, 'year', 'total', 'Year', 'Number of Businesses Formed', 'Number of Businesses Formed Per Year in Boulder 2001-2017', label_vert='vertical', y_min=0, y_max=8000)

    entity_type_boulder = counts(df_boulder, 'entitytype', 'entityid', 'entityid')
    entity_type_boulder = percentage(entity_type_boulder, 'total', total_bus_boulder, 'percent_total', 2)
    print('Number of Businesses Formed by Type in Boulder: \n ', entity_type_boulder)
    pie_chart(entity_type_boulder['percent_total'][0:3], entity_type_boulder['entitytype'][0:3], 'Top 3 Entity Types of Boulder Businesses Formed 2001-2017')

    df_gdp_boulder = count_boulder.copy()
    df_gdp_boulder = pd.merge(df_gdp_boulder, boulder_gdp_pc, on='year', how='left')

    # number of businesses formed per year - linear regression
    linear_regression(count_boulder, 'year', 'total', 'Boulder Number of Businesses Formed Per Year', 'Year', 'Number of Businesses', y_min=0, y_max=8000)

    # real gdp per capita
    linear_regression(df_gdp_boulder, 'year', 'real_per_capita_gdp', 'Boulder Real GDP Per Capita 2001-2017', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_boulder, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Boulder Real GDP Per Capita 2001-2017', label_vert='vertical', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_boulder, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Boulder Real GDP Per Capita 2001-2017 Zoomed', label_vert='vertical')

    '''Grand Junction Metro Area'''

    #prep gdp data
    gdp_pc_grand_junc['DATE'] = pd.to_datetime(gdp_pc_grand_junc['DATE'])
    grand_junc_gdp_pc = extract_year(gdp_pc_grand_junc, 'year', 'DATE')

    #drop columns
    grand_junc_gdp_pc.drop(['DATE'], inplace=True, axis=1)

    #clean column names
    grand_junc_gdp_pc.columns = ['real_per_capita_gdp', 'year']

    total_bus_grand_junc = df_grand_junc['entityid'].count()
    print('Total Number of Businesses Formed in Grand Junction: ', total_bus_grand_junc)

    status_grand_junc = counts(df_grand_junc, 'entitystatus', 'entityid', 'entityid')
    status_grand_junc = percentage(status_grand_junc, 'total', total_bus_grand_junc, 'percent_total', 2)
    print('Status of Businesses Formed in Grand Junction: \n ', status_grand_junc)
    pie_chart(status_grand_junc['percent_total'][0:4], status_grand_junc['entitystatus'][0:4], 'Top 4 Entity Status of Grand Junction Businesses Formed 2001-2017')

    count_grand_junc = counts(df_grand_junc, 'year', 'entityid', 'year')
    count_grand_junc = percentage(count_grand_junc, 'total', total_bus_grand_junc, 'percent_total', 2)
    print('Number of Businesses Formed Per Year in Grand Junction: \n ', count_grand_junc)
    simple_line_plot(count_grand_junc, 'year', 'total', 'Year', 'Number of Businesses Formed', 'Number of Businesses Formed Per Year in Grand Junction 2001-2017', label_vert='vertical', y_min=0, y_max=2500)

    entity_type_grand_junc = counts(df_grand_junc, 'entitytype', 'entityid', 'entityid')
    entity_type_grand_junc = percentage(entity_type_grand_junc, 'total', total_bus_grand_junc, 'percent_total', 2)
    print('Number of Businesses Formed by Type in Grand Junction: \n ', entity_type_grand_junc)
    pie_chart(entity_type_grand_junc['percent_total'][0:3], entity_type_grand_junc['entitytype'][0:3], 'Top 3 Entity Types of Grand Junction Businesses Formed 2001-2017')

    df_gdp_grand_junc = count_grand_junc.copy()
    df_gdp_grand_junc = pd.merge(df_gdp_grand_junc, grand_junc_gdp_pc, on='year', how='left')

    # number of businesses formed per year - linear regression
    linear_regression(count_grand_junc, 'year', 'total', 'Grand Junction Number of Businesses Formed Per Year', 'Year', 'Number of Businesses', y_min=0, y_max=2500)

    # real gdp per capita
    linear_regression(df_gdp_grand_junc, 'year', 'real_per_capita_gdp', 'Grand Junction Real GDP Per Capita 2001-2017', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_grand_junc, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Grand Junction Real GDP Per Capita 2001-2017', label_vert='vertical', y_min=20000, y_max=72000)
    simple_line_plot(df_gdp_grand_junc, 'year', 'real_per_capita_gdp', 'Year', 'Real GDP Per Capita (chained 2009 dollars)', 'Grand Junction Real GDP Per Capita 2001-2017 Zoomed', label_vert='vertical')
