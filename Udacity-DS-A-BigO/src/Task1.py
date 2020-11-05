"""
Read file into texts and calls.
"""
import csv
with open('../data/texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('../data/calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
TASK 1:
How many different telephone numbers are there in the records?
Print a message:
"There are <count> different telephone numbers in the records."
"""

def get_unique_set(lst):
    """
    Creates a set of unique values within a list.

    Parameters
    ----------
    lst : List
        List of lists that have strings in each column.
        Assumes the desired data is in the first two (2) columns: [0] and [1].

    Returns
    -------
    Set
        Returns a set of unique values found in the first two columns of the
        original list.
    """
    unique_numbers = set()
    for record in lst:
        send_num = record[0]
        receive_num = record[1]
        unique_numbers.add(send_num)
        unique_numbers.add(receive_num)
    return unique_numbers

def num_unique_phone_numbers(list1, list2):
    """
    Calculates the number of unique values within the first two columns of both
    lists passed in.

    Parameters
    ----------
    list1 : List
        List of lists. Each row is a list of strings.
    list2 : List
        List of lists. Each row is a list of strings.

    Returns
    -------
    Integer
        The total number of unique values found in the first two (2) columns of
        each list.
    """
    list1_set = get_unique_set(list1)
    list2_set = get_unique_set(list2)
    union_set = list1_set | list2_set
    unique_numbers = len(union_set)
    return unique_numbers

def pandas_check(phone_lists=[texts, calls]):
    '''
    A check function to verify the results of num_unique_numbers
    Assumes phone_lists is a list of lists including the send and receive
        phone numbers in the first two columns and they are strings.
    Returns an integer with the number of unique values in the lists
    '''
    df_calls = pd.DataFrame(calls)
    df_texts = pd.DataFrame(texts)

    s = df_calls.iloc[:, 0]
    s = s.append(df_calls.iloc[:, 1], ignore_index=True)
    s = s.append(df_texts.iloc[:, 0], ignore_index=True)
    s = s.append(df_texts.iloc[:, 1], ignore_index=True)
    pandas_num = s.nunique()
    return pandas_num

def test_num_unique_phone_numbers():
    '''
    Test function for num_unique_numbers
    '''
    assert (num_unique_phone_numbers(texts, calls) == pandas_check([texts, calls]))
    print("num_unique_phone_numbers Test Passed")


if __name__ == '__main__':
    ### call test function(s)
    import pandas as pd
    test_num_unique_phone_numbers()

    ### call function(s)
    num_unique = num_unique_phone_numbers(texts, calls)
    print(f"There are {num_unique} different telephone numbers in the records.")
