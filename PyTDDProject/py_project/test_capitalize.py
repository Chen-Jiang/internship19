import pytest

# x is a String as argument
def capital_case(x):
    if isinstance(x,str):
        return x.capitalize()
    else:
        raise TypeError('argument is not String')

def test_capital_case():
    assert capital_case("semaphore") == "Semaphore"

def test_raises_exception_when_argument_is_not_String():
    with pytest.raises(TypeError):
        capital_case(10)
