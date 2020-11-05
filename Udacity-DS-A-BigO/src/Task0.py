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
TASK 0:
What is the first record of texts and what is the last record of calls?
Print messages:
"First record of texts, <incoming number> texts <answering number> at time <time>"
"Last record of calls, <incoming number> calls <answering number> at time <time>, lasting <during> seconds"
"""

def get_first(lst):
    """
    Get the first object in a list.

    Parameters
    ----------
    lst : List
        A list of objects.

    Returns
    -------
    Object
        The first object in the list.
    """
    return lst[0]

def test_get_first():
    assert (get_first(texts) == ['97424 22395', '90365 06212',
                                    '01-09-2016 06:03:22'])
    print('get_first Test Passed')

def get_last(lst):
    """
    Get the last item in a list.

    Parameters
    ----------
    lst : List
        A list of objects.

    Returns
    -------
    Object
        Returns the last object in the list.
    """
    return lst[-1]

def test_get_last():
    assert (get_last(calls) == ['98447 62998', '(080)46304537',
                                    '30-09-2016 23:57:15', '2151'])
    print('get_last Test Passed')

if __name__ == '__main__':

    ### call test functions
    test_get_first()
    test_get_last()

    ### call functions
    first_text = get_first(lst=texts)
    last_call = get_last(lst=calls)

    print(f"First record of texts, {first_text[0]} texts {first_text[1]} at time {first_text[2]}")
    print(f"Last record of calls, {last_call[0]} calls {last_call[1]} at time {last_call[2]}, lasting {last_call[3]} seconds")
