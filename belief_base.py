from asyncio.windows_events import NULL
from xml.etree.ElementTree import tostring
import sympy.logic.boolalg as boolalg
from sympy.logic.boolalg import And, Not, Or, Xor
from utils import get_literals, pl_resolution

class BeliefBase:
    def __init__(self):
        self.beliefs = NULL

    def add_belief(self, belief):
        if (self.beliefs == NULL):
            self.beliefs = boolalg.to_cnf(belief)
        else:
            self.beliefs = And(self.beliefs, boolalg.to_cnf(belief))
            self.beliefs = boolalg.to_cnf(self.beliefs)

    def ask(self, query):
        query = Not(query)
        query = boolalg.to_cnf(query)
        return pl_resolution(self.get_clauses(), query)
        #pass

    def get_clauses(self):
        return str(self.beliefs).split(" & ")

bb = BeliefBase()
#bb.add_belief("(A >> B) & (C >> A) ")
bb.add_belief("(A & B)")
print(bb.ask("A"))
#print(bb.beliefs)
#b = And().
#s = str(bb.beliefs[0])
#print(type(bb.beliefs))
#clauses = bb.get_clauses()
#for c in clauses:
#    print(get_literals(c))