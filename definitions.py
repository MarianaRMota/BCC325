class Agent:
    """
        This class implements an interface for an agent.
    """
    def __init__(self, env):
        '''
        Constructor for the agent class.

        Args:
            env: a reference to the environment.
        '''

        self.env = env

    def act(self):
        '''
        Defines the agent action.

        Raises:
            NotImplementedError: If the method is not implemented or not overridden.
        '''

        raise NotImplementedError('act')


class Environment:
    """
        This class implements and interface for an Environment
    """

    def initial_percepts(self):
        '''
        Returns the initial percepts.

        Raises:
            NotImplementedError: if the method is not implemented or not overridden.
        '''

        raise NotImplementedError('initial_percepts')

    def signal(self, action):
        '''
        Returns the environment percepts after action is executed.

        Raises:
            NotImplementedError: If the method is not implemented or not overridden.
        '''

        raise NotImplementedError('signal')

