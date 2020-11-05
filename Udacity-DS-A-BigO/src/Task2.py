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
TASK 2: Which telephone number spent the longest time on the phone
during the period? Don't forget that time spent answering a call is
also time spent on the phone.
Print a message:
"<telephone number> spent the longest time, <total time> seconds, on the phone during
September 2016.".
"""

def find_longest_duration(call_list=calls):
    """
    Finds the phone number that spent the longest time on the phone
    Assumes phone_list is a list of lists containing incoming and receiving
        phone numbers in the first two columns (string) and duration of the
        call in the fourth column (string)
    Returns a phone number (string) and the summed duration of seconds on
        the phone
    """
    unique_num_dict = dict()
    for record in call_list:
        if record[0] in unique_num_dict:
            unique_num_dict[record[0]] += int(record[3])
        else:
            unique_num_dict[record[0]] = int(record[3])
        if record[1] in unique_num_dict:
            unique_num_dict[record[1]] += int(record[3])
        else:
            unique_num_dict[record[1]] = int(record[3])
    max_phone = max(unique_num_dict, key=unique_num_dict.get)
    max_duration = unique_num_dict[max_phone]
    return max_phone, max_duration


def test_find_longest_duration():
    """
    Test find_longest_duration function
    """
    assert (find_longest_duration(calls) == ('(080)33251027', 90456))
    print('find_longest_duration Tests Passed')


if __name__ == '__main__':
    # run test code
    test_find_longest_duration()

    # run code
    phone_num, duration = find_longest_duration(call_list=calls)
    print(f"{phone_num} spent the longest time, {duration} seconds, on the phone during September 2016.")
