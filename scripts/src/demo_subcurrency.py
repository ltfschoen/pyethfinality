import json
import web3
import solc
import math
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import install_solc, compile_source, compile_files
# Note: py-solc only supports up to 0.4.17
# Note: Below line will install Solc v0.4.17
# install_solc('v0.4.17')
from web3.contract import ConciseContract
from datetime import datetime
from web3 import middleware
from web3.middleware import pythonic_middleware, attrdict_middleware
# Cache
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

def current_time():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-1]

# Middleware Data Structures
class Blockchain(object):

    def __init__(self, _id, blocks=[]):
        self._id = _id
        self._blocks = blocks
        self._created_at = current_time()

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(self, blocks):
        self._blocks = blocks

    def is_longest(self, status):
        self.is_longest = status

    def median_account_balance(self):
        account_balances = []
        for block in self.blocks:
            for account in block.accounts:
                account_balances.append(account.get_balance())

        return sorted(account_balances)[math.ceil(len(account_balances) / 2)]

class Block(object):

    def __init__(self, id, block_hash, parent_block_hash, accounts=[], transactions=[]):
        self._id = id,
        self._block_hash = block_hash
        self._parent_block_hash = parent_block_hash
        self._accounts = accounts
        self._transactions = transactions
        self._created_at = current_time()

    @property
    def accounts(self):
        return self._accounts

    @accounts.setter
    def accounts(self, accounts):
        self._accounts = accounts

    def set_transaction(self, transaction):
        self._transactions.append(transaction)
        
    def get_balance(self):
        return self._balance

    def get_block_hash(self):
        return self._block_hash
    
    transaction = property(set_transaction)
    balance = property(get_balance)
    block_hash = property(get_block_hash)

    def serialize(self):
        s = dict(id=self._id,
                 block_hash=self._block_hash,
                 parent_block_hash=self._parent_block_hash,
                 accounts=list(map(lambda x: x.__dict__, self._accounts)),
                 transactions=list(map(lambda x: x.__dict__, self._transactions)),
                 created_at=self._created_at)
        return s

class Account(object):

    def __init__(self, address, balance=0):
        self._address = address
        self._balance = balance

    def get_address(self):
        return self._address

    def set_balance(self, balance):
        self._balance = balance
        
    def get_balance(self):
        return self._balance
    
    balance = property(get_balance, set_balance)
    address = property(get_address)

class Transaction(object):

    def __init__(self, tx_receipt, account_id, account_from, account_to, amount, status, probability_reverted):
        self.tx_receipt = tx_receipt
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount
        self.status = status
        self.probability_reverted = probability_reverted
        self.account_id = account_id

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

# FIXME
# Web3.py Middleware
#
# Each middleware in the stack gets invoked before the request 
# reaches the provider, and then processes the result after the 
# provider returns, in reverse order. It is possible for a 
# middleware to return early from a call without the request ever 
# getting to the provider (or even reaching the middlewares further down the stack).
class Middleware(object):
    def __init__(self, make_request, web3):
        self.web3 = web3
        self.make_request = make_request

    def __call__(self, method, params):
        # do pre-processing here
        print('Middleware pre-processing - __call__ method: {}'.format(method))
        print('Middleware pre-processing - __call__ params: {}'.format(params))

        # perform the RPC request, getting the response
        response = self.make_request(method, params)

        # do post-processing here
        print('Middleware post-processing - responses: {}'.format(params))

        # finally return the response
        return response

TEST_RPC_ADDR = 'http://127.0.0.1:8545'

# FIXME
# Makes a request to a given URL (first arg) and optional params (second arg)
def make_request(*args):
    opener = build_opener()
    opener.addheaders = [('User-agent',
                          'Mozilla/5.0'+str(random.randrange(1000000)))]
    try:
        return opener.open(*args).read().strip()
    except Exception as e:
        try:
            p = e.read().strip()
        except:
            p = e
        raise Exception(p)

