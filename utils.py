from matplotlib.font_manager import list_fonts
import sympy.logic.boolalg as boolalg
from sympy.logic.boolalg import And, Not, Or, Xor
import copy

# binary counter
def binary_counter(n):
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
    # String format
    #list_of_literals = []
    def __init__(self, clause, order, isString=True):
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

    def sorted_string(self):
        sorted_list = sorted(self.list_of_literals)
        sorted_list_str = ""
        for l in sorted_list:
            sorted_list_str += l.value
        return sorted_list_str
        #return ''.join(map(str, sorted(self.list_of_literals)))
    
    def debug_print(self, res_ret=False):
        output = "[DEBUG CLAUSE]:"
        for l in self.list_of_literals:
            output += " " + l.value
        if(not res_ret):
            print(output)
        else:
            return output

    def __eq__(self, other):
        return self.order == other.order

    def __lt__(self, other):
        return self.order < other.order

class Literal:
    def __init__(self, literal, order, parent):
        self.value = literal
        self.parent = parent
        self.order = order

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

def get_literals(clause):
    clause = clause.replace(" ", "")
    clause = clause.replace("(", "")
    clause = clause.replace(")", "")
    clause = clause.split("|")
    return clause

# Useless
def pl_resolution(kb, a):
    """
    Input: Kb - Knowledge base or Belief base, a - question.
    Output: True or False, based on if the question is true or false with the given knowledge.
    The function uses a brute force resolution method to proove if the question is true or false.
    """
    clauses = kb
    clauses.append(str(a))

    # Make all possible combinations of clauses where literals are subtracted
    while True:
        resolution_set = []
        for i,c in enumerate(clauses):
            for j,d in enumerate(clauses):
                if (i != j):
                    literals_a = get_literals(c)
                    literals_b = get_literals(d)
                    for l_a in literals_a:
                        # If a literal exists and a ~literal exist.
                        if (str(Not(l_a)) in literals_b):
                            
                            clause_to_append = ""
                            for l_b in literals_b:
                                if (str(Not(l_a)) != l_b):
                                    clause_to_append += l_b + " | "
                            clause_to_append = clause_to_append[:-3]
                            if(clause_to_append not in resolution_set and clause_to_append not in clauses):
                                resolution_set.append(clause_to_append)
        if (len(resolution_set) == 0):
            break
        elif ("" in resolution_set):
            clauses.append("")
            break
        else:
            clauses.extend(resolution_set)

    if ("" in clauses):
        return True
    else:
        return False


def pl_resolution2(kb_input, a):
    a = str(Not(a))
    a = str(boolalg.to_cnf(a))
    a = a.split(" & ")
    kb = copy.deepcopy(kb_input)
    for c in a:
        kb.append(Clause(c, -1))
    
    is_not_done = True
    while is_not_done:
        is_not_done = False

        for i,ci in enumerate(kb):
            for j,cj in enumerate(kb):
                if (i != j):

                    # Looking at the literals in each clause to determine if they cancel out.
                    for k,li in enumerate(ci.list_of_literals):
                        for l,lj in enumerate(cj.list_of_literals):
                            if (str(Not(li.value)) == lj.value):
                                copy_of_ci = copy.deepcopy(ci)
                                copy_of_cj = copy.deepcopy(cj)
                                #copy_of_ci.list_of_literals.remove(li)
                                del copy_of_ci.list_of_literals[k]
                                #copy_of_cj.list_of_literals.remove(lj)
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
    #kb_org = copy.deepcopy(kb_input)
    counter = 0
    clauses_to_remove = []

    # While this gives a contradiction, kb still contains a troublesome clause.
    # Basically a brute force approach.
    while True:
        counter = counter + 1
        kb = copy.deepcopy(kb_input)
        
        kb.list_of_clauses = sorted(kb.list_of_clauses)
        #kb.sort(key=lambda x: x.order)
        #for c in kb:
        #        c.debug_print()
        clauses_to_remove = binary_counter(counter)
        #print("[DEBUG]:", clauses_to_remove)
        for c in clauses_to_remove:
            #print("Removed clause: ", kb[c].debug_print())
            #print(type(kb[c]))
            #del kb[c]
            print("[{1}]This was popped: {0}".format(kb.list_of_clauses.pop(c).list_of_literals[0].value, counter))

        if (not pl_resolution2(kb.list_of_clauses, Not(a))):
            print_stuff = ""
            for c in kb.list_of_clauses:
                print_stuff += c.debug_print(True)
            print(print_stuff)
            return clauses_to_remove


    print("Stuff to remove: ", clauses_to_remove)
    return clauses_to_remove

    