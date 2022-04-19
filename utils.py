import sympy.logic.boolalg as boolalg
from sympy.logic.boolalg import And, Not, Or, Xor

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