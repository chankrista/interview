"""String sorter
The user has a file that is made up of short (less than 1000 character) strings,
each on a different line (assume any common character or character combination
that means a newline to someone might be used interchangeably in this file).
Most of these strings will be preceded by numbers, i.e. “2 Steaks”,
“10 Chicken Wings”, “343GuiltySparks”. Accept the file from the user and return
them a file with the same items sorted first by the numeric value of any leading
number (2 < 10 < 343) and then alphabetically for the rest of the string.

Usage:
  p1.py sort <path> 
  p1.py (-h | --help)

Options:
  <sort>             Replace the text in the provided path with sorted strings.
  <path>             Location of the stored .txt file.
  -h --help          Show this screen.

Examples:

  Load a sorted file in "strings/my_strings_sorted.txt" based on the existing
  unsorted file "strings/my_strings.txt"
  $ p1.py sort "strings/my_strings.txt"

"""

from docopt import docopt
import re

def number_sort(contents):
    '''
    Takes a list of strings and returns a dictionary with keys as sorted leading
    digits and values as the corresponding strings without leading digits.
    '''
    def find_number(string):
        try:
            return int(re.match('\d*', string).group())
        except:
            return float('inf')
    numbers_list = [find_number(string) for string in contents]
    numbers_list.sort()
    numbers = {number: [] for number in numbers_list}
    for string in contents:
        number = find_number(string)
        numbers[number].append(re.sub('^\d*', '', string))
    return numbers

def make_list(content_dict):
    '''
    Takes a dictionary with numbers as keys and a list of strings as values and
    sorts the lists alphabetically, then adds the number to the beginning of
    the string-unless the number was infinity-and returns a list of the strings
    sorted by the order of numbers in the dictionary and then alphabetically.
    '''
    full_list = []
    for number, string_list in content_dict.items():
        string_list.sort()
        for string in string_list:
            if number == float('inf'):
                full_list.append(string)
            else:
                full_list.append(str(number) + string)
    return full_list

def sort_string(old_str):
    contents = old_str.split('\n')
    content_dict = number_sort(contents)
    full_list = make_list(content_dict)
    return '\n'.join(full_list)

def main():

    arguments = docopt(__doc__)

    if arguments['sort']:
        f = open(arguments['<path>'])
        old_str = f.read()
        new_str = sort_string(old_str)
        assert(len(old_str) == len(new_str))
        f = open(arguments['<path>'], 'w')
        f.write(new_str)
        f.close()

if __name__ == '__main__':
    main()