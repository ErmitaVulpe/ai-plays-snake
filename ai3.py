import pickle
import random
import math

# ---

class neuralNetworkClass:
    def __init__(self, numberOfInputNodes: int, numberOfHiddenLayers: int, numberOfNodesPerHiddenLayer: int, numberOfOutputNodes: int) -> None:
        print("\033[32m", "-" * 20, "\n Initializing network\n", "-" * 20, "\n\033[0m")

        self.generation = 0  # Iteration of the generation
        self.score = 0       # Score used for grading the model
        self.layersList = {  # Stores the whole structure of the network except the connections
            "numberOfLayers": 0
        }

        # Input layer
        self.l0 = self.layerClass(numberOfInputNodes, "l0")
        self.layersList["l0"] = self.l0.nodeList
        self.layersList["numberOfLayers"] += 1
        
        # Hidden layers
        for i in range(1, numberOfHiddenLayers + 1):
            layerID = f"l{i}"
            setattr(self, layerID, self.layerClass(numberOfNodesPerHiddenLayer, layerID, getattr(self, f"l{self.layersList['numberOfLayers'] - 1}")))
            self.layersList[layerID] = getattr(getattr(self, layerID), "nodeList")
            self.layersList["numberOfLayers"] += 1

        # Output layers
        layerID = f"l{self.layersList['numberOfLayers']}"
        setattr(self, layerID, self.layerClass(numberOfOutputNodes, layerID, getattr(self, f"l{self.layersList['numberOfLayers'] - 1}")))
        self.layersList[layerID] = getattr(getattr(self, layerID), "nodeList")
        self.layersList["numberOfLayers"] += 1

        print("\n\033[32m", "-" * 35, "\n Successfuly initialized the network\n", "-" * 35, "\033[0m\n")
    

    def __getstate__(self): # Serialize the data
        output = {
            'generation': self.generation, 
            'layersList': self.layersList,
            'score': self.score
        }
        for key in self.layersList.keys():
            if key == "numberOfLayers": continue
            output[key] = getattr(self, key)
        return output
    
    def __setstate__(self, state) -> object: # Restore the data
        for key in state.keys():
            setattr(self, key, state[key])

    def export(self, fileName):
        """
        Export the network to a .pickle file

        Parameters: filename (str): filename
        """
        with open(fileName, 'wb') as file:
            pickle.dump(self, file)


    def compute(self, inputList):
        """
        Does the computaion of the network

        Parameters: inputList (list): List containing int or float inputs to the network. Length of inputList has to be the same number as the number of input nodes.

        Returns: list: A list containing float outputs of the network.
        """
        # Validate input
        # print("\033[32m Starting input validation \033[0m")
        if len(inputList) != len(self.layersList["l0"]["nodes"]): raise ValueError(f"\033[31m Invalid number o inputs \033[0m")
        for i in inputList:
            if not isinstance(i, (float, int)): raise ValueError(f"\033[31m Input contains a non numerical value \033[0m")
        # print("\033[32m Input successfully validated! \033[0m")

        # Assign values to the input layer
        # print("\033[32m Assigning input to the input layer \033[0m")
        for i, nodeID in enumerate(self.layersList["l0"]["nodes"]):
            getattr(self.l0, nodeID).value = inputList[i]

        # Main computing loop
        # print("\033[32m Starting the computation \033[0m")
        layersList = self.layersList.copy()
        layersList.pop("numberOfLayers")
        layersList.pop("l0")
        for layerID in list(layersList):
            for nodeID in layersList[layerID]["nodes"]:
                nodePointer = getattr(getattr(self, layerID), nodeID)
                parrentsList = nodePointer.parrentsList
                value = nodePointer.bias
                for i in list(parrentsList):
                    value += getattr(getattr(self, layerID[0] + str(int(layerID[1:]) - 1)), parrentsList[i]["ID"]).value * parrentsList[i]["weight"]
                nodePointer.value = max(math.tanh(value), 0) # rectifier
                # nodePointer.value = value
        # print("\033[32m Successfully finished the computation! \033[0m")

        # Reurning network output
        output = []
        for i in layersList[layerID]["nodes"]: output.append(getattr(getattr(self, layerID), i).value)
        return output
    
    def mutate(self):
        self.generation += 1
        layersList = self.layersList.copy()
        layersList.pop("numberOfLayers")
        layersList.pop("l0")
        for layerID in list(layersList):
            layerPointer = getattr(self, layerID)
            for nodeID in layersList[layerID]["nodes"]:
                nodePointer = getattr(layerPointer, nodeID)
                nodePointer.mutateWeights()
                nodePointer.mutateBias()

    # ---

    class layerClass: 
        def __init__(self, numberOfNodesToCreate: int, layerID: str, previousLayerPointer: object = None) -> None:
            self.ID = layerID
            self.nodeList = {
                "nextNodeID": 0,
                "nodes": []
            }
            # Creating nodes
            for i in range(numberOfNodesToCreate):
                setattr(self, f"n{i}", self.nodeClass(f"n{i}"))
                self.nodeList["nodes"].append(f"n{i}")
                self.nodeList["nextNodeID"] += 1

            # Creating connections
            if self.ID == "l0" or previousLayerPointer == None: return print(f"\033[32mSucessfully initialized input layer with {numberOfNodesToCreate} nodes\033[0m")
            nodeList = self.nodeList["nodes"].copy()
            previousNodeList = previousLayerPointer.nodeList["nodes"].copy()

            for i in list(nodeList): # iterate through nodes in currnet layer

                usedParrentNodesIndexes = [] # Make sure to not create multiple connection to the same node
                # connectionsToCreate = random.randint(math.ceil(len(previousNodeList) / 2), len(previousNodeList)) # Number of parrent nodes. from 1/2 of len(previousNodeList) to len(previousNodeList)
                connectionsToCreate = len(previousNodeList) # Number of parrent nodes. from 1/2 of len(previousNodeList) to len(previousNodeList)
                
                for j in range(connectionsToCreate):

                    # no duplicates
                    while True:
                        randomNodeFromPreviousLayerIndex = random.choice(list(previousNodeList))
                        if randomNodeFromPreviousLayerIndex not in usedParrentNodesIndexes: break
                    usedParrentNodesIndexes.append(randomNodeFromPreviousLayerIndex)

                    randomNodeFromPreviousLayerPointer = getattr(previousLayerPointer, randomNodeFromPreviousLayerIndex)
                    randomNodeFromPreviousLayerPointer.childrenList.append(i)
                    getattr(self, i).parrentsList[randomNodeFromPreviousLayerIndex] = {
                        "ID": randomNodeFromPreviousLayerIndex,
                        "weight": math.sinh(4.5 * random.uniform(-1, 1)) / 100,
                    }
            print(f"\033[32mSucessfully initialized layer with {numberOfNodesToCreate} nodes\033[0m")


        def __getstate__(self) -> object:
            output = {
                'ID': self.ID,
                'nodeList': self.nodeList
            }
            for key in self.nodeList["nodes"]:
                output[key] = getattr(self, key)
            return output

        def __setstate__(self, state) -> object:
            for key in state.keys():
                setattr(self, key, state[key])

        # ---

        class nodeClass:
            def __init__(self, nodeID: str) -> None:
                self.ID = nodeID
                self.parrentsList = {} # A nested dictionary containing: pointer, weight, and a connection id which is the index in childrenList of the parrent
                self.childrenList = []
                self.bias = math.sinh(4.5 * random.uniform(-1, 1)) / 100
                self.value = 0

            def __getstate__(self) -> object:
                return {
                    'ID': self.ID, 
                    'parrentsList': self.parrentsList, 
                    'childrenList': self.childrenList, 
                    'bias': self.bias
                }

            def __setstate__(self, state) -> object:
                for key in state.keys():
                    setattr(self, key, state[key])

            def mutateWeights(self):
                for i in list(self.parrentsList):
                    self.parrentsList[i]["weight"] += math.sinh(2 * random.uniform(-1, 1)) / 17

            def mutateBias(self):
                self.bias += math.sinh(2 * random.uniform(-1, 1)) / 17

