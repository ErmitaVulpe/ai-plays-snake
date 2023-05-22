import pickle
import random
import math


class neuralNetworkClass:
    def __init__(self, numberOfInputNodes: int, numberOfHiddenLayers: int, numberOfNodesPerHiddenLayer: int, numberOfOutputNodes: int) -> None:
        self.generation = 0  # Iteration of the generation
        self.score = 0       # Score used for grading the model
        self.layersList = [] # List of all the layers in a network, ordered from input to output

        self.layersList.append(layerClass(numberOfInputNodes))
        for _ in range(numberOfHiddenLayers): 
            self.layersList.append(layerClass(numberOfNodesPerHiddenLayer, self.layersList[-1]))
            print(f"\033[32mSucessfully created a hidden layer. ID: {len(self.layersList)}\033[0m")
        self.layersList.append(layerClass(numberOfOutputNodes, self.layersList[-1]))

    def __getstate__(self): # Serialize the data
        return {
            'generation': self.generation, 
            'score': self.score, 
            'layersList': self.layersList
        }
    
    def __setstate__(self, state) -> object: # Restore the data
        self.generation = state['generation']
        self.score      = state['score']
        self.layersList = state['layersList']

# ---

class layerClass: 
    def __init__(self, numberOfNodesToCreate: int, previousLayerPointer: object = None) -> None:
        self.nodeID = 0    # The id that each new node gets assigned
        self.nodeList = {} # To avoid possible duplcating ids after some nodes get deleted, every new node gets assigned a new id

        for _ in range(numberOfNodesToCreate):
            self.nodeList[self.nodeID] = nodeClass()
            self.nodeID += 1
        if previousLayerPointer == None: return
        
        previousLayerNodeList = previousLayerPointer.nodeList
        for i in list(self.nodeList):
            usedParrentNodesIndexes = []
            connectionsToCreate = random.randint(math.ceil(len(previousLayerNodeList) / 2), len(previousLayerNodeList))
            for j in range(connectionsToCreate):
                randomNodeFromPreviousLayerIndex = random.randint(0, len(previousLayerNodeList) - 1)
                while randomNodeFromPreviousLayerIndex in usedParrentNodesIndexes: randomNodeFromPreviousLayerIndex = random.randint(0, len(previousLayerNodeList) - 1) # no duplicates
                usedParrentNodesIndexes.append(randomNodeFromPreviousLayerIndex)

                parrentNodePointer = previousLayerNodeList[randomNodeFromPreviousLayerIndex]
                connectionID = len(parrentNodePointer.childrenList)

                parrentNodePointer.childrenList.append(self.nodeList[i])

                self.nodeList[i].parrentsList.append({
                    "pointer": parrentNodePointer,
                    "weight": math.sinh(4.5 * random.uniform(-1, 1)) / 100,
                    "connectionID": connectionID
                })

    def __getstate__(self) -> object:
        return {
            'nodeID': self.nodeID, 
            'nodeList': self.nodeList, 
        }

    def __setstate__(self, state) -> object:
        self.nodeID     = state['nodeID']
        self.nodeList   = state['nodeList']

# ---

class nodeClass:
    def __init__(self) -> None:
        self.parrentsList = [] # A list with a dictionary inside containing: pointer, weight, and a connection id which is the index in childrenList of the parrent
        self.childrenList = []
        self.bias = 0
        self.value = 0

    def __getstate__(self) -> object:
        return {
            'parrentsList': self.parrentsList, 
            'childrenList': self.childrenList, 
            'bias': self.bias, 
            'value': self.value, 
        }

    def __setstate__(self, state) -> object:
        self.parrentsList   = state['parrentsList']
        self.childrenList   = state['childrenList']
        self.bias           = state['bias']
        self.value          = state['value']

# ---

neuralNetwork = neuralNetworkClass(4805, 200, 100, 50)



with open('object_file.pickle', 'wb') as file:
    pickle.dump(neuralNetwork, file)