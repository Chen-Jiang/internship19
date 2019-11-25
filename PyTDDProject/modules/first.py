import sys
sys.path.insert(0, "/Users/Shawn/Desktop/PyProject/tests")

class First(object):
    print(1)
    def firstHello(self,name):
        print(2)
        result = "Hello " + name
        print(result)
        return result


    def calculate_division(self,a,b):
        if b != 0:
            return a/b
        else:
            raise(ZeroDivisionError)
