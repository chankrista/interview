import pytest
import p1

def test_number_sort_1():
	assert p1.number_sort(["f", "2 d", "2 c", "1 a", "0fl", "e", "1 b"]) == \
		{0: ["fl"], 1: [" a", " b"], 2: [" d", " c"], \
		float('inf'): ["f", "e"]}

def test_make_list():
	assert p1.make_list(
		{0: [" a", "a"], 2: ["", "  l"], float('inf'): ["zz", "az"]}) == \
		['0 a', '0a', '2', '2  l', 'az', 'zz']

def test_sort_string():
	assert p1.sort_string("600\n~*0\n0123hello\n321hello\nhello") == \
		'123hello\n321hello\n600\nhello\n~*0'
