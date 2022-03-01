import time
from hashlib import sha256
import json
import PoW
import numpy as np


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, vector=[]):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.vector = vector

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof_Vector):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        block.vector = proof_Vector

        # print(block.vector)

        block.hash = block.compute_hash()
        self.chain.append(block)
        return True

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def proofBench(self, block):        

        for x in range(700,800,10):
            for i in range(100,170,10):
                try:
                    with open("D:\\results.txt","a") as f:
                        f.write(f"{x}x{x}\n\nTime spent;n\n")
                        f.close()

                    for k in range (1):                        
                        Gen = PoW.Generate(
                            hash(sha256(json.dumps(block.__dict__, sort_keys=True).encode()).hexdigest()),i)
                        PoW.Proof(Gen,x)
                except: 
                    print("error occured")
                    continue

    def proof_of_work(self, block):


        Gen = PoW.Generate(
            hash(sha256(json.dumps(block.__dict__, sort_keys=True).encode()).hexdigest()))
        return PoW.Proof(Gen)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)



        #proof_Vector = self.proof_of_work(new_block)
        proof_Vector = self.proofBench(new_block)


        self.add_block(new_block, proof_Vector)
        self.unconfirmed_transactions = []
        return new_block.index

    def verifyLastBlock(self):
        last_block = self.last_block
        targ_magn = last_block.vector[0][0]
        B = np.array(last_block.vector[0][2])
        v = np.array(last_block.vector[1][1])
        cursiveV_check = np.array(last_block.vector[1][0])
        cursiveV = np.matmul(v, B)
        magn = np.linalg.norm(cursiveV)
        magn_check = np.linalg.norm(cursiveV_check)
        if(magn_check == magn and magn <= targ_magn):
            print("Last block is ok")
        else:
            print("Last block is corrupted")


def parseTransaction(sender, reciever, data):
    return({"name": sender, "reciever": reciever, "timestamp": time.time(), "data": data})


def main():

    blockchain = Blockchain()
    blockchain.add_new_transaction(parseTransaction("Alice", "Bob", 36))
    blockchain.add_new_transaction(parseTransaction("Bob", "Alice", 55))

    print("Mining block...")
    blockchain.mine()
    print("Verifying last block...")
    blockchain.verifyLastBlock()
    
    print("DONE, terminating")


if __name__ == "__main__":
    main()
