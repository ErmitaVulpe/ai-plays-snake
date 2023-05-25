import random
import math
import pickle

class NeuralNetwork:
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
        self.generation = 0

        # Define an initail structure of the network
        self.addLayer(0)
        for _ in range(input_size - 1): self.addNode("l0")
        self.addLayer(1)
        for _ in range(output_size - 1): self.addNode("l1")
        self.addConnection()

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

    # --- addNode
    
    def addNode(self, layerID: str = None):
        nodeID = f"n{self.nextNodeID}"
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
        if nodeID in self.layers["l0"] + self.layers["l1"]: return print("Cannot remove a node from input or output layer.")
        filteredLayers = [element for element in list(self.layers) if element != "l0" and element != "l1"]
        if len(filteredLayers) == 0: return print("No layers to remove nodes from")
        nodeID = random.choice(self.layers[random.choice(filteredLayers)])
        nodePointer = self.nodes[nodeID]

        for connection in nodePointer.parentsConnections + nodePointer.childrenConnections:
            self.removeConnection(connection)
        
        self.layers[nodePointer.layer].remove(nodeID)
        self.nodes.pop(nodeID)
        del nodePointer

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

        # connectionExists = False
        # if childNodeID in self.nodes[parentNodeID].childrenConnections: print("lolo")

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

        if parentNodeID == None: parentNodeID = random.choice(self.layers[parentLayerID])
        if childNodeID == None: childNodeID = random.choice(self.layers[childLayerID])

        if len(self.layers[childLayerID]) == 0: self.addNode(childLayerID) # this might be useless. TODO check later
        if len(self.layers[parentLayerID]) == 0: self.addNode(parentLayerID)

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
        # Initialize the output values of all nodes
        for node in self.nodes.values():
            node.output = 0

        # Set the input values
        for i, input_val in enumerate(inputs):
            self.nodes[i].output = input_val

        # Propagate the inputs through the network
        for layer_id in self.layers:
            for node_id in layer_id:
                node = self.nodes[node_id]
                for conn in self.connections.values():
                    if conn.to_node == node_id:
                        node.output += self.nodes[conn.from_node].output * conn.weight
                node.output = math.tanh(node.output)

        # Collect the output values
        outputs = []
        for i in range(self.input_size, self.input_size + self.output_size):
            outputs.append(self.nodes[i].output)

        return outputs
    
    # --- mutate

    def mutate(self, mutation_rate):
        for conn in self.connections.values():
            if random.random() < mutation_rate:
                conn.weight += math.sinh(2 * random.uniform(-1, 1)) / 20

# ---

class node:
    def __init__(self, layer):
        self.parentsConnections = []
        self.childrenConnections = []
        self.layer = layer
        self.bias = math.tanh(2 * random.uniform(-1, 1))


class connection:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.weight = math.tanh(2 * random.uniform(-1, 1))

# ---

# Create a neural network with 2 input nodes and 1 output node
network = NeuralNetwork(3, 4)

def printall(network):
    print(f"input_size: \n", network.input_size, "\n")
    print(f"output_size: \n", network.output_size, "\n")
    print(f"nodes: \n", network.nodes, "\n")
    print(f"nextNodeID: \n", network.nextNodeID, "\n")
    print(f"connections: \n", network.connections, "\n")
    print(f"nextConnectionID: \n", network.nextConnectionID, "\n")
    print(f"layers: \n", network.layers, "\n")
    print(f"nextLayerID: \n", network.nextLayerID, "\n")
    print(f"layerOrder: \n", network.layerOrder, "\n")
    print(f"generation: \n", network.generation, "\n")




# printall(network)
# network.addConnection(parentNodeID="n0", childNodeID="n3")
# network.addConnection(parentNodeID="n0", childNodeID="n3")
printall(network)
network.addLayer()
network.removeNode()
# network.addLayer()
# network.removoNode("n7")
# print(network.connections["c2"].parent)
# print(network.connections["c2"].child)




# # test removeConnection()
# network.addLayer()
# con = network.connections["c0"]
# parentNode = network.nodes[con.parent]
# childNode = network.nodes[con.child]
# print(parentNode.childrenConnections)
# print(childNode.parentsConnections)
# network.removeConnection("c0")
# print(parentNode.childrenConnections)
# print(childNode.parentsConnections)