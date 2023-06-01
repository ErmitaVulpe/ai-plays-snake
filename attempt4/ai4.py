import random
import math
import pickle
# from numba import jit
# @jit(target_backend='cuda')


class neuralNetwork:
    def __init__(self, input_size: int, output_size: int):
        self.input_size = input_size
        self.output_size = output_size
        self.nodes = {}
        self.nextNodeID = 0
        self.connections = {}
        self.nextConnectionID = 0
        self.layers = {}
        self.nextLayerID = 0
        self.layerOrder = []
        self.score = 0
        self.generation = 0

        # Define an initail structure of the network
        self.addLayer(0)
        for _ in range(input_size - 1): self.addNode("l0")
        self.addLayer(1)
        for _ in range(output_size - 1): self.addNode("l1")
        self.addConnection()

    def printall(self):
        print(f"input_size: \n", self.input_size, "\n")
        print(f"output_size: \n", self.output_size, "\n")
        print(f"nodes: \n", self.nodes, "\n")
        print(f"nextNodeID: \n", self.nextNodeID, "\n")
        print(f"connections: \n", self.connections, "\n")
        print(f"nextConnectionID: \n", self.nextConnectionID, "\n")
        print(f"layers: \n", self.layers, "\n")
        print(f"nextLayerID: \n", self.nextLayerID, "\n")
        print(f"layerOrder: \n", self.layerOrder, "\n")
        print(f"generation: \n", self.generation, "\n")

    # --- addLayer

    def addLayer(self, layerIndex: int = -1):
        """
        parameters:
            layerIndex - index of the new layer
        """
        match len(self.layerOrder):
            case 0: layerIndex = 0
            case 1: layerIndex = 1
            case _:
                if layerIndex < 0 or layerIndex > len(self.layers): layerIndex = random.randint(1, len(self.layerOrder) - 1)
        self.layerOrder.insert(layerIndex, f"l{self.nextLayerID}")
        self.layers[f"l{self.nextLayerID}"] = []
        self.addNode(f"l{self.nextLayerID}")
        self.nextLayerID += 1

    # --- removeLayer

    def removeLayer(self, layerIndex: int = None):
        if layerIndex == "l0" or layerIndex == "l1": return print(f"(-) Cannot remove {layerIndex}")
        if layerIndex == None:
            filteredLayers = [element for element in list(self.layers) if element != "l0" and element != "l1"]
            if len(filteredLayers) == 0: return print("(-) No layers to remove.")
            layerIndex = random.choice(filteredLayers)
        if layerIndex not in self.layers: return print("(-) Cannot remove a non-existing layer.")

        for node in self.layers[layerIndex]:
            self.removeNode(node)
        if layerIndex in self.layers: self.layers.pop(layerIndex)
        if layerIndex in self.layerOrder: self.layerOrder.remove(layerIndex)

    # --- addNode
    
    def addNode(self, layerID: str = None):
        nodeID = f"n{self.nextNodeID}"
        if layerID not in self.layers: return print("(-) invalid layer to add a node to")
        if layerID == None: 
            filteredLayers = [element for element in list(self.layers) if element != "l0" and element != "l1"]
            if len(filteredLayers) < 3: return self.addLayer()
            layerID = random.choice(filteredLayers)
        self.nodes[nodeID] = node(layerID)
        self.layers[layerID].append(nodeID)
        if layerID != "l0" and layerID != "l1": 
            self.addConnection(childNodeID=nodeID) # Node becomes a child
            self.addConnection(parentNodeID=nodeID) # Node becomes a parent
        self.nextNodeID += 1

    # --- removeNode
    
    def removeNode(self, nodeID: str = None):
        if nodeID in self.layers["l0"] + self.layers["l1"]: return print("(-) Cannot remove a node from input or output layer.")
        filteredLayers = [element for element in list(self.layers) if element != "l0" and element != "l1"]
        if len(filteredLayers) == 0: return print("(-) No layers to remove nodes from")
        nodeID = random.choice(self.layers[random.choice(filteredLayers)])
        nodePointer = self.nodes[nodeID]

        for connection in nodePointer.parentsConnections + nodePointer.childrenConnections:
            self.removeConnection(connection)
        
        layer = nodePointer.layer
        self.layers[layer].remove(nodeID)
        self.nodes.pop(nodeID)
        del nodePointer

        if len(self.layers[layer]) == 0: self.removeLayer(layer)

    # --- addConnection

    def addConnection(self, parentNodeID: str = None, childNodeID: str = None, parentLayerID: str = None, childLayerID: str = None):
        preferedParentLayerID = (parentLayerID if parentNodeID == None else self.nodes[parentNodeID].layer)
        preferedChildLayerID = (childLayerID if childNodeID == None else self.nodes[childNodeID].layer)
        # I took a lot of single brain cell processing power to end up with this decision tree for filling in missing data
        # The parent part
        if parentNodeID == None:
            if parentLayerID != None: parentNodeID = random.choice(self.layers[parentLayerID])
            else: parentLayerID = random.choice(self.layerOrder[:1])
        else: parentLayerID = self.nodes[parentNodeID].layer
        # The child part
        if childNodeID == None:
            if childLayerID != None: childNodeID = random.choice(self.layers[childLayerID])
            else: childLayerID = random.choice(self.layerOrder[1:])
        else: childLayerID = self.nodes[childNodeID].layer

        # 3 diffrent loops for performance sake. Computational efficiency wise it's better to have an if statement that executes once than every loop iteration
        if preferedParentLayerID != None:
            while self.layerOrder.index(parentLayerID) >= self.layerOrder.index(childLayerID):
                childLayerID = random.choice(self.layerOrder[1:])
        elif preferedChildLayerID != None:
            while self.layerOrder.index(parentLayerID) >= self.layerOrder.index(childLayerID):
                parentLayerID = random.choice(self.layerOrder[:1])
        else:
            while self.layerOrder.index(parentLayerID) >= self.layerOrder.index(childLayerID):
                parentLayerID = random.choice(self.layerOrder[:1])
                childLayerID = random.choice(self.layerOrder[1:])

        if len(self.layers[parentLayerID]) == 0: return print("(-) Parent layer is empty")
        if len(self.layers[childLayerID]) == 0: return print("(-) Child layer is empty")
        if parentNodeID == None: parentNodeID = random.choice(self.layers[parentLayerID])
        if childNodeID == None: childNodeID = random.choice(self.layers[childLayerID])

        if len(self.layers[childLayerID]) == 0: self.addNode(childLayerID) # this might be useless. TODO check later
        if len(self.layers[parentLayerID]) == 0: self.addNode(parentLayerID)

        for connectionID in self.nodes[parentNodeID].childrenConnections:
            if self.connections[connectionID].child == childNodeID: return "Such a connection already exists."

        connectionID = f"c{self.nextConnectionID}"
        self.connections[connectionID] = connection(parentNodeID, childNodeID)
        self.nodes[parentNodeID].childrenConnections.append(connectionID)
        self.nodes[childNodeID].parentsConnections.append(connectionID)
        self.nextConnectionID += 1

    # --- removeConnection

    def removeConnection(self, connectionID: str = None):
        if len(self.connections) == 0: return 1
        if connectionID == None: connectionID = random.choice(list(self.connections))
        connectionPointer = self.connections[connectionID]

        self.nodes[connectionPointer.parent].childrenConnections.remove(connectionID)
        self.nodes[connectionPointer.child].parentsConnections.remove(connectionID)
        self.connections.pop(connectionID)
        del connectionPointer

    # --- forward propagation 

    def forward(self, inputs):
        # @jit(target_backend='cuda')
        def matrixMultiplication(list1: list, list2: list):
            if len(list1) != len(list2): return print("Bruh")
            output = 0
            for i in range(len(list1)):
                output += list1[i] * list2[i]
            return output


        if len(inputs) != self.input_size: raise ValueError(f"\033[31m Invalid number o inputs \033[0m")
        for i in inputs:
            if not isinstance(i, (float, int)): raise ValueError(f"\033[31m Input contains a non numerical value \033[0m")

        for index, nodeID in enumerate(self.layers["l0"]):
            self.nodes[nodeID].value = inputs[index]

        for layerID in self.layerOrder:
            for nodeID in self.layers[layerID]:
                weights = []
                values = []
                for connectionID in self.nodes[nodeID].parentsConnections:
                    # value += self.nodes[self.connections[connectionID].parent].value * self.connections[connectionID].weight
                    weights.append(self.connections[connectionID].weight)
                    values.append(self.nodes[self.connections[connectionID].parent].value)
                value = matrixMultiplication(weights, values)
                value += self.nodes[nodeID].bias
                self.nodes[nodeID].value = max(math.tanh(2 * value), 0)

        output = []
        for nodeID in self.layers[self.layerOrder[-1]]:
            output.append(self.nodes[nodeID].value)
        return output

    
    # --- mutations

    def mutate(self):
        addLayerChance = 0.075
        removeLayerChance = 0.05
        addNodeChance = 0.10
        removeNodeChance = 0.075
        addConnectionChance = 0.33
        removeConnectionChance = 0.10
        metateWeightChance = 0.75
        metateBiasChance = 0.75

        if random.random() < addLayerChance: self.addLayer()
        if random.random() < removeLayerChance: self.removeLayer()

        for layer in [element for element in list(self.layers) if element != "l0" and element != "l1"]:
            if random.random() < addNodeChance: self.addNode(layer)
            if random.random() < removeNodeChance: self.removeNode(layer)

        for node in list(self.nodes):
            # if random.random() < addConnectionChance: self.addConnection(parentNodeID=node)
            # if random.random() < addConnectionChance: self.addConnection(childNodeID=node)
            if random.random() < addConnectionChance: self.addConnection()
            if random.random() < metateBiasChance: self.mutateBias(node)

        for connection in list(self.connections):
            if random.random() < metateWeightChance: self.mutateWeight(connection)
            if random.random() < removeConnectionChance: self.removeConnection(connection)

        self.generation += 1

    
    def mutateWeight(self, connectionID: str = None):
        if connectionID == None: connectionID = random.choice(self.connections)
        self.connections[connectionID].weight += math.sinh(2 * random.uniform(-1, 1)) / 30

    def mutateBias(self, nodeID: str = None):
        if nodeID == None: nodeID = random.choice(self.nodes)
        self.nodes[nodeID].bias += math.sinh(2 * random.uniform(-1, 1)) / 30

# ---

class node:
    def __init__(self, layer):
        self.parentsConnections = []
        self.childrenConnections = []
        self.layer = layer
        self.bias = math.tanh(2 * random.uniform(-1, 1))
        self.value = 0


class connection:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.weight = math.tanh(2 * random.uniform(-1, 1))

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
