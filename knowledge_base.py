class Askable():
    ''' Implements the askable type
    '''

    def __init__(self,atom):
        self.atom = atom
  
    def __str__(self):
        return 'askable ' + self.atom + '.'


class Clause():
    ''' Implements a representation of definite clauses
    '''
  
    def __init__(self,head,body=[]):
        self.head = head
        self.body = body
    
    def __str__(self):
        if self.body:
            return self.head + ' <- ' + ' & '.join(self.body) + '.'
        else:
            return self.head + '.'

class Assumable():
    ''' Implements the representation for a assumable 
    '''

    def __init__(self,atom):
        self.atom = atom

    def __str__(self):
        return 'assumable ' + self.atom + '.'

class KB():
    ''' Implements a representation for a knowlwdge base
    '''
  
    def __init__(self, statements = []):
        ''' Class constructor

        Args:
            statements: a list of statements
        '''
        self.statements = statements

        # Splits the list of statements into clauses and askables
        self.clauses = [c for c in self.statements if isinstance(c,Clause)]
        self.askables = [a for a in self.statements if isinstance(a,Askable)]
        
        # Create a map from atoms to clauses
        # I.e, for a given atom, store the clause that have that atom as thei head
        self.c_for_a = {}
        for c in self.clauses:
            if c.head in self.c_for_a:
                self.c_for_a[c.head].append(c)
            else:
                self.c_for_a[c.head] = [c]
  
    def clauses_for_atom(self,atom):
        ''' Retrieves that clauses the have a given atom as head
        
        Args: 
            atom

        Returns:
            clauses tha have 'atom' as head
        '''
        
        if atom in self.c_for_a:
            return self.c_for_a[atom]
        else:
          return set()
    
    def __str__(self):
        ''' String representation for the class
        '''
        return '\n'.join([str(c) for c in self.statements])

class KBA(KB):
    ''' Implements a representation for a knowledge base that handles assumables
    '''

    def __init__(self, statements):
        self.assumables = [a.atom for a in statements if isinstance(a,Assumable)]
        KB.__init__(self,statements)