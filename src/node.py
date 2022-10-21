import hashlib
import socket
import threading
import pickle

from .blocks import CODE_FORMAT, Block, BlockChain, Transaction
from .wallet import Wallet, verify_sign
from .concensus import ProofOfWork


NODE_LST = []
DIFFICULTY = 5
PER_BYTE = 64


class Node(threading.Thread):
    """
    A decentralized network is made of nodes.
    In this implementation, each node takes a thread.
    A node can send the following request:
    1. get a blockchain copy
    2. verify transaction and add it as a new block
    3. verify block and add it as a new block
    """
    def __init__(self, name, port, host='localhost'):
        threading.Thread.__init__(self, name=name)
        self.host = host
        self.port = port
        self.name = name # unique
        self.wallet = Wallet()
        self.blockchain = None # save a blockchain copy. When the chain is too big, size will be a problem.

    def run(self):

        self.init_blockchain()

        # listening at the node
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.bind((self.host, self.port))
        NODE_LST.append(
            {
                "name": self.name,
                "host": self.host,
                "port": self.port,
            }
        )
        my_socket.listen(10) # prepare the server for incoming client request
        print(self.name, 'Node running...')
        while True:
            connection, addr = my_socket.accept()
            try:
                print(self.name, 'Processing request...')
                self.handle_request(connection)
            except my_socket.timeout:
                print('Connection time out!')
            except Exception as e:
                print(e, )
            connection.close()

    def handle_request(self, connection):
        """
        3 request types:
        1. request reporting a new transaction. need to 1) verify if the transaction is valid 2) append the transaction as a new block to the chain.
        2. request reporting a new block. need to 1) verify if the block is valid 2) append the block to the chain
        3. request reporting INIT blockchain. need to send back the current blockchain copy.
        """
        data = []
        while True:
            buffer = connection.recv(PER_BYTE) # receive max byte until the end of msg.
            if not buffer:
                break
            data.append(buffer)
            if len(buffer) < PER_BYTE: # if butter is leq than PER_BYTE, means data is complete. break
                break

        data = pickle.loads(b''.join(data))

        if isinstance(data, Transaction):
            print('Processing new transaction request...')
            if verify_sign(data.pubkey, str(data), data.signature):
                print(f"{self.name} transaction validation succeeded!")
                new_block = Block(transactions=[data], prev_hash="")
                w = ProofOfWork(new_block, self.wallet)
                valid_new_block = w.mine()
                self.blockchain.add_block(valid_new_block)
                self.broadcast_new_block(valid_new_block)
            else:
                print(f"{self.name} transaction validation failed!")

        elif isinstance(data, Block):
            print('Processing new block request...')
            if self.verify_block(data):
                print(f"{self.name} block validation succeeded!")
                self.blockchain.add_block(data)
            else:
                print(f"{self.name} block validation failed!")

        else: # INIT reqeust
            print("Request is neither new transaction or block, return blockchain info")
            connection.send(pickle.dumps(self.blockchain))

    def verify_block(self, block):
        msg = hashlib.sha256()
        msg.update(str(block.prev_hash).encode(CODE_FORMAT))
        msg.update(str(block.timestamp).encode(CODE_FORMAT))
        msg.update(str(block.nonce).encode(CODE_FORMAT))
        msg.update(str(block.transactions).encode(CODE_FORMAT))

        digest = msg.hexdigest()
        prefix = '0' * DIFFICULTY
        return digest.startswith(prefix)

    def broadcast_new_block(self, block):
        """
        update blockchain to very node.
        """
        for node in NODE_LST:
            host = node['host']
            port = node['port']
            if host==self.host and port==self.port: # the node is self.
                return
            print(f"broadcasting to node {self.name}")
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.connect((host, port))
            my_socket.send(pickle.dumps(block))
            my_socket.close()

    def init_blockchain(self):
        """
        check if there are other nodes in the network.
        1. if is the first node, create genesis block
        2. if is not the first node, copy blockchain to the cur node.
        """
        if not NODE_LST:
            genesis_block = Block(transactions=[], prev_hash="")
            w = ProofOfWork(genesis_block, self.wallet)
            valid_genesis_block = w.mine()
            self.blockchain = BlockChain()
            self.blockchain.add_block(valid_genesis_block)
            print('Genesis block created!')

        else:
            any_node = NODE_LST[0] # could be anynode, not just the first. cuz every node should have the same blockchain.
            host = any_node['host']
            port = any_node['port']
            name = any_node['name']
            print(f"{self.name} sends init request to {name}")
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.connect((host, port))
            my_socket.send(pickle.dumps('INIT')) # Request is neither new transaction or block, so the socket will return blockchain copy.
            data = []
            while True:
                buffer = my_socket.recv(PER_BYTE)
                if not buffer:
                    break
                data.append(buffer)
                if len(buffer) < PER_BYTE:
                    break
            my_socket.close()

            # update blockchain using the newly received copy.
            self.blockchain = pickle.loads(b''.join(data))
            print(f"{self.name} initialization succeeded!")

    def submit_transaction(self, transaction):
        """
        A node could also submit a transaction and broadcast the transaction.
        """
        for node in NODE_LST:
            host = node['host']
            port = node['port']
            if host==self.host and port==self.port:
                print("ignore itself")
            else:
                print(f"broadcasting to node {self.name}")
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                my_socket.connect((host, port))
                my_socket.send(pickle.dumps(transaction))
                my_socket.close()

    def get_balance(self):
        balance = 0
        for block in self.blockchain.blocks:
            for t in block.transactions:
                if t.sender == self.wallet.address.decode():
                    balance -= t.amount
                elif t.recipient == self.wallet.address.decode():
                    balance += t.amount
        print(f"balance: {balance}")

    def print_blockchain(self):
        print(f"number of blocks: {len(self.blockchain.blocks)}")
        for block in self.blockchain.blocks:
            print(f"prev_hash: {block.prev_hash}")
            print(f"content:{block.transactions}")
            print(f"hash: {block.hash}")
            print("\n")


# # Sample codes to test the nodes
# # run the codes in jupyter notebook
# node1 = Node('node1', 8000)
# node1.start() # thread start()

# node1.print_blockchain()
# node2 = Node("node2", 8001)
# node2.start()
# node2.print_blockchain()

# node1.get_balance()
# node2.get_balance()

# print("node1 sends node2 0.3 coins...")
# new_transaction = Transaction(
# sender=node1.wallet.address,
# recipient=node2.wallet.address,
# amount=0.3
# )
# sig = node1.wallet.sign(str(new_transaction))
# new_transaction.set_sign(sig, node1.wallet.pubkey)

# node1.submit_transaction(new_transaction)

# node1.print_blockchain()
# node2.print_blockchain()

# node1.get_balance()
# node2.get_balance()