import pytest
import sys
sys.path.insert(0, "/Users/Shawn/Desktop/PyTDDProject")
from modules import first

case = first.First()
def test_firstHello():

    result = case.firstHello("World")

    assert result == 'Hello World'


def test_divisor_can_not_be_zero():
    with pytest.raises(ZeroDivisionError) as e_info:
        case.calculate_division(8,0)
        raise Exception('Zero can not be divisor')
    # exception_raised = e_info.value
    # assert calculate_division(8,0)
