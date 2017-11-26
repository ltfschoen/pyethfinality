# Reference: https://gist.github.com/heikoheiko/a84b05c78d2971c26f2d3e3c49ec8d83
# Converted to Python 3 by Luke Schoen

import collections
import random
import json
import hashlib
import math


def hexhash(x):
    """
    Account address for given index

    :param x:int
    :return: address:string
    """

    # References:
    # - https://docs.python.org/3/library/hashlib.html
    hash_str = str(x)
    # encode the Unicode string into Bytes
    hash_bytes = hash_str.encode('utf-8')
    # Constructor for secure hash algorithm SHA224
    hash_sha = hashlib.sha224(hash_bytes)
    # Request digest concatenation of input strings fed so far
    hash_sha_digest = hash_sha.hexdigest()[:6]
    # print('hash sha224 digest: {}'.format(hash_sha.hexdigest()))
    address = '0x' + hash_sha_digest
    return address


TransferEvent = collections.namedtuple('TransferEvent', 'sender, receiver, amount')


class Accounts(object):
    """
    Generate accounts instances
    """

    initial_supply = 0

    def __init__(self, num_accounts=0, copy_from=None):
        self.balances = dict()
        if copy_from:
            self.balances = copy_from.balances.copy()
        else:
            self._gen_accounts(num_accounts)
        self.initial_supply = self.supply

    def _gen_accounts(self, num):
        for i in range(num):
            k = hexhash(i)
            v = random.randint(1, 100)
            self.balances[k] = v

    @property
    def supply(self):
        return sum(self.balances.values())

    def median(self):
        """
        Median of the list of values stored in balances hash

        Reference: https://docs.python.org/3/howto/sorting.html
        i.e. balances = [1,5,3,7,6,7] # => [1, 3, 5, 6, 7, 7]
             sorted(balances)[int(len(balances)/2)] # => 6
        """
        return sorted(self.balances.values())[len(self.balances) / 2]

    def transfer(self, sender, receiver, amount):
        # Transfer an amount from a sender account to a receiver account
        self.balances[sender] -= amount
        self.balances[receiver] += amount
        assert self.supply == self.initial_supply

    def random_transfer(self):
        """
        Generate a valid random transfer by:
        - Choosing a random sender and receiver.
        - Sending a random proportion of the senders balance to the receiver.
        """
        while True:
            sender = random.choice(list(self.balances.keys()))
            if not self.balances[sender]:
                continue
            receiver = random.choice(list(self.balances.keys()))
            if sender == receiver:
                continue
            amount = random.randint(1, self.balances[sender])
            self.transfer(sender, receiver, amount)
            return TransferEvent(sender, receiver, amount)


class Block(object):

    def __init__(self, prevblock=None, num_accounts=0):
        if not prevblock:  # genesis block
            self.accounts = Accounts(num_accounts=num_accounts)
            self.prevhash = hexhash(-1)
            self.number = 0
        else:
            self.accounts = Accounts(copy_from=prevblock.accounts)
            self.number = prevblock.number + 1
            self.prevhash = prevblock.hash
        self.transfers = []
        self.prevblock = prevblock

    def copy_transfers(self, other, fraction=0.5):
        assert isinstance(other, Block)
        for t in other.transfers[:int(len(other.transfers) * fraction)]:
            self.transfers.append(t)
            self.accounts.transfer(t.sender, t.receiver, t.amount)

    @property
    def hash(self):
        return hexhash(repr(self.__dict__))

    def random_transfers(self, num):
        for i in range(num):
            self.transfers.append(self.accounts.random_transfer())

    def serialize(self, include_balances=False):
        s = dict(number=self.number,
                 hash=self.hash,
                 prevhash=self.prevhash,
                 transfers=[dict(x._asdict()) for x in self.transfers]
                 )
        if include_balances or self.number == 0:
            s['balances'] = self.accounts.balances
        return s


def gen_chain(max_height, p_revert, num_accounts, max_transfers):
    head = Block(num_accounts=num_accounts)
    chain = [head]
    while head.number < max_height:
        if head.number > 0 and random.random() < p_revert:
            head = head.prevblock
        else:
            head = Block(prevblock=head)
            # check if there is a sibling (same block height)
            if len(chain) > 2 and chain[-2].number == head.number:
                sibling = chain[-2]
                # include some of its txs
                head.copy_transfers(sibling, 0.5)
                head.random_transfers(random.randint(0, math.ceil(max_transfers / 2)))
            else:
                head.random_transfers(random.randint(0, max_transfers))
            chain.append(head)
    return chain


def longest_revert(chain):
    highest_chain = 0
    longest_revert = 0
    for block in chain:
        highest_chain = max(highest_chain, block.number)
        longest_revert = max(longest_revert, highest_chain - block.number)
    return longest_revert


def run():
    """
    Generate a blockchain with:
    - height - Max. amount of blocks
    - p_revert - Probability of the state of the head of the blockchain reverting 
      to a previous block based on quantity of block confirmations until finalised 
      and the value of the transaction 
    - num_accounts - Amount of Accounts to generate in the block
    - max_transfers - Amount of transfers allowed between accounts
    """

    random.seed(43)
    # chain = gen_chain(max_height=10, p_revert=0.5, num_accounts=100, max_transfers=10)
    chain = gen_chain(max_height=3, p_revert=0.6, num_accounts=2, max_transfers=1)
    serialized_blocks = [b.serialize(include_balances=True) for b in chain]
    # random.shuffle(serialized_blocks)
    print('json dumps: {}'.format(json.dumps(serialized_blocks, indent=4, sort_keys=True)))
    print('blocks: {} max reverted:{}'.format(len(chain), longest_revert(chain)))

    txs = []
    for block in set(chain):
        txs.extend(block.transfers)
    print('total transfers:{} unique transfers:{}'.format(len(txs), len(set(txs))))

if __name__ == '__main__':
    run()