# ---

def export(fileName, network):
    """
    Export the network to a .pickle file

    Parameters: 
        - fileName (str): filename
        - network (object): object to export
    """
    with open(fileName, 'wb') as file:
        pickle.dump(network, file)

def load(fileName):
    """
    Export the network to a .pickle file

    Parameters: fileName (str): filenamen

    Returns: obj: Object containing the network
    """
    with open(fileName, 'rb') as file:
        return pickle.load(file)

# ---

if __name__ == "__main__": 

    neuralNetwork = neuralNetworkClass(4, 5, 5, 4)
    print("\033[32m", "-" * 150, "\033[0m")
    # print(neuralNetwork.l2.n2.parrentsList)
    print(neuralNetwork.layersList)

    print(neuralNetwork.compute([1, 2, 3, 4]))
    neuralNetwork.mutate()
    print(neuralNetwork.compute([1, 2, 3, 4]))

    with open('object_file.pickle', 'wb') as file:
        pickle.dump(neuralNetwork, file)






"""
Ignore this
"""

# import pickle
# import random
# import math

# # ---

# class neuralNetworkClass:
#     def __init__(self, numberOfInputNodes: int, numberOfHiddenLayers: int, numberOfNodesPerHiddenLayer: int, numberOfOutputNodes: int) -> None:
#         print("\033[32m", "-" * 20, "\n Initializing network\n", "-" * 20, "\n\033[0m")

