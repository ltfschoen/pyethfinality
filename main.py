import json
import web3
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract Greeter {
    string public greeting;

    function Greeter() {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
'''
# Compiled source code
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Greeter']

# Web3.py instance
web3 = Web3(TestRPCProvider())
# web3 = Web3(HTTPProvider('http://localhost:8545'))
web3.eth.blockNumber

# Instantiate and deploy contract
# http://web3py.readthedocs.io/en/latest/web3.eth.html#contracts
contract = web3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
# http://web3py.readthedocs.io/en/latest/contracts.html?highlight=deploy#web3.contract.Contract.deploy
tx_hash = contract.deploy(transaction={'from': web3.eth.accounts[0], 'gas': 410000})

# Get tx receipt to get contract address
tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
# http://web3py.readthedocs.io/en/latest/contracts.html?highlight=deploy#web3.contract.ConciseContract
contract_instance = web3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.greet()))
contract_instance.setGreeting('Nihao', transact={'from': web3.eth.accounts[0]})
print('Setting value to: Nihao')
print('Contract value: {}'.format(contract_instance.greet()))