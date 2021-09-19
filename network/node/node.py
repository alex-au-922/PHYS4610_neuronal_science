import enum
class NodeType(enum.Enum):
    EXCITED = 1
    INHIBIT = -1
    UNCLEAR = 0

# class Node:
#     '''Implementation of Node in weighted directed graphs'''
#     # in_nodes of a Node => list of (nodes that are directed to self Node, weight)
#     # out_nodes of a Node => list of (nodes that are directed from self Node, weight)
#     def __init__(self):
#         self.in_exc_nodes = []
#         self.in_inh_nodes = []
#         self.out_exc_nodes = []
#         self.out_inh_nodes = []

#     # connect int the following way: self --(weight)--> node_j
#     def direct_to(self, node_j, weight):
#         self.out_nodes.append((node_j, weight))
#         node_j.in_nodes.append((self, weight))


# class Neuron(Node):
#     # u: Recovery variable
#     # v: Membrane potential
#     def __init__(self, u, v):
#         super().__init__()
#         self.u = u
#         self.v = v

# class ExciNeuron(Node):
#     def __init__(self, n):
#         self.neuron_type = NodeType.EXCITED
#         self.n = n

# class InhiNeuron(Node):
#     def __init__(self, n):
#         self.neuron_type = NodeType.INHIBIT
#         self.n = n



class Neuron:
    '''Implementation of Node in weighted directed graphs'''
    # in_nodes of a Node => list of (nodes that are directed to self Node, weight)
    # out_nodes of a Node => list of (nodes that are directed from self Node, weight)
    # self.in_exc_nodes = [(Node_1, 0.3), (Node_2, 0.7), (k, weight), ...)]
    # for (n, w) in node_map[i].in_exc_nodes:
    
    def __init__(self, n, nodeType):
        self.in_exc_nodes = []
        self.in_inh_nodes = []
        self.n = n
        self.type = nodeType

    # connect int the following way: self --(weight)--> node_j
    def direct_to(self, node_j, weight):
        if self.type == NodeType.EXCITED:
            node_j.in_exc_nodes.append((self.n, weight))
        if self.type == NodeType.INHIBIT:
            node_j.in_inh_nodes.append((self.n, weight))

        