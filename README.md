# Lattice-Based Proof-of-Work for Post-Quantum Blockchains

## Required libraries
- numpy - `pip install numpy`

## Files
- PoW.py
    - GenerateVector()
        - Generate a random vector with the size of n
    - Generate(randomness)
        - Generates prime and matrix B for a given block
    - Proof(Gen)
        - Parses generated values and tries to find a vector of a given magnitude, after finding it, it will be returned
- Blockchain.py
    - Class `Block` with attribues
    - Class `Blockchain` with attribues
        - Generating genesis block
        - adding block to the chain
        - adding transactions 
        - Proof of work
        - Mining a given block
        - Verifinyg last block

## Running
- The program is ran by blockchain.py without any arguments.