import pytest

from wallet import Wallet, InsufficientAmount

# initial = Wallet(0)
# firstAdd = Wallet(100)

@pytest.fixture
def empty_wallet():
    '''Returns a Wallet instance with a zero balance'''
    return Wallet(0)

@pytest.fixture
def wallet():
    '''Returns a Wallet instance with a balance of 20'''
    return Wallet(100)

def test_default_init_amount(empty_wallet):
    assert empty_wallet.balance == 0

def test_setting_initial_amount(wallet):
    assert wallet.balance == 100

def test_wallet_add_cash(wallet):
    wallet.wallet_add_cash(90)
    assert wallet.balance == 190

def test_wallet_spend_cash(wallet):
    wallet.wallet_spend_cash(10)
    assert wallet.balance == 90

def test_wallet_spend_cash_raises_exception_on_insufficient_amount(wallet):
    with pytest.raises(InsufficientAmount):
        wallet.wallet_spend_cash(200)

# 以下这两个部分，如果都是为了同时测试多个函数的话，是需要连在一起写的！！！！
@pytest.mark.parametrize("added,spent,expected", [
    (30, 10, 20),
    (20, 2, 18),
])

# 如果要用之前定义好的class，在参数里一定要加上这个class的名称！！！！！！
def test_transaction(empty_wallet, added, spent, expected):
    # my_wallet = Wallet(0)
    empty_wallet.wallet_add_cash(added)
    empty_wallet.wallet_spend_cash(spent)

    assert empty_wallet.balance == expected