#         self.generation = 0  # Iteration of the generation
#         self.score = 0       # Score used for grading the model
#         self.layersList = {  # Stores the whole structure of the network except the connections
#             "numberOfLayers": 0
#         }

#         # Input layer
#         self.l0 = layerClass(numberOfInputNodes, "l0")
#         self.layersList["l0"] = self.l0.nodeList
#         self.layersList["numberOfLayers"] += 1
        
#         # Hidden layers
#         for i in range(1, numberOfHiddenLayers + 1):
#             layerID = f"l{i}"
#             setattr(self, layerID, layerClass(numberOfNodesPerHiddenLayer, layerID, getattr(self, f"l{self.layersList['numberOfLayers'] - 1}")))
#             self.layersList[layerID] = getattr(getattr(self, layerID), "nodeList")
#             self.layersList["numberOfLayers"] += 1

#         # Output layers
#         layerID = f"l{self.layersList['numberOfLayers']}"
#         setattr(self, layerID, layerClass(numberOfOutputNodes, layerID, getattr(self, f"l{self.layersList['numberOfLayers'] - 1}")))
#         self.layersList[layerID] = getattr(getattr(self, layerID), "nodeList")
#         self.layersList["numberOfLayers"] += 1

#         print("\n\033[32m", "-" * 35, "\n Successfuly initialized the network\n", "-" * 35, "\033[0m\n")
    

#     def __getstate__(self): # Serialize the data
#         output = {
#             'generation': self.generation, 
#             'score': self.score, 
#             'layersList': self.layersList
#         }
#         for key in self.layersList.keys():
#             if key == "numberOfLayers": continue
#             output[key] = getattr(self, key)
#         return output
    
#     def __setstate__(self, state) -> object: # Restore the data
#         for key in state.keys():
#             setattr(self, key, state[key])


#     def compute(self, inputList):
#         """
#         Does the computaion of the network

#         Parameters: inputList (list): List containing int or float inputs to the network. Length of inputList has to be the same number as the number of input nodes.

#         Returns: list: A list containing float outputs of the network.
#         """
#         # Validate input
#         print("\033[32m Starting input validation \033[0m")
#         if len(inputList) != len(self.layersList["l0"]["nodes"]): raise ValueError(f"\033[31m Invalid number o inputs \033[0m")
#         for i in inputList:
#             if not isinstance(i, (float, int)): raise ValueError(f"\033[31m Input contains a non numerical value \033[0m")
#         print("\033[32m Input successfully validated! \033[0m")

#         # Assign values to the input layer
#         print("\033[32m Assigning input to the input layer \033[0m")
#         for i, nodeID in enumerate(self.layersList["l0"]["nodes"]):
#             getattr(self.l0, nodeID).value = inputList[i]

#         # Main computing loop
#         print("\033[32m Starting the computation \033[0m")
#         layersList = self.layersList.copy()
#         layersList.pop("numberOfLayers")
#         layersList.pop("l0")
#         for layerID in list(layersList):
#             for nodeID in layersList[layerID]["nodes"]:
#                 nodePointer = getattr(getattr(self, layerID), nodeID)
#                 parrentsList = nodePointer.parrentsList
#                 value = nodePointer.bias
#                 for i in list(parrentsList):
#                     value += getattr(getattr(self, layerID[0] + str(int(layerID[1:]) - 1)), parrentsList[i]["ID"]).value * parrentsList[i]["weight"]
#                 nodePointer.value = max(math.tanh(value), 0) # rectifier
#         print("\033[32m Successfully finished the computation! \033[0m")

#         # Reurning network output
#         output = []
#         for i in layersList[layerID]["nodes"]: output.append(getattr(getattr(self, layerID), i).value)
#         return output
    
