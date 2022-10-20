from src.concensus import ProofOfWork
from src.blocks import Block, BlockChain, Transaction
from src.wallet import Wallet, verify_sign


if __name__ == '__main__':

    my_chain = BlockChain()

    usr1 = Wallet()
    usr2 = Wallet()
    usr3 = Wallet()

    print(f"current balances:")
    print(f"user1: {my_chain.get_balance(usr1)}")
    print(f"user2: {my_chain.get_balance(usr2)}")
    print(f"user3: {my_chain.get_balance(usr3)}")

    genesis_block = Block(transactions=[], prev_hash='')

    print('usr1 mine the genesis_block...')
    w0 = ProofOfWork(genesis_block, usr1)
    valid_genesis_block = w0.mine()
    my_chain.add_block(valid_genesis_block)
    print(f"user1 balance: {my_chain.get_balance(usr1)}")

    print('usr1 transfer x amount to usr2...')
    transactions = []
    new_transaction = Transaction(
        sender=usr1.address,
        recipient=usr2.address,
        amount=0.3
    )
    sig = usr2.sign(str(new_transaction))
    new_transaction.set_sign(sig, usr2.pubkey)

    print('usr3 trying to mine this transaction between usr1 and usr2...')
    if verify_sign(new_transaction.pubkey, str(new_transaction), new_transaction.signature):
        print('validation succeeded!')
        # adding the new block
        new_block = Block(transactions=[new_transaction], prev_hash='')
        w2 = ProofOfWork(new_block, usr3)
        new_block_validated = w2.mine()
        my_chain.add_block(new_block_validated)
    else:
        print('validation failed!')

    print(f"current balances:")
    print(f"user1: {my_chain.get_balance(usr1)}")
    print(f"user2: {my_chain.get_balance(usr2)}")
    print(f"user3: {my_chain.get_balance(usr3)}")
