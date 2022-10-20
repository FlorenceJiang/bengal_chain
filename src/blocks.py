import json
from datetime import datetime


CODE_FORMAT = 'utf-8'


class Block:
    '''
    Each block contains: prev_hash, transactions, timestamp, hash, nonce.
    In practice, the transactions could be any type of transactions structure, here the structure is defined by Transaction. replace it with whatever u want.
    '''
    def __init__(self, transactions, prev_hash):
        self.prev_hash = prev_hash
        self.transactions = transactions # a list of transactions
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.nonce = None
        self.hash = None

    def __repr__(self):
        return f'[block info] content: {self.transactions}; hash: {self.hash}'


class BlockChain:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def __repr__(self):
        print(f'[blockchain info] total blocks in the chain: {len(self.blocks)}')
        for block in self.blocks:
            print(f'[blockchain info] prev hash: {block.prev_hash}')
            print(f'[blockchain info] data: {block.data}')
            print(f'[blockchain info] hash: {block.hash}')
            print('[blockchain info] \n')

    def get_balance(self, user):
        """
        giving the chain, compute any user's balance by looping through all transactions on the block.
        """
        balance = 0
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.sender == user.address.decode():
                    balance -= transaction.amount
                elif transaction.recipient == user.address.decode():
                    balance += transaction.amount
        return balance


class Transaction:
    """
    write a class to define the structures of encoded data.
    You could defined however you wish.
    """
    def __init__(self, sender, recipient, amount):
        if isinstance(sender, bytes):
            sender = sender.decode(CODE_FORMAT)

        if isinstance(recipient, bytes):
            recipient = recipient.decode(CODE_FORMAT)

        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def set_sign(self, signature, pubkey):
        """
        to verify the transaction, give source of transactions: access to senders" pubkey and signature.
        """
        self.signature = signature
        self.pubkey = pubkey

    def __repr__(self):
        """
        2 types of transactions:
        1) from mining: senders is none
        2) from transfer: sender is not none
        """
        source = self.sender if self.sender else 'mining'
        return f"source: {source}, recipient: {self.recipient}, amount: {self.amount}"


class TransactionEncoder(json.JSONEncoder):
    """
    to serialize transactions.
    """
    def default(self, obj):
        if isinstance(obj, Transaction):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)
