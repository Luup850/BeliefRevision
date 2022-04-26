from asyncio.windows_events import NULL
import copy
from xml.etree.ElementTree import tostring
import sympy.logic.boolalg as boolalg
from sympy.logic.boolalg import And, Not, Or, Xor
from utils import pl_resolution2, Clause, revision

class BeliefBase:

    def __init__(self):
        self.list_of_clauses = []
        self.order_int = 0

    def tell(self, query):
        if (not pl_resolution2(self.list_of_clauses, str(Not(query))) or len(self.list_of_clauses) == 0):
            print("Expansion with '{0}' succeded".format(query))
            self._expand(query)
        else:
            print("Expansion with '{0}' failed".format(query))
            print("Solving issue by revision...")

            # Get all clauses that causes contradictions with the given query.
            list_of_clauses_to_remove = revision(self, query)
            self._contract(list_of_clauses_to_remove)
            self._expand(query)
    
    def ask(self, question):
        question = boolalg.to_cnf(question)
        return pl_resolution2(self.list_of_clauses, question)

    def _expand(self, query):
            query = str(boolalg.to_cnf(query))
            query = query.split(" & ")
            print(query)
            for q in query:
                #print(Clause(q, self.order_int).list_of_literals)
                #print("Clause", new_clause.list_of_literals)
                self.list_of_clauses.append(Clause(q, self.order_int))
                self.order_int = self.order_int + 1

    # Contract a Clause
    def _contract(self, query):
        self.list_of_clauses.sort()
        for c in query:
            del self.list_of_clauses[c]
    
    def debug_print(self):
        output = ""
        for c in self.list_of_clauses:
            for l in c.list_of_literals:
                output += " " + l.value
        print(output)


bb = BeliefBase()
bb.tell("(A & B)")
bb.tell("C")
bb.tell("D")
#print(bb.ask("(A & B)"))
print("----------")
bb.debug_print()
print("----------")
bb.tell("~B & E")
#print(bb.ask("C"))
#print("Im an idiot!")
print("----------")
bb.debug_print()
#s = Clause("G | D", 0)
#print(bb.ask("C | A"))
#print(bb.list_of_clauses)