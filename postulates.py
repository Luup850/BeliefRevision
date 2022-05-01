from belief_base import *
from utils import *
from sympy.logic.boolalg import And, Not, Or, Xor
import copy

base = BeliefBase()
base.tell("(A & B)")
print(base.ask("A"))
print(base.list_of_clauses[1].list_of_literals[0].value)


def succeed(base, query):
    set1 = []
    base.tell(query)
    for i in range(len(base.list_of_clauses)):
        set1.append(base.list_of_clauses[i].list_of_literals[0].value)
    if(query in set1):
        print('Succeed succesful')
        return True
    return False


def vacuity(base, query):
    set1, set2 = [],[]
    for i in range(len(base.list_of_clauses)):
        set1.append(base.list_of_clauses[i].list_of_literals[0].value)

    if (str(Not(query)) not in set1):
        temp = copy.deepcopy(base)
        base.tell(query)

        for i in range(len(base.list_of_clauses)):
            set2.append(base.list_of_clauses[i].list_of_literals[0].value)

        set1.append(query)
        if (set2 == set1):
            print('Vacuity succesful')
            return True
    return False


def inclusion(base, query):
    temp = copy.deepcopy(base)
    base.tell(query)
    set1 = []
    set2 = []
    for i in range(len(temp.list_of_clauses)):
        set1.append(temp.list_of_clauses[i].list_of_literals[0].value)

    for i in range(len(base.list_of_clauses)):
        set2.append(base.list_of_clauses[i].list_of_literals[0].value)

    if(set.issubset(set(set2), set(set1))):
        print('Inclusion successful')
        return True
    return False


def extensionality(base, query1, query2):
    if (query1 == query2): #Equivalence
        temp = copy.deepcopy(base)
        base.tell(query1)
        temp.tell(query2)

        if (base.__eq__(temp)):
            print('Extensionality succesful')
            return True

    else: print('Queries are not equivalent')
    return False



def closure(base, query):
    temp = copy.deepcopy(base)
    set1 = []
    set2 = []
    base.tell(query)
    for i in range(len(base.list_of_clauses)):
        set1.append(base.list_of_clauses[i].list_of_literals[0].value)

    for i in range(len(temp.list_of_clauses)):
        set2.append(temp.list_of_clauses[i].list_of_literals[0].value)

    if(query in set1):
        if(a in set2 for a in set2):
            print('Closure succesful')
            return True
    return False


succeed(base, "C")
vacuity(base, "C")
extensionality(base, "C", "C")
inclusion(base, "C")
closure(base, "C")
