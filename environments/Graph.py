from collections import deque


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

    def is_reachable(self, pos, goal_side) -> bool:
        """checks if a goal side is reachable for player given the position of the player"""

        # Mark all the vertices as not visited
        visited = set()

        # Create a queue for BFS
        queue = deque([])

        # Mark the source node as visited and enqueue it
        queue.append(self.nodes[pos])
        visited.add(pos)

        while queue:

            # Dequeue a vertex from queue
            node = queue.pop()

            # If this adjacent node is the destination node,
            # then return true
            if node.key[0] == goal_side:
                return True

            #  Else, continue to do BFS
            for node in self.nodes[node.key].connected_to:
                if node not in visited:
                    queue.append(node)
                    visited.add(node)
        # If BFS is complete without visited d
        return False

    def shortest_path(self, pos, goal_side):
        pass
