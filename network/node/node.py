import enum
class NodeType(enum.Enum):
    EXCITED = 1
    INHIBIT = -1
    UNCLEAR = 0

class Node:
    '''Implementation of Node in weighted directed graphs'''
    # in_nodes of a Node => list of (nodes that are directed to self Node, weight)
    # out_nodes of a Node => list of (nodes that are directed from self Node, weight)
    def __init__(self):
        self.in_nodes = []
        self.out_nodes = []

    # connect int the following way: self --(weight)--> node_j
    def direct_to(self, node_j, weight):
        self.out_nodes.append((node_j, weight))
        node_j.in_nodes.append((self, weight))

class Neuron(Node):
    # u: Recovery variable
    # v: Membrane potential
    def __init__(self, u, v):
        super().__init__()
        self.u = u
        self.v = v

class ExciNeuron(Neuron):
    def __init__(self, u, v):
        super().__init__(u, v)
        self.neuron_type = NodeType.EXCITE

class InhiNeuron(Neuron):
    def __init__(self, u, v):
        super().__init__(u, v)
        self.neuron_type = NodeType.INHIBIT
        