def get_or_set_blockchain_data(name, serialized_blocks):
    rv = cache.get(name)
    if rv is None:
        rv = serialized_blocks
        cache.set(name, rv, timeout=5 * 60)
    return rv

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

        /// Transferred between two accounts
        event TransferredSubCurrency(address from, address to, uint amount);

        // Constructor run only when contract created to generate minter initial account balance
        function SubCurrency() {
            minter = msg.sender;
            balances[tx.origin] = 1000;
        }

        function sendSubCurrency(address sender, address receiver, uint amount) public returns (bool success) {
            if (balances[sender] < amount) {
                return false;
            }
            balances[sender] -= amount;
            balances[receiver] += amount;
            SentSubCurrency(sender, receiver, amount);
            return true;
        }

        function transferSubCurrency(address sender, address receiver, uint amount) public returns (bool success) {
            if (balances[sender] < amount) {
                return false;
            }
            balances[sender] -= amount;
            balances[receiver] += amount;
            TransferredSubCurrency(sender, receiver, amount);
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

    # Web3.py Middleware
    # Reference: http://web3py.readthedocs.io/en/latest/middleware.html

    # FIXME
    # Add Middleware
    # web3.middleware_stack.add(pythonic_middleware(make_request(TEST_RPC_ADDR), web3), 'pythonic')

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
    tx1 = contract_instance.sendSubCurrency(web3.eth.accounts[0], web3.eth.accounts[1], 50)
    print('Tx1 successful: {}'.format(tx1))
    tx2 = contract_instance.sendSubCurrency(web3.eth.accounts[0], web3.eth.accounts[1], 200)
    print('Tx2 successful: {}'.format(tx2))
    tx3 = contract_instance.sendSubCurrency(web3.eth.accounts[0], web3.eth.accounts[1], 300)
    print('Tx3 successful: {}'.format(tx3))
    print('Account #1 & #2 balances - AFTER tx: {}, {}'.format(get_balance(web3.eth.accounts[0]), get_balance(web3.eth.accounts[1])))
    print('Account #1 balance: {}'.format(contract_instance.getBalance(web3.eth.accounts[0])))
    print('Account #2 balance: {}'.format(contract_instance.getBalance(web3.eth.accounts[1])))
    print('TestRPC block number: {}'.format(web3.eth.blockNumber))
    print('TestRPC block details: {}'.format(web3.eth.getBlock('latest')))

    print('Accounts: {}'.format(web3.eth.accounts));

    # transactions for longest (only) block 
    transactions = web3.eth.getBlock('latest')['transactions']
    print('Blockchain transactions: {}'.format(transactions))

    # FIXME
    # Web3.py API Block, Transaction, and Event Log Filters 
    # Reference: http://web3py.readthedocs.io/en/latest/filters.html
    # print('Web3 Filters: {}'.format(web3.utils.filters.get_all_entries()))

    # FIXME
    # Web3.py TX Pool API
    print('Tx Pool: {}'.format(web3.txpool.__dict__))

    # Demonstration of generating a list of sample transactions with multiple chain reorganisations
    # that each would result in different balances. We handle this by our algorithm calculating 
    # the longest one of these chains and providing that to the Client App

    a1 = web3.eth.accounts[0]
    a2 = web3.eth.accounts[1]

    # Create Chain No. 1.
    #   - Balance of Account No. 0 (with address 0x7e5f4552091a69125d5dfcb7b8c2659029395bdf): 5
    #   - Balance of Account No. 1 (with address 0x2b5ad5c4795c026514f8317c7a215e218dccd6cf): 37

    # Blockchain 1
    # ==============
    blockchain1 = Blockchain(_id=1)
    
    # Block 0 on Blockchain 1
    block0 = Block(0, web3.eth.getBlock('latest')['hash'], web3.eth.getBlock('latest')['parentHash'])
    blockchain1.blocks.append(block0)
    account1 = Account(a1, contract_instance.getBalance(a1))
    account2 = Account(a2, contract_instance.getBalance(a2))
    block0.accounts.append(account1)
    block0.accounts.append(account2)

    # Block 1 on Blockchain 1
    block1 = Block(1, '0xa700000000000000000000000000000000000000000000000000000000000000', block0.get_block_hash())
    blockchain1.blocks.append(block1)
    account1 = Account(a1, contract_instance.getBalance(a1))
    account2 = Account(a2, contract_instance.getBalance(a2))
    block1.accounts.append(account1)
    block1.accounts.append(account2)

    # Block 2 on Blockchain 1 (with transfer)
    block2 = Block(2, '0x7100000000000000000000000000000000000000000000000000000000000000', block1.get_block_hash())
    blockchain1.blocks.append(block2)
    account1 = Account(a1, contract_instance.getBalance(a1))
    account2 = Account(a2, contract_instance.getBalance(a2))
    block2.accounts.append(account1)
    block2.accounts.append(account2)
    # Simulate transfer on Block 2 of Blockchain 1
    tx1_bc1_from = a1
    tx1_bc1_to = a2
    tx1_bc1_amount = 5000
    tx1_bc1 = contract_instance.transferSubCurrency(tx1_bc1_from, tx1_bc1_to, tx1_bc1_amount)
    transaction1 = Transaction(None, tx1_bc1_from, tx1_bc1_to, tx1_bc1_amount, 'pending', 0.5, account1.get_address())
    block2.set_transaction(transaction1)

    # Blockchain 2
    # ==============
    blockchain2 = Blockchain(_id=2)

    # Create Chain No. 2 

    # Block 3 on Blockchain 2 has Parent of Block 0 on Blockchain 1 (has same Block ID of 1 as that already on Chain No. 1)
    block3 = Block(1, '0xfb00000000000000000000000000000000000000000000000000000000000000', block0.get_block_hash())
    blockchain2.blocks.append(block3)
    account1 = Account(a1, contract_instance.getBalance(a1))
    account2 = Account(a2, contract_instance.getBalance(a2))
    block3.accounts.append(account1)
    block3.accounts.append(account2)

    # Block 4 on Blockchain 2 has Parent of Block 3 on Blockchain 2 (has same Block ID of 2 as that already on Chain No. 1)
    block4 = Block(2, '0x5a00000000000000000000000000000000000000000000000000000000000000', block3.get_block_hash())
    blockchain2.blocks.append(block4)
    account1 = Account(a1, contract_instance.getBalance(a1))
    account2 = Account(a2, contract_instance.getBalance(a2))
    block4.accounts.append(account1)
    block4.accounts.append(account2)
    # Simulate transfer on Block 4 of Blockchain 2
    tx1_bc2_from = a1
    tx1_bc2_to = a2
    tx1_bc2_amount = 34000
    tx1_bc2 = contract_instance.transferSubCurrency(tx1_bc2_from, tx1_bc2_to, tx1_bc2_amount)
    transaction2 = Transaction(None, tx1_bc2_from, tx1_bc2_to, tx1_bc2_amount, 'pending', 0.5, account2.get_address())
    block4.set_transaction(transaction2)

    # Block 5 on Blockchain 2 has Parent of Block 4 on Blockchain 2
    block5 = Block(3, '0x5100000000000000000000000000000000000000000000000000000000000000', block4.get_block_hash())
    blockchain2.blocks.append(block5)
    account1 = Account(a1, contract_instance.getBalance(a1))
    account2 = Account(a2, contract_instance.getBalance(a2))
    block5.accounts.append(account1)
    block5.accounts.append(account2)

    # Find longest chain to return to Client App due to chain re-organisation
    def get_longest_chain(chains):
        longest_length = 0
        longest_chain_id = None
        for chain_id, chain in chains.items():
            if len(chain.blocks) > longest_length:
                longest_chain_id = chain_id

        chains[longest_chain_id].is_longest = True

        # Longest blockchain with median account balance
        longest_blockchain_serialized_blocks = [b.serialize() for b in chains[longest_chain_id].blocks]

        # Re-calculate blockchain median account balance
        longest_blockchain_serialized_blocks[0]['median_account_balance'] = chains[longest_chain_id].median_account_balance()
        longest_blockchain_serialized_blocks[0]['blockchain_length'] = len(chains[longest_chain_id].blocks)
        print('Longest chain json dumps: {}'.format(json.dumps(longest_blockchain_serialized_blocks, indent=4, sort_keys=True)))

        return longest_blockchain_serialized_blocks

    blockchains = {
        "1": blockchain1,
        "2": blockchain2
    }
    longest_chain = get_longest_chain(blockchains)
    print('Longest chain: {}'.format(longest_chain))
    
    # Store in cache - http://flask.pocoo.org/docs/0.12/patterns/caching/
    get_or_set_blockchain_data('blockchain_data', longest_chain)

    print('Cached data: {}'.format(get_or_set_blockchain_data('blockchain_data', None)))

    # Clear Middleware
    web3.middleware_stack.clear()
    assert len(web3.middleware_stack) == 0

if __name__ == '__main__':
    run()
