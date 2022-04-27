from matplotlib.font_manager import list_fonts
import sympy.logic.boolalg as boolalg
from sympy.logic.boolalg import And, Not, Or, Xor
import copy

# binary counter
def binary_counter(n : int):
    """
    Input: n - number.
    
    Return: Returns a list of integers representing the binary 
    representation of n with little-endian notation (If I remember correctly).
    
    Example: binary_counter(5) returns [2, 0]
    """
    count = list(str(bin(n)[2:])[::-1])
    counter = 0
    output = []
    for i,c in enumerate(count):
        if (c == "1"):
            output.append(i)
        counter += 1
    output.sort(reverse=True)
    return output

class Clause:
    """
    Representation of a clause.
    """
    def __init__(self, clause : str, order : int, isString=True):
        """
        Input: clause - clause as string. order - int representing the clause importance.
        """
        self.list_of_literals = []
        self.order = copy.copy(order)

        if(isString):
            new_clause = copy.copy(clause)
            new_clause = new_clause.replace(" ", "")
            new_clause = new_clause.replace("(", "")
            new_clause = new_clause.replace(")", "")
            list_of_beliefs = new_clause.split("|")
            for belief in list_of_beliefs:
                self.list_of_literals.append(Literal(belief, self.order, self))
        elif(isString == False):
            for l in clause:
                self.list_of_literals.append(l)

    # Returns a sorted string of all the literals in the clause (Used for comparing if two clauses are equivalent).
    def sorted_string(self):
        sorted_list = sorted(self.list_of_literals)
        sorted_list_str = ""
        for l in sorted_list:
            sorted_list_str += l.value
        return sorted_list_str
    
    # Used for debug purposes.
    def debug_print(self, res_ret=False):
        output = "[DEBUG CLAUSE]:"
        for l in self.list_of_literals:
            output += " " + l.value
        if(not res_ret):
            print(output)
        else:
            return output

    # Overwritten equality operator. Allows comparison of two clauses based on their order number.
    def __eq__(self, other):
        return self.order == other.order

    # Overwritten less-than operator. Allows comparison of two clauses based on their order number.
    def __lt__(self, other):
        return self.order < other.order

class Literal:
    """
    Representation of a literal.
    """
    def __init__(self, literal, order, parent):
        """
        Input: literal - string representing the literal, order - int representing the literal importance.
        """
        self.value = literal
        self.parent = parent
        self.order = order

    # Overwritten equality operator. Allows comparison of two literals based on their value.
    # Used in the clause class sorted_string method.
    def __eq__(self, other):
        return self.value == other.value

    # Overwritten less-than operator. Allows comparison of two literals based on their value.
    # Used in the clause class sorted_string method.
    def __lt__(self, other):
        return self.value < other.value

def get_literals(clause):
    clause = clause.replace(" ", "")
    clause = clause.replace("(", "")
    clause = clause.replace(")", "")
    clause = clause.split("|")
    return clause


def pl_resolution2(kb_input, a):
    """
    Input: Kb - Knowledge base or Belief base, a - question.
    Output: True or False, based on if the question is true or false with the given knowledge.
    The function uses a brute force resolution method to proove if the question is true or false.
    """
    a = str(Not(a))
    a = str(boolalg.to_cnf(a))
    a = a.split(" & ")
    kb = copy.deepcopy(kb_input)
    for c in a:
        kb.append(Clause(c, -1))
    
    is_not_done = True
    # Make all possible combinations of clauses where literals are subtracted
    while is_not_done:
        is_not_done = False

        for i,ci in enumerate(kb):
            for j,cj in enumerate(kb):
                if (i != j):

                    # Looking at the literals in each clause to determine if they cancel out.
                    for k,li in enumerate(ci.list_of_literals):
                        for l,lj in enumerate(cj.list_of_literals):
                            # Check for contradiction.
                            # Example: If a literal 'A' exists and a ~'A' literal exist. Then this statement is true
                            if (str(Not(li.value)) == lj.value):
                                copy_of_ci = copy.deepcopy(ci)
                                copy_of_cj = copy.deepcopy(cj)
                                del copy_of_ci.list_of_literals[k]
                                del copy_of_cj.list_of_literals[l]

                                # If ci and cj are empty, we have a contradiction.
                                if (len(copy_of_ci.list_of_literals) == 0 and len(copy_of_cj.list_of_literals) == 0):
                                    return True

                                # Otherwise add it to the kb.
                                new_clause = copy_of_ci.list_of_literals + copy_of_cj.list_of_literals
                                new_clause = Clause(new_clause, -1, False)
                                
                                # Check if clause already exists
                                doesnt_exist = True
                                for c in kb:
                                    if (new_clause.sorted_string() == c.sorted_string()):
                                        doesnt_exist = False
                                        break
                                if (doesnt_exist):
                                    kb.append(new_clause)
                                    is_not_done = True

    # No more clauses was addded in the last run and no contradictions were found, hence we are done.
    return False

# Easy solution - Delete the whole clause that contains outdated information
def revision(kb_input, a):
    """
    Input: Kb - Knowledge base or Belief base, a - question.

    Output: List of clauses that needs to be removed in order not to break our knowledge / belief base.

    The function uses a brute force revision method to proove if the question is true or false.
    """
    counter = 0
    clauses_to_remove = []

    while True:
        counter = counter + 1
        kb = copy.deepcopy(kb_input)
        kb.list_of_clauses = sorted(kb.list_of_clauses)
        clauses_to_remove = binary_counter(counter)

        for c in clauses_to_remove:
            kb.list_of_clauses.pop(c)


        if (not pl_resolution2(kb.list_of_clauses, Not(a))):
            return clauses_to_remove