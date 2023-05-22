import pickle
import random
import math

modelsFile = "models.picke"
bestModelFile = "best_model.pickle"

class neuralNetworkInator:
    score = 0
    generation = 0

    class layerInator:
        numberOfNodes = 0

        class nodeInator:
            def __init__(self, parrents=[], bias=0, value=0):
                self.parrents = parrents
                self.bias = bias
                self.value = value

        def __init__(self, numberOfInputNodes: int = 0, numberOfOutputNodes: int = 0, type="hidden"):
            self.type = type
            match type:
                case "input":
                    self.numberOfNodes = numberOfInputNodes
                    for i in range(self.numberOfNodes):
                        setattr(self, f"inputLayer_{i}", self.nodeInator(parrents=None))
                case "output":
                    self.numberOfNodes = numberOfOutputNodes
                    for i in range(self.numberOfNodes):
                        setattr(self, f"outputLayer_{i}", self.nodeInator())

    def __init__(self, numberOfInputNodes: int, numberOfOutputNodes: int, numberOfHiddenLayers: int):
        self.inputLayer = self.layerInator(numberOfInputNodes=numberOfInputNodes, type="input")
        self.outputLayer = self.layerInator(numberOfOutputNodes=numberOfOutputNodes, type="output")
        self.numberOfHiddenLayers = numberOfHiddenLayers
        for i in range(numberOfHiddenLayers): setattr(self, f"hiddenLayer{i}", self.layerInator())
        # self.hiddenLayer0 = self.layerInator()


    def mutate(self, level: int=1):
        """
        Randomly sligthly alter the network.

        Parameters:
            - level (int): 1 - 100. Choose how much the network gets mutated

        Returns: None
        """
        if level < 1 or level > 100: raise ValueError("Mutation level out of range. Try 1 - 100")

        def mutation():
            layerIndex = random.randint(0, self.numberOfHiddenLayers - 1)
            layerPointer = getattr(self, f"hiddenLayer{layerIndex}")
            nodePointer = None if layerPointer.numberOfNodes == 0 else getattr(layerPointer, f"node_{random.randint(0, layerPointer.numberOfNodes - 1)}")
            previousLayerNodesList = []
            if layerIndex == 0:
                previousLayerPointer = self.inputLayer
                for i in range(previousLayerPointer.numberOfNodes): previousLayerNodesList.append(getattr(previousLayerPointer, f"inputLayer_{i}"))
            else:
                previousLayerPointer = getattr(self, f"hiddenLayer{layerIndex}")
                for i in range(getattr(previousLayerPointer, "numberOfNodes")): previousLayerNodesList.append(f"hiddenLayer_{i}")

            def createNode(layerPointer: object = None):
                """
                Creates a node in any existing HIDDEN layer.
                """
                if layerPointer == None: return print('\033[31m' + "Tried to create a node without specifiyng the layer. Skipping mutation" + '\033[0m')

                newNode = layerPointer.nodeInator()
                setattr(layerPointer, f"node_{layerPointer.numberOfNodes}", newNode)
                layerPointer.numberOfNodes += 1

                print(f"\033[32mSucessfully created a new node at {newNode} in layer at {layerPointer}\033[0m")

            def addConnection(layerPointer: object, previousLayerNodesList: object, nodePointer: object = None):
                """
                Adds a connection between a node and a parrent node
                """
                if nodePointer == None:
                    if layerPointer.numberOfNodes == 0: return print('\033[31m' + "Tried to create a connection for a layer without any nodes. Skipping mutation" + '\033[0m')
                    nodePointer = getattr(layerPointer, f"node_{random.randint(0, layerPointer.numberOfNodes - 1)}")
                
                randomParrentNodePointer = random.choice(previousLayerNodesList)
                nodePointer.parrents.append({"pointer": randomParrentNodePointer, "weight": 0.0})

                print(f"\033[32mSucessfully created a connection from {nodePointer} to a parrent at {randomParrentNodePointer}\033[0m")

            def modifyParrentWeigth(nodePointer: object):
                """
                Modifies weigth inside an existing parrent connection  
                """
                if nodePointer == None: return print('\033[31m' + "Tried to modify a connection without specifying a node. Skipping mutation" + '\033[0m')
                numberOfConnections = len(nodePointer.parrents)
                if numberOfConnections == 0: return print('\033[31m' + f"Tried to modify a connection but a node at {nodePointer} doesn't have any connections" + '\033[0m')

                weightChange = math.sinh(4.5 * random.uniform(-1, 1)) / 100
                nodePointer.parrents[random.randint(0, numberOfConnections - 1)]["weight"] += weightChange

                print(f"\033[32mSucessfully adjusted weight for a connection of node {nodePointer} by {weightChange}\033[0m")


            mutationFloat = random.uniform(0, 100)
            if      mutationFloat < 70: modifyParrentWeigth(nodePointer)
            elif    mutationFloat < 80: addConnection(layerPointer=layerPointer, previousLayerNodesList=previousLayerNodesList, nodePointer=nodePointer)
            elif    mutationFloat < 81: createNode(layerPointer=layerPointer)
            
            # TODO remove a node, remove a connection, add a layer, remove a layer


        for _ in range(level * 1000):
            mutation()

    def compute(headDrection: str, bodyList: list, foodPos: list) -> str:
        """
        This is the actual method that makes the predictions.

        Parameters:
            - headdDrection (str): up, rigth, down or left.
            - bodyList (list): Nested list with coordinates of each body part of the snake. The first one has to be the head of the snake.
            - foodPos (list): List of coordinates of the food.

        Returns:
            str: A string containing the way for the snake to turn.
        """
        


neuralNetwork = neuralNetworkInator(numberOfInputNodes=60 * 40 * 2 + 5, numberOfOutputNodes=4, numberOfHiddenLayers=10)
neuralNetwork.mutate(10)
# print(neuralNetwork.hiddenLayer0.node_0)
# print(neuralNetwork.hiddenLayer0.node_0.parrents)


with open('object_file.pickle', 'wb') as file:
    pickle.dump(neuralNetwork, file)

"""
# # Define your object
class dupa:
    key = "value"
# my_object = dupa()
# # my_object = {'key': 'value'}
# print(my_object.key)

# # Export the object to a file
# with open('object_file.pickle', 'wb') as file:
#     pickle.dump(my_object, file)



# Load the object from the file
with open('object_file.pickle', 'rb') as file:
    loaded_object = pickle.load(file)

# Now you can work with the loaded object
print(loaded_object.key)  # Output: {'key': 'value'}

"""