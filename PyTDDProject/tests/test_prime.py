# a Python program that returns the sum of all numbers in a sequence that are prime numbers
# test cases

import sys
sys.path.insert(0,'/Users/Shawn/Desktop/PyTDDProject/modules')
import prime

def test_number_less_than_two_is_not_prime():
    assert prime.is_prime(1) == False

def test_has_other_divisor_other_than_one_and_itself_is_not_prime():
    assert prime.is_prime(3) == True
    assert prime.is_prime(17) == True

def test_has_only_one_and_itself_as_divisor_is_prime():
    assert prime.is_prime(9) == False
    assert prime.is_prime(9999999999999) == False


def test_only_prime_can_be_added():
    assert prime.sum_of_primes([13,2,25]) == 15
    assert prime.sum_of_primes([9,8,4,11,1]) == 11
    assert prime.sum_of_primes([13,29,2]) == 44
