from definitions import Agent
import numpy as np
from scipy.spatial import distance


class RandAgent(Agent):
    """
    This class implements an agent that explores the environmente randomly
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)

        # Get initial percepts
        self.percepts = env.initial_percepts()

        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]

        # Initializes list of visited nodes for multiple path pruning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        path = self.frontier.pop(0)

        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path}

        # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
        self.percepts = self.env.signal(action)

        # Add visited node 
        self.visited.append(path[-1])

        # From the list of viable neighbors given by the environment
        # Select a random neighbor that has not been visited yet

        viable_neighbors = self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors:
            # Select random neighbor
            visit = viable_neighbors[np.random.randint(0, len(viable_neighbors))]

            # Append neighbor to the path and add it to the frontier
            self.frontier = [path + [visit]] + self.frontier

    def run(self):
        """Keeps the agent acting until it finds the target
        """

        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])


class BFSAgent(Agent):
    """
    This class implements an agent that explores the environment through Breadth-First Search
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self, env)

        # Get initial percepts
        self.percepts = env.initial_percepts()

        # Initializes the frontier with the initial postion
        self.frontier = [[self.percepts['current_position']]]

        # Initializes list of visited nodes for multiple path pruning
        self.visited = []

    def pruning(self, neighbor, path, visited):

        """
        Implements cycle Pruning and Multiple-Path Pruning

        Args:
            neighbor: a reference to the node to be added
            path: the path to be analyzed in Cycle Pruning
            visited: a list with the visited nodes

        Returns:
            Boolean value indicating if the node is value
        """

        cycle_p = all([any(n != neighbor) for n in path])
        path_p = all([any(v != neighbor) for v in visited])

        return cycle_p and path_p


    def act(self):
        """Implements the agent action, which position visit
        """

        # Select a path from the frontier
        path = self.frontier.pop(0)

        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path}

        # The agente sends a position and the full path to the environment, the environment can plot the path in the room
        self.percepts = self.env.signal(action)

        # Add visited node
        self.visited.append(path[-1])

        viable_neighbors = self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors:
            for neighbor in viable_neighbors:

                # Performs Cycle Pruning and Multiple-Path Pruning
                if self.pruning(neighbor, path, self.visited):
                    # Append neighbor to the path and add it to the frontier
                    self.frontier = self.frontier + [path + [neighbor]]


    def run(self):
        """Keeps the agent acting until it finds the target
        """

        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])


class DFSAgent(Agent):
    """
    This class implements an agent that explores the environment through Depth-First Search
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self, env)

        # Get initial percepts
        self.percepts = env.initial_percepts()

        # Initializes the frontier with the initial postion
        self.frontier = [[self.percepts['current_position']]]

        # Initializes list of visited nodes for multiple path pruning
        self.visited = []

    def pruning(self, neighbor, path, visited):

        """
        Implements cycle Pruning and Multiple-Path Pruning

        Args:
            neighbor: a reference to the node to be added
            path: the path to be analyzed in Cycle Pruning
            visited: a list with the visited nodes

        Returns:
            Boolean value indicating if the node is value
        """

        cycle_p = all([any(n != neighbor) for n in path])
        path_p = all([any(v != neighbor) for v in visited])

        return cycle_p and path_p

    def act(self):
        """Implements the agent action, which position visit
        """

        # Select a path from the frontier
        path = self.frontier.pop(0)

        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path}

        # The agente sends a position and the full path to the environment, the environment can plot the path in the room
        self.percepts = self.env.signal(action)

        # Add visited node
        self.visited.append(path[-1])

        viable_neighbors = self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors:
            for neighbor in viable_neighbors:

                # Performs Cycle Pruning and Multiple-Path Pruning
                if self.pruning(neighbor, path, self.visited):

                    # Append neighbor to the path and add it to the frontier
                    self.frontier = [path + [neighbor]] + self.frontier



    def run(self):
        """Keeps the agent acting until it finds the target
        """

        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])


class GreedyAgent(Agent):
    """
    This class implements an agent that explores the environment through Greedy Search
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self, env)

        # Get initial percepts
        self.percepts = env.initial_percepts()

        # Initializes the frontier with the initial postion and the cost of the respective path
        self.frontier = [[[self.percepts['current_position']], 0]]

        # Initializes list of visited nodes for multiple path pruning
        self.visited = []

    def pruning(self, neighbor, path, visited):

        """
        Implements cycle Pruning and Multiple-Path Pruning

        Args:
            neighbor: a reference to the node to be added
            path: the path to be analyzed in Cycle Pruning
            visited: a list with the visited nodes

        Returns:
            Boolean value indicating if the node is value
        """

        cycle_p = all([any(n != neighbor) for n in path])
        path_p = all([any(v != neighbor) for v in visited])

        return cycle_p and path_p

    def act(self):
        """Implements the agent action
        """

        # Select a list with path and cost of the respective path from the frontier
        path_cost = self.frontier.pop(0)

        # Get the path from the list
        path = path_cost[0]

        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path}

        # The agente sends a position and the full path to the environment, the environment can plot the path in the room
        self.percepts = self.env.signal(action)

        # Add visited node
        self.visited.append(path[-1])

        viable_neighbors = self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors:
            for n in viable_neighbors:

                # Performs Cycle Pruning and Multiple-Path Pruning
                if self.pruning(n, path, self.visited):

                    # Calculate the heuristic function
                    h = distance.euclidean(n, self.percepts['target'])

                    # Append neighbor to the path and add it to the frontier
                    self.frontier = [[path + [n], h]] + self.frontier

                    # Sort the frontier according to the heuristic value
                    self.frontier.sort(key=lambda item: item[1])


    def run(self):
        """Keeps the agent acting until it finds the target
        """
        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])


class AStarAgent(Agent):
    """
    This class implements an agent that explores the environment through A* Search
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self, env)

        # Get initial percepts
        self.percepts = env.initial_percepts()

        # Initializes the frontier as a list with the initial position, the value of (h + cost) and cost
        self.frontier = [[[self.percepts['current_position']], 0, 0]]

        # Initializes list of visited nodes for multiple path pruning
        self.visited = []

    def pruning(self, neighbor, path, visited):

        """
        Implements cycle Pruning and Multiple-Path Pruning

        Args:
            neighbor: a reference to the node to be added
            path: the path to be analyzed in Cycle Pruning
            visited: a list with the visited nodes

        Returns:
            Boolean value indicating if the node is value
        """

        cycle_p = all([any(n != neighbor) for n in path])
        path_p = all([any(v != neighbor) for v in visited])

        return cycle_p and path_p

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        path_cost = self.frontier.pop(0)
        path = path_cost[0]
        cost = path_cost[2]

        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path}

        # The agente sends a position and the full path to the environment, the environment can plot the path in the room
        self.percepts = self.env.signal(action)

        # Add visited node
        self.visited.append(path[-1])

        viable_neighbors = self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors:
            for n in viable_neighbors:

                # Performs Cycle Pruning and Multiple-Path Pruning
                if self.pruning(n, path, self.visited):

                    # Calculate the heuristic function
                    h = distance.euclidean(n, self.percepts['target'])

                    # Estimates the total cost of the path from source to objective
                    f = cost + distance.euclidean(path[-1], n) + h

                    # Append path with neighbor, f and path cost to the frontier
                    self.frontier = [[path + [n], f, cost + distance.euclidean(path[-1], n)]] + self.frontier

                    # Sort the frontier according to f = h + cost
                    self.frontier.sort(key=lambda item: item[1])


    def run(self):
        """Keeps the agent acting until it finds the target
        """
        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])
