from definitions import Environment
import numpy as np
import matplotlib.pyplot as plt
import copy


class Sudoku(Environment):
    '''Implements a sudoku environment

    '''
    def __init__(self, sudoku, make_arc_cosistent=True):
        ''' Class constructor

        Args:
            sudoku: A matrix representing the sudoku game
            make_arc_cosistent: A flag indicating whether the environment is acr consistent
        '''

        self.sudoku = sudoku
        self.csp = []
        self.make_arc_consistent = make_arc_cosistent

    def initial_percepts(self):

        self.ini_csp()

        if self.make_arc_consistent:
            self.apply_GAC()

        return {'is_viable': None,
                'sudoku': self.sudoku,
                'csp': self.csp}

    def signal(self, action):
        ''' Signals the current state of the problem to the agent 

        Args:
            action: Contains the position that the agent wants to change
                and the value the agent wants to put in that position
        '''

        position = action['position']
        value = action['value']

        viable = is_viable(self.sudoku, position[0], position[1], value)

        return {'is_viable': viable,
                'csp': self.csp,
                'sudoku': self.sudoku}

    def ini_csp(self):
        ''' Builds a CSP representation of the sudoku game 

        '''

        for i in range(len(self.sudoku)):
            self.csp.append([])
            for j in range(len(self.sudoku[0])):
                if self.sudoku[i][j] == 0:
                    constraints = []
                    # Cells in the same column
                    for k in range(len(self.sudoku)):
                        if i != k:
                            constraints.append(DiffConstraint([[i, j], [k, j]]))

                    # Cells in the same row
                    for k in range(len(self.sudoku[0])):
                        if j != k:
                            constraints.append(DiffConstraint([[i, j], [i, k]]))

                    # Different from other cell in the same group
                    ig = (i // 3) * 3
                    jg = (j // 3) * 3

                    for ii in range(0, 3):
                        for jj in range(0, 3):
                            if (ii + ig) != i and (jj + jg) != j:
                                constraints.append(DiffConstraint([[i, j], [(ii + ig), (jj + jg)]]))

                    self.csp[i].append(
                        {'X': [i, j], 'D': [int(n) for n in range(1, 10)], 'C': copy.deepcopy(constraints)})

                else:
                    self.csp[i].append({'X': [i, j], 'D': [self.sudoku[i][j]],
                                        'C': [EqNumConstraint([[i, j], self.sudoku[i][j]])]})

    # TODO
    def apply_GAC(self):
        to_do = []
        for row in self.csp:
            for cell in row:
                for cons in cell['C']:
                    to_do.append([cell['X'], cons])

        removed = []    
        while(to_do):
            arc = to_do.pop(0)
            removed.append(arc)

            viable = []
            cons = arc[1]
            var = arc[0]      
            var2 = cons.scope[1]

            if type(var2) != int:
                for e in self.csp[var[0]][var[1]]['D']:
                    viable = viable + [any([cons.condition(e, e2) for e2 in self.csp[var2[0]][var2[1]]['D']])]
                    
                for i, v in enumerate(viable):
                    if not v:
                        del self.csp[var[0]][var[1]]['D'][i]

                if not all(viable):
                    back = []
                    for removed_arc in removed:
                        if (var == removed_arc[1].scope[1]) and (removed_arc[1] != cons):
                            back.append(removed_arc)

                    for arc in back:
                        to_do.append(arc)
                        removed.remove(arc)


        
def is_viable(sudoku, i, j, v):
    ''' Auxiliary method that verifies whether a value, v, can be assigned to position [i,j] in the sudoku

    Args:
        sudoku: 
        i: row index
        j: column index
        v: value

    Returns:
        True if the move is viable or False, otherwise

    '''

    # Different from other cell in the same row
    for k in range(len(sudoku[0])):
        if k != j and sudoku[i][k] == v:
            return False

    # Different from other cell in the same row
    for k in range(len(sudoku)):
        if k != i and sudoku[k][j] == v:
            return False

    # Different from other cell in the same group
    ig = (i // 3) * 3
    jg = (j // 3) * 3

    for ii in range(0, 3):
        for jj in range(0, 3):
            if (ii + ig) != i and (jj + jg) != j and sudoku[ii + ig][jj + jg] == v:
                return False

    return True



class Constraint:
    ''' Defines the interface for a constraint 
    
    '''


    def __init__(self, scope, condition):
        self.scope = scope
        self.condition = condition

    def apply(self):
        raise NotImplementedError('apply')


class DiffConstraint(Constraint):
    ''' Implements a non-equality constraint 
    
    '''

    def __init__(self, scope):
        condition = lambda a, b: a != b
        Constraint.__init__(self, scope, condition)

    def __repr__(self):
        return '{} != {}'.format(self.scope[0], self.scope[1])

    def apply(self, sudoku):
        return self.condition(sudoku[self.scope[0][0]][self.scope[0][1]],
                              sudoku[self.scope[1][0]][self.scope[1][1]])


class EqNumConstraint(Constraint):
    ''' Implements a equality constraint 
    
    '''

    def __init__(self, scope):
        condition = lambda a, b: a == b
        Constraint.__init__(self, scope, condition)

    def __repr__(self):
        return '{} == {}'.format(self.scope[0], self.scope[1])

    def apply(self, sudoku):
        return self.condition(sudoku[self.scope[0][0]][self.scope[0][1]],
                              self.scope[1])


if __name__ == '__main__':
    from sudoku import Sudoku
    from sudoku_agent import SudokuAgent

    s1 = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    s2 = [[1, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 3, 0, 7, 0, 5, 0, 2, 0],
        [0, 0, 2, 0, 0, 0, 5, 0, 0],
        [0, 7, 0, 8, 0, 9, 0, 3, 0],
        [9, 0, 0, 0, 3, 0, 0, 0, 8],
        [0, 1, 0, 4, 0, 7, 0, 5, 0],
        [0, 0, 6, 0, 0, 0, 9, 0, 0],
        [0, 2, 0, 6, 0, 1, 0, 4, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 2]]

    s3 = [[0, 0, 0, 0, 9, 4, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 6, 0, 7],
        [0, 0, 4, 8, 0, 1, 0, 2, 0],
        [0, 0, 9, 0, 0, 0, 4, 0, 6],
        [4, 0, 0, 0, 2, 0, 0, 0, 1],
        [6, 0, 7, 0, 0, 0, 5, 0, 0],
        [0, 1, 0, 5, 0, 2, 7, 0, 0],
        [3, 0, 5, 0, 0, 0, 0, 0, 0],
        [0, 6, 0, 9, 3, 0, 0, 0, 0]]


    # Create an environment
    env = Sudoku(s3, True) #s1 termina com 1 valor pra cada dominio

    # Creat an agent
    ag = SudokuAgent(env, True)

    # Print CSP
    for c in ag.csp:
        for cell in c:
            print(cell['D'])

    #input('Press ENTER to start')
    ag.act()

