from datetime import datetime


class Block:
    '''
    contains: prev_hash, data, timestamp, hash, nonce
    '''
    def __init__(self, data, prev_hash):
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.nonce = None
        self.hash = None

    def __repr__(self):
        return f'block content: {self.data}; block hash: {self.hash}'


class BlockChain:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)
