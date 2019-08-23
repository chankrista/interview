# Problem 1: String Sorter

Files in this folder answer problem 1:

The user has a file that is made up of short (less than 1000 character) strings, each on a different line (assume any common character or character combination that means a newline to someone might be used interchangeably in this file). Most of these strings will be preceded by numbers, i.e. “2 Steaks”, “10 Chicken Wings”, “343GuiltySparks”. Accept the file from the user and return them a file with the same items sorted first by the numeric value of any leading number (2 < 10 < 343) and then alphabetically for the rest of the string.

## Requirements

Python 3.x
Packages documented within requirements.txt or downloaded via `pip install -r requirements.txt`

## Usage

My solution provides a command-line interface for sorting text according to the criteria described in the prompt. The text must be entered in a locally saved .txt file.

To sort a file, enter the command

	$ python p1.py sort <path>

The same file will be overwritten with the sorted outcome.

For example, to load a sorted file in "strings/my_strings_sorted.txt" based on the existing unsorted file, "strings/my_strings.txt", run

	$ python p1.py sort "strings/my_strings.txt"

## Tests

Test code is available within tests.py. Run using `pytest tests.py`.