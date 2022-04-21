from matplotlib.font_manager import list_fonts
import sympy.logic.boolalg as boolalg
from sympy.logic.boolalg import And, Not, Or, Xor
import copy

class Clause:
    # String format
    #list_of_literals = []
    def __init__(self, clause, order):
        self.list_of_literals = []
        self.order = copy.copy(order)
        new_clause = copy.copy(clause)
        new_clause = new_clause.replace(" ", "")
        new_clause = new_clause.replace("(", "")
        new_clause = new_clause.replace(")", "")
        list_of_beliefs = new_clause.split("|")
        for belief in list_of_beliefs:
            self.list_of_literals.append(belief)

    def sorted_string(self):
        return ''.join(map(str, sorted(self.list_of_literals)))

def get_literals(clause):
    clause = clause.replace(" ", "")
    clause = clause.replace("(", "")
    clause = clause.replace(")", "")
    clause = clause.split("|")
    return clause

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
    kb = copy.deepcopy(kb_input)
    kb.append(Clause(a, -1))
    
    is_not_done = True
    while is_not_done:
        is_not_done = False

        for i,ci in enumerate(kb):
            for j,cj in enumerate(kb):
                if (i != j):

                    # Looking at the literals in each clause to determine if they cancel out.
                    for li in ci.list_of_literals:
                        for lj in cj.list_of_literals:
                            if (str(Not(li)) == str(lj)):
                                copy_of_ci = copy.deepcopy(ci)
                                copy_of_cj = copy.deepcopy(cj)
                                copy_of_ci.list_of_literals.remove(li)
                                copy_of_cj.list_of_literals.remove(lj)

                                # If ci and cj are empty, we have a contradiction.
                                if (len(copy_of_ci.list_of_literals) == 0 and len(copy_of_cj.list_of_literals) == 0):
                                    return True

                                # Otherwise add it to the kb.
                                new_clause = copy_of_ci.list_of_literals + copy_of_cj.list_of_literals
                                new_clause = Clause('|'.join(new_clause), -1)
                                
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

