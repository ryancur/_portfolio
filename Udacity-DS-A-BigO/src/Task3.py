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
TASK 3:
(080) is the area code for fixed line telephones in Bangalore.
Fixed line numbers include parentheses, so Bangalore numbers
have the form (080)xxxxxxx.)

Part A: Find all of the area codes and mobile prefixes called by people
in Bangalore.
 - Fixed lines start with an area code enclosed in brackets. The area
   codes vary in length but always begin with 0.
 - Mobile numbers have no parentheses, but have a space in the middle
   of the number to help readability. The prefix of a mobile number
   is its first four digits, and they always start with 7, 8 or 9.
 - Telemarketers' numbers have no parentheses or space, but they start
   with the area code 140.

Print the answer as part of a message:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
The list of codes should be print out one per line in lexicographic order with no duplicates.

Part B: What percentage of calls from fixed lines in Bangalore are made
to fixed lines also in Bangalore? In other words, of all the calls made
from a number starting with "(080)", what percentage of these calls
were made to a number also starting with "(080)"?

Print the answer as a part of a message::
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
The percentage should have 2 decimal digits
"""

def find_all_calls(phone_list=calls):
    """
    Finds all the area codes and mobile prefixes called from Bangalore.

    Parameters
    ----------
    phone_list : List
        List of lists containing call records as strings.
        Assumes
            column 0: incoming phone number (string)
            column 1: receiving phone number (string)

    Returns
    -------
    List
        Returns a sorted unique list of variable length prefixes as strings.

    Float
        The percentage of calls made between landline calls in Bangalore out of
        the total number of calls made from a landline in Bangalore rounded to
        2 decimal places.
    """
    prefix_set = set()
    total_calls = 0
    land_to_land_calls = 0
    for call in phone_list:
        if call[0].startswith('(080)'):
            total_calls += 1
            if call[1].startswith('('):
                last_idx = call[1].find(')')
                prefix_set.add(call[1][:last_idx+1])
            if call[1][0] in ['7', '8', '9']:
                prefix_set.add(call[1][:4])
            if call[1].startswith('140'):
                prefix_set.add('140')
            if call[1].startswith('(080)'):
                land_to_land_calls += 1
    prefix_sorted = sorted(prefix_set)
    pct_total = round((land_to_land_calls / total_calls) * 100, 2)
    return prefix_sorted, pct_total

def test_find_all_calls():
    """
    Test function for find_all_calls function
    """
    assert (find_all_calls(calls) == ['(022)','(040)','(04344)','(044)',
                                    '(04546)','(0471)','(080)','(0821)','7406',
                                    '7795','7813','7829','8151','8152','8301',
                                    '8431','8714','9008','9019','9035','9036',
                                    '9241','9242','9341','9342','9343','9400',
                                    '9448','9449','9526','9656','9738','9740',
                                    '9741','9742','9844','9845','9900','9961'],
                                    24.81)
    print("find_all_calls Tests Passed")


if __name__ == '__main__':
    # test functions
    test_find_all_calls()

    # run code
    prefix_list, pct_total = find_all_calls(phone_list=calls)
    print("The numbers called by people in Bangalore have codes:")
    print(*prefix_list, sep = "\n")
    print(f"{pct_total} percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore.")
