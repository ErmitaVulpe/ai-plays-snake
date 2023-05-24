import random
import math
import pickle

class NeuralNetwork:
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.nodes = {}
        self.nextNodeID = 0
        self.connections = {}
        self.nextConnectionID = 0
        self.layers = {}
        self.nextLayerID = 0
        self.generation = 0

        for i in range(3): self.addLayer()


    def addLayer(self):
        self.layers[f"l{self.nextLayerID}"] = []
        self.nextLayerID += 1

    
    def addNode(self, layerID: str = None):
        nodeID = f"n{self.nextNodeID}"
        self.nodes[nodeID] = node()
        if layerID == None: layerID = random.choice([element for element in list(self.layers) if element != "l0" and element != "l1"])
        self.layers[layerID].append(nodeID)
        self.nextNodeID += 1


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

    def mutate(self, mutation_rate):
        for conn in self.connections.values():
            if random.random() < mutation_rate:
                conn.weight += math.sinh(2 * random.uniform(-1, 1)) / 20

# ---

class node:
    def __init__(self):
        self.parentConnections = []
        self.childrenConnections = []
        self.biaas = math.tanh(2 * random.uniform(-1, 1))


class connection:
    def __init__(self, parent, child, weight):
        self.parent = parent
        self.child = child
        self.weight = weight

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
    print(f"generation: \n", network.generation, "\n")

# network.addLayer()
network.addNode()
network.addNode()
network.addNode()
network.addNode()
network.addNode("l0")
printall(network)