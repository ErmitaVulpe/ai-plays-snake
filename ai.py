import pickle
import random

modelsFile = "models.picke"
bestModelFile = "best_model.pickle"

class neuralNetworkInator:
    score = 0
    generation = 0
    NumberOfHiddenLayers = 1

    class layerInator:
        NumberOfNodes = 0

        class nodeInator:
            def __init__(self, parrent=None, bias=0, value=0):
                self.parrent = parrent
                self.bias = bias
                self.value = value

        def __init__(self, type="hidden"):
            self.type = type
            match type:
                case "input":
                    self.NumberOfNodes = 4805
                    for i in range(self.NumberOfNodes): # grid size: 60 x 40 so 2400 tiles (times 2) plus 5
                        setattr(self, f"inputLayer_{i}", self.nodeInator())
                case "output":
                    self.NumberOfNodes = 4
                    for i in range(self.NumberOfNodes):
                        setattr(self, f"outputLayer_{i}", self.nodeInator())

    def __init__(self):
        self.inputLayer = self.layerInator(type="input")
        self.outputLayer = self.layerInator(type="output")
        self.hiddenLayer0 = self.layerInator()

    def mutate(self, level: int=1):
        """
        Randomly sligthly alter the network.

        Parameters:
            - level (int): 1 - 5. Choose how much the network gets mutated

        Returns: None
        """
        def createNode():
            """
            Creates a node in any existing HIDDEN layer.
            """
            layer = random.randint(0, self.NumberOfHiddenLayers - 1)
            layerPointer = self.inputLayer
            previousLayerNodesList = []
            if layer == 0:
                previousLayerPointer = self.inputLayer
                for i in range(layerPointer.NumberOfNodes): previousLayerNodesList.append(f"inputLayer_{i}")
            else:
                previousLayerPointer = getattr(self, f"hiddenLayer{layer}")
                for i in range(getattr(previousLayerPointer, "NumberOfNodes")): previousLayerNodesList.append(f"hiddenLayer_{i}")
                # LATER CHECK IF previousLayerPointer IS NEEDED ------------------------------------------------------------------------------------------------------------

        for _ in range(level):
            createNode()


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
        


neuralNetwork = neuralNetworkInator()
print(neuralNetwork.outputLayer.outputLayer_3)
neuralNetwork.mutate()





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