#     def mutate(self):
#         layersList = self.layersList.copy()
#         layersList.pop("numberOfLayers")
#         layersList.pop("l0")
#         for layerID in list(layersList):
#             layerPointer = getattr(self, layerID)
#             for nodeID in layersList[layerID]["nodes"]:
#                 getattr(layerPointer, nodeID).mutateWeights()

# # ---

# class layerClass: 
#     def __init__(self, numberOfNodesToCreate: int, layerID: str, previousLayerPointer: object = None) -> None:
#         self.ID = layerID
#         self.nodeList = {
#             "nextNodeID": 0,
#             "nodes": []
#         }
#         # Creating nodes
#         for i in range(numberOfNodesToCreate):
#             setattr(self, f"n{i}", nodeClass(f"n{i}"))
#             self.nodeList["nodes"].append(f"n{i}")
#             self.nodeList["nextNodeID"] += 1

#         # Creating connections
#         if self.ID == "l0" or previousLayerPointer == None: return print(f"\033[32mSucessfully initialized input layer with {numberOfNodesToCreate} nodes\033[0m")
#         nodeList = self.nodeList["nodes"].copy()
#         previousNodeList = previousLayerPointer.nodeList["nodes"].copy()

#         for i in list(nodeList): # iterate through nodes in currnet layer
#             usedParrentNodesIndexes = [] # Make sure to not create multiple connection to the same node
#             connectionsToCreate = random.randint(math.ceil(len(previousNodeList) / 2), len(previousNodeList)) # Number of parrent nodes. from 1/2 of len(previousNodeList) to len(previousNodeList)
#             for j in range(connectionsToCreate):

#                 # no duplicates
#                 while True:
#                     randomNodeFromPreviousLayerIndex = random.choice(list(previousNodeList))
#                     if randomNodeFromPreviousLayerIndex not in usedParrentNodesIndexes: break
#                 usedParrentNodesIndexes.append(randomNodeFromPreviousLayerIndex)

#                 randomNodeFromPreviousLayerPointer = getattr(previousLayerPointer, randomNodeFromPreviousLayerIndex)
#                 randomNodeFromPreviousLayerPointer.childrenList.append(i)
#                 getattr(self, i).parrentsList[randomNodeFromPreviousLayerIndex] = {
#                     "ID": randomNodeFromPreviousLayerIndex,
#                     "weight": math.sinh(4.5 * random.uniform(-1, 1)) / 100,
#                 }
#         print(f"\033[32mSucessfully initialized layer with {numberOfNodesToCreate} nodes\033[0m")


#     def __getstate__(self) -> object:
#         output = {
#             'ID': self.ID,
#             'nodeList': self.nodeList
#         }
#         for key in self.nodeList["nodes"]:
#             output[key] = getattr(self, key)
#         return output

#     def __setstate__(self, state) -> object:
#         for key in state.keys():
#             setattr(self, key, state[key])

# # ---

# class nodeClass:
#     def __init__(self, nodeID: str) -> None:
#         self.ID = nodeID
#         self.parrentsList = {} # A nested dictionary containing: pointer, weight, and a connection id which is the index in childrenList of the parrent
#         self.childrenList = []
#         self.bias = math.sinh(4.5 * random.uniform(-1, 1)) / 100
#         self.value = 0

#     def __getstate__(self) -> object:
#         return {
#             'ID': self.ID, 
#             'parrentsList': self.parrentsList, 
#             'childrenList': self.childrenList, 
#             'bias': self.bias
#         }

#     def __setstate__(self, state) -> object:
#         for key in state.keys():
#             setattr(self, key, state[key])

#     def mutateWeights(self):
#         for i in list(self.parrentsList):
#             self.parrentsList[i]["weight"] += math.sinh(2 * random.uniform(-1, 1)) / 20

# # ---

# if __name__ == "__main__": 

#     neuralNetwork = neuralNetworkClass(4, 5, 5, 4)
#     print("\033[32m", "-" * 150, "\033[0m")
#     # print(neuralNetwork.l2.n2.parrentsList)
#     print(neuralNetwork.layersList)

#     print(neuralNetwork.compute([1, 2, 3, 4]))
#     neuralNetwork.mutate()
#     print(neuralNetwork.compute([1, 2, 3, 4]))

#     with open('object_file.pickle', 'wb') as file:
#         pickle.dump(neuralNetwork, file)