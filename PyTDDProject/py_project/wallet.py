
# EXCEPTION here, and the argument of Exception should be "Exception"!!!
class InsufficientAmount(Exception):
    pass

class Wallet(object):

    #  init function, the underline is two "_"
    #  if I write the function like this, means that the init function must has one argument, amount, so if amount = 0, it also writes down 0
    def __init__(self, amount):
        self.balance = amount

    # def __init__(self, initial_amount=0):
    #     self.balance = initial_amount

    def wallet_add_cash(self, amount):
        if isinstance(amount, int):
            self.balance += amount
        else:
            raise TypeError('amount should be integer')

    def wallet_spend_cash(self,amount):
        if isinstance(amount, int):
            if self.balance < amount:
                raise InsufficientAmount('Balance is less than your spend {}'.format(amount))
            else:
                self.balance -= amount
        else:
            raise TypeError('amount should be integer')
