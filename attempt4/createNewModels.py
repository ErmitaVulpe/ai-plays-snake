import ai4

fileName = "trainingModels.pickle"

lolo = []
for i in range(100):
    lolo.append(ai4.neuralNetwork(72, 4))
ai4.export(fileName, lolo)