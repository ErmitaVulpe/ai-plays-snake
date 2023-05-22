import pickle
import random
import math
import ai3

fileName = "object_file.pickle"

lolo = []
for i in range(100):
    lolo.append(ai3.neuralNetworkClass(5, 10, 10, 3))
ai3.export(fileName, lolo)


# network = ai3.load(fileName)[0]
# print(network.l2.n2.parrentsList)