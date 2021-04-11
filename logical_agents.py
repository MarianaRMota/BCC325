from knowledge_base import *

class LogicalAgent():

    def __init__(self,KB):
        self.KB = KB
        self.askable_atoms = [a.atom for a in KB.askables] 
          

    def bottom_up(self):
        ''' Implements the botton up proof strategy and returns all the logical consequence odf the KB

        Returns:
            A list with all the logical consequences of KB
        '''

        C = []

        while True:
            size = len(C)
            for s in self.KB.statements:

                if isinstance(s, Clause):
                    if s.head not in C:
                        valid = [atom in C for atom in s.body]
                        if all(valid):
                            C = [s.head] + C

                if isinstance(s, Askable):
                    if s.atom not in C:
                        ask = input('\nAtom {} is True or False? (T or F)'.format(s.atom))
                        if ask == "T":
                            C = [s.atom] + C

            if size == len(C):
                break
                
        return C 



    def top_down(self,query):
        '''Implements the top down proof strategy. Given a query (the atom that it wants to prove) 
        it returns True if the query is a consequence of the knowledge base. 
        
        Args:
            querry: The atom that should be proved

        Returns: 
            True if the query is a logical consequence of KB, False otherwise

        '''

        if query:
            atom = query[0]

            if atom in [a.atom for a in self.KB.statements if isinstance(a,Askable)]:
                ask = input('\nAtom {} is True or False? (T or F)'.format(atom))
                if ask == "T":
                    query = query[1:]
                    if query:
                        atom = query[0]
                    else:
                        return True
                    #print(query)

            clauses = self.KB.clauses_for_atom(atom)
            found = False

            if not clauses:
                del query[0]

            else:
                for clause in clauses:
                        query = clause.body + query[1:]
                        #print(query)
                        found = self.top_down(query)
                        if found:
                            return found

            return found
        else:
            return True
        

    # TODO
    def explain(self,g, explanation = set()):
        '''Implements the process of abductions. It tries to explain the atoms  in the list g using
         the assumable in KB.

        Args:
            g: A set of atoms that should be explained
        
        Returns:
            A list of explanation for the atoms in g
        '''

        if g:
            selected = g[0]

            if selected in self.askable_atoms:
                if ask_askable(selected):
                    return self.explain(g[1:], explanation)
                else:
                    return []

            if selected in self.KB.assumables:
                return self.explain(g[1:], explanation|{selected})
            else:
                l = []
                for clause in self.KB.clauses_for_atom(selected):
                    l = l + self.explain(clause.body + g[1:], explanation)

                return l

        else:
            return [explanation]
        

def yes(ans):
    """ Returns true if answer is yes
    """

    return ans.lower() in ['sim', 's', 'yes', 'y']

def ask_askable(atom):
    """ Asks if an atom is true or false
    """
    return yes(input('Is {} true? '.format(atom)))