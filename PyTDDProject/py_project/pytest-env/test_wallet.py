import pytest

def test_wallet_exist():
    my_wallet = Wallet()
    assert my_wallet.balance == 0
