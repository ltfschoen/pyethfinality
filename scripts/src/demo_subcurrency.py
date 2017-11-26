import json
import web3
import solc
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import install_solc, compile_source, compile_files
# Note: py-solc only supports up to 0.4.17
# Note: Below line will install Solc v0.4.17
# install_solc('v0.4.17')
from web3.contract import ConciseContract
from datetime import datetime

def current_time():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-1]

# Middleware Data Structures
class Blockchain(object):

    def __init__(self, blocks):
        self.blocks = blocks
        self.created_at = current_time()

    def is_longest(self, status):
        self.is_longest = status

    def median_account_balance(self):
        account_balances = map((lambda x:func(x.account.balance)), self.blocks)
        return sorted(account_balances)[len(self.account_balances) / 2]

class Block(object):

    def __init__(self, block_name, blockchain_id):
        self.block_name = block_name
        self.blockchain_id = blockchain_id
        self.created_at = current_time()

class Account(object):

    def __init__(self, block_id, address, balance=0):
        self.address = address
        self.balance = balance
        self.block_id = block_id

class Transaction(object):

    def __init__(self, tx_receipt, account_id, address_from, address_to, amount, status, probability_reverted):
        self.tx_receipt = tx_receipt
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount
        self.status = status
        self.probability_reverted = probability_reverted
        self.account_id = account_id
        self.transfer()

    def transfer(self):
        self.account_from.balance -= self.amount
        self.account_to.balance += self.amount

class BlockConfirmation(object):

    def __init__(self, block_id, transaction_id, block_hash, previous_block_id):
        self.block_id = block_id
        self.transaction_id = transaction_id
        self.block_hash = block_hash
        self.previous_block_id = previous_block_id
        self.created_at = current_time()

class EventLog(object):

    def __init__(self, block_confirmation_id, log_hash, topic_name):
        self.block_confirmation_id = block_confirmation_id
        self.log_hash = log_hash
        self.topic_name = topic_name
        self.created_at = current_time()

# Web3.py Middleware
class Middleware(object):
    def __init__(self, make_request, web3):
        self.web3 = web3
        self.make_request = make_request

    def __call__(self, method, params):
        # do pre-processing here

        # perform the RPC request, getting the response
        response = self.make_request(method, params)

        # do post-processing here

        # finally return the response
        return response


def run():
    # Solidity source code
    contract_source_code = '''
    pragma solidity ^0.4.17;

    /*
    *  About: Contract that implements simplest form of Cryptocurrency that generates
    *    coins out of thin air. Issuance scheme prevents generation of coins by anyone
    *    other than creator of the Contract. Anyone may send coins to each other with
    *    only an Ethereum keypair required.
    */
    contract SubCurrency {
        /// Generates function `minter()` allowing state variable value to be readable from outside by other contracts.
        address public minter;

        /// Getter function `balances(address)` to check an account balance from outside by other contracts 
        /// is generated by use of the `public` keyword. Maps 
        mapping (address => uint) public balances;

        /// Middleware listens for this event to fire on the blockchain with minimal cost when `sendSubCurrency` called.
        /// Listener receives arguments `from`, `to`, `amount` when "event" fired to help track transactions.
        event SentSubCurrency(address from, address to, uint amount);

        // Constructor run only when contract created to generate minter initial account balance
        function SubCurrency() {
            minter = msg.sender;
            balances[tx.origin] = 1000;
        }

        function sendSubCurrency(address receiver, uint amount) returns (bool success) {
            if (balances[msg.sender] < amount) {
                return false;
            }
            balances[msg.sender] -= amount;
            balances[receiver] += amount;
            SentSubCurrency(msg.sender, receiver, amount);
            return true;
        }

        function getBalance (address user) constant returns (uint balance) {
            return balances[user];
        }

        /// Fallback Function
        function() {}
    }
    '''

    # Compiled source code
    compiled_sol = compile_source(contract_source_code)
    # Reference: https://github.com/ethereum/py-solc
    # compiled_sol = compile_files(["./contracts/src/SubCurrency.sol"])
    contract_interface = compiled_sol['<stdin>:SubCurrency']

    # Web3.py instance
    # web3 = Web3(TestRPCProvider())
    web3 = Web3(HTTPProvider('http://localhost:8545'))
    print('TestRPC accounts: {}'.format(web3.eth.accounts))
    print('TestRPC block number: {}'.format(web3.eth.blockNumber))


    # Instantiate and deploy contract
    # http://web3py.readthedocs.io/en/latest/web3.eth.html#contracts
    contract = web3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])

    # Get transaction hash from deployed contract
    # http://web3py.readthedocs.io/en/latest/contracts.html?highlight=deploy#web3.contract.Contract.deploy
    tx_hash = contract.deploy(transaction={'from': web3.eth.accounts[0], 'gas': 4712387})

    # Get tx receipt to get contract address
    tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    print('Contract deployed to address: {}'.format(contract_address))

    # Contract instance in concise mode
    # http://web3py.readthedocs.io/en/latest/contracts.html?highlight=deploy#web3.contract.ConciseContract
    contract_instance = web3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

    # Getters + Setters for web3.eth.contract object
    print('Minter address: {}'.format(contract_instance.minter()))
    minter_balance = contract_instance.minter()
    print('Minter balance: {}'.format(contract_instance.balances(minter_balance)))

    def get_balance(account):
        return web3.fromWei(web3.eth.getBalance(account), "ether")

    print('Account #1 & #2 balances - BEFORE tx: {}, {}'.format(get_balance(web3.eth.accounts[0]), get_balance(web3.eth.accounts[1])))
    tx_res = contract_instance.sendSubCurrency(web3.eth.accounts[0], 50)
    print('Tx successful: {}'.format(tx_res))
    print('Account #1 & #2 balances - AFTER tx: {}, {}'.format(get_balance(web3.eth.accounts[0]), get_balance(web3.eth.accounts[1])))
    print('Account #1 balance: {}'.format(contract_instance.getBalance(web3.eth.accounts[0])))
    print('Account #2 balance: {}'.format(contract_instance.getBalance(web3.eth.accounts[1])))
    print('TestRPC block number: {}'.format(web3.eth.blockNumber))
    print('TestRPC block details: {}'.format(web3.eth.getBlock('latest')))

    # Web3.py API Block, Transaction, and Event Log Filters 
    # Reference: http://web3py.readthedocs.io/en/latest/filters.html
    # web3.utils.filters.get_all_entries()

    # Web3.py Middleware
    # Reference: http://web3py.readthedocs.io/en/latest/middleware.html
    web3.middleware_stack.clear()
    assert len(web3.middleware_stack) == 0

    # Web3.py TX Pool API
    print('Tx Pool: {}'.format(web3.txpool.inspect))

if __name__ == '__main__':
    run()