from wallet import Wallet
from concensus import ProofOfWork
from blocks import Block, BlockChain


if __name__ == '__main__':

    my_chain = BlockChain()

    genesis_block = Block(data='this is bengal genesis block', prev_hash='')
    w = ProofOfWork(genesis_block)
    valid_genesis_block = w.mine()
    my_chain.add_block(valid_genesis_block)

    prev_block = genesis_block
    block_size = 5
    for i in range(block_size):
        cur_block = Block(data=f'this is bengal {i+1} block', prev_hash=prev_block.hash)
        w = ProofOfWork(cur_block)
        valid_cur_block = w.mine()
        my_chain.add_block(valid_cur_block)
        prev_block = valid_cur_block

    print(f'total blocks in the chain: {len(my_chain.blocks)}')
    for block in my_chain.blocks:
        print(f'prev hash: {block.prev_hash}')
        print(f'data: {block.data}')
        print(f'hash: {block.hash}')
        print('\n')
