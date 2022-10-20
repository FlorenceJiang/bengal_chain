import hashlib
import json

from .blocks import Block, Transaction, TransactionEncoder
from .wallet import Wallet
from .utilites import timeit


CODE_FORMAT = "utf-8"


class ProofOfWork:
    def __init__(self, block: Block, miner: Wallet, difficult=5, reward_amount=0.1):
        self.block = block
        self.miner = miner
        self.difficulty = difficult
        self.reward_amount = reward_amount  # default, very simple, each mining gets one coin.

    @timeit
    def mine(self):
        i = 0
        prefix = "0" * self.difficulty

        # add reward to miner
        t = Transaction(
            sender="",
            recipient=self.miner.address,
            amount=self.reward_amount,
        )
        sig = self.miner.sign(json.dumps(t, cls=TransactionEncoder))
        t.set_sign(sig, self.miner.pubkey)
        self.block.transactions.append(t)

        while True:
            msg = hashlib.sha256()
            msg.update(str(self.block.prev_hash).encode(CODE_FORMAT))
            msg.update(str(self.block.timestamp).encode(CODE_FORMAT))
            msg.update(str(i).encode(CODE_FORMAT))

            # update transaction data in the block
            # msg.update(str(self.block.data).encode(CODE_FORMAT)) # use this line unless TransactionType is used.
            msg.update(str(self.block.transactions).encode(CODE_FORMAT))

            digest = msg.hexdigest()
            if digest.startswith(prefix):
                self.block.nonce = i
                self.block.hash = digest
                return self.block
            i += 1

    @timeit
    def validate(self):
        msg = hashlib.sha256()

        # update transaction data in the block
        # msg.update(str(self.block.data).encode(CODE_FORMAT)) # use this line unless TransactionType is used.
        msg.update(str(json.dumps(self.block.transactions)).encode(CODE_FORMAT))
        msg.update(str(self.block.prev_hash).encode(CODE_FORMAT))
        msg.update(str(self.block.timestamp).encode(CODE_FORMAT))
        msg.update(str(self.block.nonce).encode(CODE_FORMAT))

        digest = msg.hexdigest()

        prefix = "0" * self.difficulty # default is 5, meaning the valid hash start w 5*'0'
        return digest.startswith(prefix)