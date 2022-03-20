class Node:
    """a node represents a position on the quoridor board"""
    def __init__(self, key: tuple):
        self.key: tuple = key
        self.connected_to = set()

    def __str__(self):
        return f"{self.key} connected to:  {[node.key for node in self.connected_to]}"

    def add_connected_node(self, connected_node):
        self.connected_to.add(connected_node)

    def delete_connected_node(self, connected_node):
        self.connected_to.remove(connected_node)


class Graph:
    """
    the graph is the internal representation of the board,
    it is used to perform queries like is connected to and shortest path faster
    """

    def __init__(self):
        self.nodes = dict()

    def add_node(self, key):
        if key not in self.nodes:
            self.nodes[key] = Node(key)

    def add_edge(self, node1: tuple, node2: tuple):
        """"edge can only be added if both nodes exist"""
        if node1 not in self.nodes:
            return
        if node2 not in self.nodes:
            return
        self.nodes[node1].add_connected_node(self.nodes[node2])
        self.nodes[node2].add_connected_node(self.nodes[node1])

    def remove_edge(self, node1: tuple, node2: tuple):
        self.nodes[node1].delete_connected_node(self.nodes[node2])
        self.nodes[node2].delete_connected_node(self.nodes[node1])

    def is_connected(self, pos, goal_side) -> bool:
        pass

    def shortest_path(self, pos, goal_side):
        pass

# g = Graph()
# g.add_node((0, 0))
# g.add_edge((0, 0), (0, 1))
# for node in g.nodes.values():
#     print(node)
# g.remove_edge((0,0), (0,1))
# for node in g.nodes.values():
#     print(node)
