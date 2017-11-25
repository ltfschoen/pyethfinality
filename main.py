import json
import web3
import solc
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import install_solc, compile_source, compile_files
# Note: py-solc only supports up to 0.4.17
# Note: Below line will install Solc v0.4.17
# install_solc('v0.4.17')
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract Greeter {
    string public greeting;

    event LogGreeting();

    /// Greeter smart contract - Greeter() function called
    function Greeter() {
        greeting = 'Hello';
    }

    /// Greeter smart contract - setGreeter() function called
    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    /// Greeter smart contract - greet() function called
    function greet() constant returns (string) {
        LogGreeting();
        return greeting;
    }
}
'''

# Compiled source code
compiled_sol = compile_source(contract_source_code)
# Reference: https://github.com/ethereum/py-solc
# compiled_sol = compile_files(["./contracts/Greeter.sol"])
contract_interface = compiled_sol['<stdin>:Greeter']

# Web3.py instance
web3 = Web3(TestRPCProvider())
# web3 = Web3(HTTPProvider('http://localhost:8545'))
print('TestRPC accounts: {}'.format(web3.eth.accounts))
print('TestRPC block number: {}'.format(web3.eth.blockNumber))


# Instantiate and deploy contract
# http://web3py.readthedocs.io/en/latest/web3.eth.html#contracts
contract = web3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
# http://web3py.readthedocs.io/en/latest/contracts.html?highlight=deploy#web3.contract.Contract.deploy
tx_hash = contract.deploy(transaction={'from': web3.eth.accounts[0], 'gas': 410000})

# Get tx receipt to get contract address
tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']
print('Contract deployed to address: {}'.format(contract_address))

# Contract instance in concise mode
# http://web3py.readthedocs.io/en/latest/contracts.html?highlight=deploy#web3.contract.ConciseContract
contract_instance = web3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.greet()))
contract_instance.setGreeting('Nihao', transact={'from': web3.eth.accounts[0]})
print('Setting value to: Nihao')
print('Contract value: {}'.format(contract_instance.greet()))
print('TestRPC block number: {}'.format(web3.eth.blockNumber))
print('TestRPC block details: {}'.format(web3.eth.getBlock('latest')))

print('TestRPC current gas price: {}'.format(web3.eth.gasPrice))
print('TestRPC syncing status: {}'.format(web3.eth.syncing))
print('TestRPC mining status: {}'.format(web3.eth.mining))
