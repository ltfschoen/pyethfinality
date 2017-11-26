# Reference: https://github.com/loredanacirstea/test-populus/blob/master/tests/test_greeter.py
# Reference: https://github.com/ice09/invite_me/blob/master/registry/test/TestKeybaseRegistryDeployed.sol
import pytest
from ethereum import tester

@pytest.fixture()
# `chain` is a py.test fixture provided by Populus pytest plugin
def subcurrency_contract(chain):
    subcurrency_contract, _ = chain.provider.get_or_deploy_contract('SubCurrency')
    return subcurrency_contract

def test_initial_balance_using_deployed_contract(subcurrency_contract):
    subcurrency = subcurrency_contract.call().minter()
    minter_address = subcurrency.minter()
    assert subcurrency.getBalance(minter_address) == 1000