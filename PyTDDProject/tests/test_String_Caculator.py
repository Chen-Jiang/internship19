# Create a simple String calculator with a method int Add(string numbers)
# The method can take 0, 1 or 2 numbers, and will return their sum
# test cases

import sys
sys.path.insert(0,'/Users/Shawn/Desktop/PyTDDProject/modules')
import pytest
import String_Caculator as str

def test_parameters_no_more_than_two():
    assert str.add([""]) == 0
    assert str.add(["2","12"]) == 14
    assert str.add(["90","1","1000"]) == 1091

def test_parameter_more_than_two():
    with pytest.raises(Exception) as exc_info:
        str.add(["1","5","999","34"])
        str.add(["1","5","999","34","45","444"])
        raise Exception('More than two numbers can not be added')

def test_if_parameter_is_not_integer():
    with pytest.raises(Exception) as exc_info:
        str.add(["1","c"])
        str.add(["h","w"])
        raise Exception('Input type needs to be number')

def test_if_has_negative_parameter():
    with pytest.raises(Exception) as exc_info:
        str.add(["3","-90"])
        str.add(["-9","-23"])
        raise Exception('Negatives not allowed')

def test_if_parameter_more_than_1000():
    assert str.add(["1999999","6666666"]) == 0
    assert str.add(["199999","2"]) == 2

# from here, delimiters situations
# def test_if_new_line_inside_numbers():

# def test_if_delimiter_is_not_comma():

# def test_if_delimiter_length_more_than_one():

# def test_if_has_multiple_delimiters():
