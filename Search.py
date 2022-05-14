import time

from heapq import *

from Board import Board

UNIFORM_COST = 0
A_STAR = 1

MISPLACED_TILE = 0
MANHATTAN_DISTANCE = 1


class Search(object):
    """
    Class for finding a solution to a provided 8-Puzzle using search.
    """
    def __init__(self, algorithm, heuristic, initial_state):
        if algorithm != A_STAR and algorithm != UNIFORM_COST:
            exit(-1)
        if algorithm == A_STAR and \
                (heuristic != MANHATTAN_DISTANCE and heuristic != MISPLACED_TILE):
            exit(-1)
        self.algorithm = algorithm
        self.heuristic = heuristic
        self.initial_state = initial_state
        self.max_queue_size = 0
        self.depth = 0
        self.count_nodes_expanded = 0
        self.start_time = 0
        self.end_time = 0

    def get_heuristic_cost(self, node):
        """
        Return the heuristic cost of a node based on the type
        of heuristic expected.

        :param node: Node for which heuristic is required
        :return: Cost of the heuristic
        """
        if node is None:
            return 0

        # Calculate heuristic based on option provided.
        heuristic_cost = 0
        if self.heuristic == MANHATTAN_DISTANCE:
            heuristic_cost = node.manhattan_distance()
        elif self.heuristic == MISPLACED_TILE:
            heuristic_cost = node.misplaced_tile()

        return heuristic_cost

    @staticmethod
    def expand(board, visited):
        """
        Function to expand a particular board.

        :param board: The board to expand.
        :param visited: The set of visited states.
        :return: The set of expanded states.
        """
        return board.generate_children(visited)

    def uc_search(self):
        """
        Perform Uniform Cost Search.

        :return: The final node if solution found. Otherwise, None.
        """
        nodes = []
        visited = set()

        # Push the first node into the heap.
        heappush(nodes, (0, Board(self.initial_state, None)))

        while len(nodes) > 0:

            # Pop the cheapest node
            (cost, b) = heappop(nodes)

            # Test for goal state
            if b.is_final_state():
                return b

            # Add the node to the visited state
            visited.add(b)

            # Generate more nodes
            children = Search.expand(b, visited)

            # Update count of nodes expanded
            self.count_nodes_expanded = self.count_nodes_expanded + 1

            # Start adding to the heap
            for child in children:
                heappush(nodes, (1 + cost, child))

            # Update the max queue size
            if len(nodes) > self.max_queue_size:
                self.max_queue_size = len(nodes)

        # No solution, return.
        return None

    def astar_search(self):
        """
        Perform A*.

        :return: The final node if solution found. Otherwise, None.
        """
        nodes = []
        board_start = Board(self.initial_state, None)
        g_x = dict()
        g_x[board_start] = 0
        visited = set()

        # Push the first node into the heap.
        heappush(nodes, (0, board_start))

        # While there are still nodes in the set
        while len(nodes) > 0:

            # Pop the cheapest node
            (cost, b) = heappop(nodes)

            # If solution reached, return
            if b.is_final_state():
                return b

            # Generate more nodes
            children = Search.expand(b, None)

            # Update count of nodes expanded
            self.count_nodes_expanded = self.count_nodes_expanded + 1

            # Start adding to the heap
            for child in children:

                # Add nodes based on g_x
                # If this is
                child_g_x = 1 + g_x[b]
                if child not in g_x.keys():
                    g_x[child] = 100000000

                # If going through the current node provides a better cost,
                # take it.
                if child_g_x < g_x[child]:

                    # Update the child's g(x)
                    g_x[child] = child_g_x

                    # Get the heuristic cost based on
                    h_x = self.get_heuristic_cost(child)

                    # f(x) = h(x) + g(x)
                    child_total_cost = h_x + g_x[child]

                    # Insert into the nodes set iff a child
                    # with updated cost does not exist.
                    n = (child_total_cost, child)
                    if n not in visited:
                        heappush(nodes, (child_total_cost, child))
                        visited.add(n)

            # Update the max queue size
            if len(nodes) > self.max_queue_size:
                self.max_queue_size = len(nodes)

        # No solution, return.
        return None

    def print_search_stats(self, node):
        """
        Print the statistics of the search performed.

        :return: Nothing.
        """
        if node is None:
            print("8-Puzzle provided is not solvable.")
            print("Number of nodes expanded: {0}".format(self.count_nodes_expanded))
            print("Max queue size: {0}".format(self.max_queue_size))
            print("Time taken: {0:.2f}".format(self.end_time - self.start_time))
            return

        self.depth = Board.get_cost(node.parent)
        print("Solution depth was: {0}".format(self.depth))
        print("Number of nodes expanded: {0}".format(self.count_nodes_expanded))
        print("Max queue size: {0}".format(self.max_queue_size))
        print("Time taken: {0:.2f} seconds".format(self.end_time - self.start_time))

    def search(self):
        """
        Perform search and print statistics.

        :return: Return final goal node.
        """
        self.max_queue_size = 0
        self.depth = 0
        self.count_nodes_expanded = 0
        self.start_time = 0
        self.end_time = 0

        final_node = None
        if self.algorithm == UNIFORM_COST:
            self.start_time = time.time()
            final_node = self.uc_search()
            self.end_time = time.time()
        elif self.algorithm == A_STAR:
            self.start_time = time.time()
            final_node = self.astar_search()
            self.end_time = time.time()

        self.print_search_stats(final_node)

        return final_node
