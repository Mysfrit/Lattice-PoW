import multiprocessing
import string
from sys import getsizeof
import numpy as np
from Crypto.Util import number
from sympy import re, true
from alphaMatrix import Alpha_matrix, Alpha_vector, Mega_vector
import time
import random
from random import randrange
from decimal import *
from TargetMagn import targMagnDict
from multiprocessing import Process, Array, Value, Pipe
import time


global n, n_for_prime, prime, returnVal
n = 40
n_for_prime = 40
prime = 0
singleTread = True


def BenchmarkVecGen():
    start1 = time.time()
    for i in range(100000):
        GenerateVector()
    # print(time.time()-start1)

    start1 = time.time()
    for i in range(100000):
        GenerateVector2()
    # print(time.time()-start1)


def GenerateVector(rangeVec, n):
    return np.random.randint(-rangeVec, rangeVec, n)


def GenerateVector2():
    array = []
    for i in range(n):
        array.append(random.randint(-500, 500))
    return np.array(array)


def Generate(randomness, size=0):

    if size != 0:
        global n, n_for_prime
        n = size
        n_for_prime = size

    #print("size of matrix: ",n)
    # generate prime
    # npr.seed(randomness%2**32)

    prime = number.getPrime(10*n_for_prime)
    #print("Prime: ", prime)

    uniform_Dist = np.zeros((n), dtype=object)

    # uniform Dist
    for i in range(n):
        uniform_Dist[i] = randrange(prime)

    # B Matrix
    # generation zeroes
    B = np.zeros(shape=(n, n), dtype=object)
    for i in range(n):
        B[i, i] = 1

    # put vars into B
    B[0, 0] = prime
    for i in range(1, n):
        B[0, i] = uniform_Dist[i-1]

    # Alpha Matrix
    return (Alpha_vector, n, B, prime)


def Proof(Gen, vecSize):
    # Parsing Gen
    # BenchmarkVecGen()
    Alpha_vector = Gen[0]
    #n = Gen[1]
    B = Gen[2]
    global prime, singleTread
    prime = Gen[3]

    # Setting target
    global n

    if n not in targMagnDict:
        targetMagn = targMagnDict[n+1]

    else:
        targetMagn = targMagnDict[n]
    if not singleTread:
        threads = [None]*5

        parent_conn, child_conn = Pipe()
        for i in range(len(threads)):

            threads[i] = Process(target=findSolution, args=(
                n, B, targetMagn, vecSize, child_conn,))
            threads[i].daemon = True

        for k in range(len(threads)):
            threads[k].start()

        while(True):
            recv = parent_conn.recv()
            while(parent_conn.poll()):
                parent_conn.recv()
            parent_conn.close()

            print(f"THREAD {j} found solution")
            # print(threads[j].join())
            for j in range(len(threads)):
                threads[j].terminate()

            with open("D:\\results.txt", "a") as f:
                # f.write(f"{parent_conn[0]};{parent_conn[1]}\n")

                #f.write(str(recv))
                f.write(recv[0]+";"+n)
                f.close()
            del threads
            return (recv[1:3])
    else:
        child_conn = None
        result = findSolution(n, B, targetMagn, vecSize, child_conn,)
        with open("D:\\results.txt", "a") as f:
                f.write(f"{str(result[2])};{str(n)}")
                f.close()
        return result


def findSolution(n, B_, targetMagn, vecSize, retArr, ):

    start = time.time()
    counter = 0
    # print(n)
    while True:
        counter += 1
        v = GenerateVector(vecSize, n)
        cursiveV = np.matmul(v, B_, dtype=object)
        magn = np.linalg.norm(cursiveV,)

        if counter % 15000 == 0:
            print("Tries per second", counter/(time.time()-start))
            print(magn)

        if(magn <= targetMagn and magn != 0):
            print("SOLUTION", cursiveV)
            print("Time elapsed: ", time.time()-start)
            print("Target magnitude: ", targetMagn)
            print("Magn found: ", magn)
            c_ = (int(magn), n, B_.tolist(), prime)
            T_ = (cursiveV.tolist(), v.tolist())
            #print("Failed attempts: ", counter)
            if not singleTread:

                retArr.send([time.time()-start, n, c_, T_])
                retArr.close()

            return (c_, T_, time.time()-start)
