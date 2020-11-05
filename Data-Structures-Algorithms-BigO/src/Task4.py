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
TASK 4:
The telephone company want to identify numbers that might be doing
telephone marketing. Create a set of possible telemarketers:
these are numbers that make outgoing calls but never send texts,
receive texts or receive incoming calls.

Print a message:
"These numbers could be telemarketers: "
<list of numbers>
The list of numbers should be print out one per line in lexicographic order with no duplicates.
"""

def get_separate_sets(phone_list):
    """
    Creates two unique sets of data from the first two columns.

    Parameters
    ----------
    phone_list : List
        List of lists containing call records as strings.
        Assumes
            column 0: incoming phone number (string)
            column 1: receiving phone number (string)

    Returns
    -------
    Set
        Unique set of values from column 0.

    Set
        Unique set of values from column 1.
    """
    sender_set = set()
    receiver_set = set()
    for record in phone_list:
        sender_set.add(record[0])
        receiver_set.add(record[1])
    return sender_set, receiver_set

def get_aggregate_set(phone_list):
    """
    Creates one unique set of data from the first two columns.

    Parameters
    ----------
    phone_list : List
        List of lists containing call records as strings.
        Assumes
            column 0: incoming phone number (string)
            column 1: receiving phone number (string)

    Returns
    -------
    Set
        Unique set of values from columns 0 and 1.
    """
    agg_set = set()
    for record in phone_list:
        agg_set.add(record[0])
        agg_set.add(record[1])
    return agg_set

def find_telemarketers(calls_list=calls, texts_list=texts):
    """
    Finds a list of phone numbers of possible telemarketers.

    Parameters
    ----------
    calls_list : List
        List of lists containing call records as strings.
        Assumes
            column 0: incoming phone number (string)
            column 1: receiving phone number (string)
    texts_list : List
        List of lists containing call records as strings.
        Assumes
            column 0: sending phone number (string)
            column 1: receiving phone number (string)

    Returns
    -------
    List
        A sorted list of phone numbers as strings.

    """
    possible_telemkt = set()
    caller_set, receiver_set = get_separate_sets(calls_list)
    texts_set = get_aggregate_set(texts_list)
    for caller in caller_set:
        if caller not in receiver_set and caller not in texts_set:
            possible_telemkt.add(caller)
    sorted_telemkt_list = sorted(possible_telemkt)
    return sorted_telemkt_list

def test_find_telemarketers():
    """
    Test function for find_telemarketers function
    """
    assert (find_telemarketers(calls, texts) == ['(022)37572285',
                    '(022)65548497','(022)68535788','(022)69042431',
                    '(040)30429041','(044)22020822','(0471)2171438',
                    '(0471)6579079','(080)20383942','(080)25820765',
                    '(080)31606520','(080)40362016','(080)60463379',
                    '(080)60998034','(080)62963633','(080)64015211',
                    '(080)69887826','(0821)3257740','1400481538',
                    '1401747654','1402316533','1403072432','1403579926',
                    '1404073047','1404368883','1404787681','1407539117',
                    '1408371942','1408409918','1408672243','1409421631',
                    '1409668775','1409994233','74064 66270','78291 94593',
                    '87144 55014','90351 90193','92414 69419','94495 03761',
                    '97404 30456','97407 84573','97442 45192','99617 25274'])
    print("find_telemarketers Test Passed")

if __name__ == '__main__':
    # run test
    test_find_telemarketers()

    # run code
    telemkt_list = find_telemarketers(calls, texts)
    print("These numbers could be telemarketers: ")
    print(*telemkt_list, sep='\n')
