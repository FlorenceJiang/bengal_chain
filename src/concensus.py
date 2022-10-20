import hashlib
from datetime import datetime
from functools import wraps


CODE_FORMAT = 'utf-8'


def timeit(func):
    """
    decorator to measure execution time for PoW.
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = datetime.now()
        res = func(*args, **kwargs)
        print(f'excution time of {func.__name__} is {datetime.now() - start_time}')
        return res
    return timeit_wrapper


class ProofOfWork:
    '''
    concensus for bitcoin
    '''
    def __init__(self, block, difficult=5):
        self.block = block
        self.difficulty = difficult

    @timeit
    def mine(self):
        i = 0
        prefix = '0' * self.difficulty

        while True:
            msg = hashlib.sha256()
            msg.update(str(self.block.prev_hash).encode(CODE_FORMAT))
            msg.update(str(self.block.data).encode(CODE_FORMAT))
            msg.update(str(self.block.timestamp).encode(CODE_FORMAT))
            msg.update(str(i).encode(CODE_FORMAT))
            digest = msg.hexdigest()
            if digest.startswith(prefix):
                self.block.nonce = i
                self.block.hash = digest
                return self.block
            i += 1

    @timeit
    def validate(self):
        msg = hashlib.sha256()
        msg.update(str(self.block.prev_hash).encode(CODE_FORMAT))
        msg.update(str(self.block.data).encode(CODE_FORMAT))
        msg.update(str(self.block.timestamp).encode(CODE_FORMAT))
        msg.update(str(i).encode(CODE_FORMAT))
        digest = msg.hexdigest()

        prefix = '0' * self.difficulty
        return digest.startswith(prefix)