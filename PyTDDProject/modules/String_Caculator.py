# Create a simple String calculator with a method int Add(string numbers)
# The method can take 0, 1 or 2 numbers, and will return their sum
# python program

def add(list):
    if len(list) > 2:
        raise('More than two numbers can not be added')
    elif len(list) == 0:
        return 0
    else:
        sum = 0
        for n in list:
            if not int(n):
                raise('Input type needs to be number')
            elif int(n) < 0:
                raise('Negatives not allowed')
            elif int(n) > 1000:
                n = 0
                sum += int(n)
            else:
                sum += int(n)
        return sum
