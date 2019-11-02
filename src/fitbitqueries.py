import pandas as pd
import numpy as np

def create_chunks(l, n):
    """
    :param l: list like iterable 
    :param n: max size of chunk
    
    :return: list of list containing chunks of size n. 
             The last element has length rem(len(list_var),n) which is between 0 and n.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]

def split_date_range(start, end, max_size=100):
    """
    :param start: start date, string or datetime object
    :param end: end date, string or datetime object
    :param max_size: maximum number of dates in each interval
    
    :return: list of tuples containing smaller chunks of date ranges
    """
    
    dates = pd.date_range(start, end)
    date_splits = create_chunks(dates, max_size)
    
    return [(date_split[0], date_split[-1]) for date_split in date_splits]


def get_sleep_data(auth_client, start, end):
    """
    :param auth_client: fitbit API object
    :param start: start date
    :param end: end date
    
    :return: pandas dataframe with sleep data
    """
    # Pull sleep data for each split
    sleep = []
    for endpoint in split_date_range(start, end):
        sleep += auth_client.time_series(
            resource='sleep', base_date=endpoint[0], end_date=endpoint[-1]
        )['sleep']

    # Parse sleep data range API output 
    sleep_data = [{item:s[item] for item in sleep[0].keys()} for s in sleep]
    
    # Create dataframe 
    df = pd.DataFrame(sleep_data)
    df['dateOfSleep'] = pd.to_datetime(df['dateOfSleep'])
    df = df.sort_values('dateOfSleep').reset_index(drop=True)
    
    return df