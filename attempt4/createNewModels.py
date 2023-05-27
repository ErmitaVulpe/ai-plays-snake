import pickle
import random
import math
import ai4

fileName = "object_file.pickle"

lolo = []
for i in range(100):
    lolo.append(ai4.neuralNetworkClass(5, 10, 10, 3))
ai4.export(fileName, lolo)