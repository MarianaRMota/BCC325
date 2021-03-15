class LogicalAgent():

    def __init__(self,KB):
        self.KB = KB

    # TODO
    def bottom_up(self):
        ''' Implements the botton up proof strategy and returns all the logical consequence odf the KB

        Returns:
            A list with all the logical consequences of KB
        '''

        C = []

        while True:
            size = len(C)
            for clause in self.KB.clauses:
                if clause.head not in C:
                    valid = [atom in C for atom in clause.body]
                    if all(valid):
                        C = [clause.head] + C

            if size == len(C):
                break
                
        return C


    # TODO
    def top_down(self,query):
        '''Implements the top down proof strategy. Given a query (the atom that it wants to prove) 
        it returns True if the query is a consequence of the knowledge base. 
        
        Args:
            querry: The atom that should be proved

        Returns: 
            True if the query is a logical consequence of KB, False otherwise

        '''

        atom = query[0]
        clauses = self.KB.clauses_for_atom(atom)

        if not clauses:
            del query[0]
            print("2 - ", query)
        else:
            for clause in clauses:         
                query = clause.body + query[1:]
                print("3 - ", query)

                if not query:
                    result = True
                    break
                if :
                    self.top_down(query)
            return result            
        
        
    # TODO
    def explain(self,g):
        '''Implements the process of abductions. It tries to explain the atoms  in the list g using
         the assumable in KB.

        Args:
            g: A set of atoms that should be explained
        
        Returns:
            A list of explanation for the atoms in g
        '''
        pass



