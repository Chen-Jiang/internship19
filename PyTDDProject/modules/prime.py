# a Python program that returns the sum of all numbers in a sequence that are prime numbers
# python program

import math

def is_prime(number):
    if number < 2:
        return False
    else:
        count = 0
        for i in range(2,math.floor(math.sqrt(number)+1)):
            if number % i == 0:
                count += 1
        if count == 0:
            return True
        elif count >= 1:
            return False

def sum_of_primes(list):
    sum = 0
    for num in list:
        if is_prime(num):
            sum += num
    return sum
