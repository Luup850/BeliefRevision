from asyncio.windows_events import NULL
from xml.etree.ElementTree import tostring
import sympy.logic.boolalg as boolalg
from sympy.logic.boolalg import And, Not, Or, Xor
from utils import pl_resolution2, Clause

class BeliefBase:

    def __init__(self):
        self.list_of_clauses = []
        self.order_int = 0

    def tell(self, query):
        query = str(boolalg.to_cnf(query))
        query = query.split(" & ")
        print(query)
        for q in query:
            #print(Clause(q, self.order_int).list_of_literals)
            #print("Clause", new_clause.list_of_literals)
            self.list_of_clauses.append(Clause(q, self.order_int))
        self.order_int = self.order_int + 1
    
    def ask(self, question):
        question = boolalg.to_cnf(question)
        return pl_resolution2(self.list_of_clauses, question)



bb = BeliefBase()
bb.tell("(A & B)")
#print(bb.list_of_clauses)
#s = Clause("G | D", 0)
print(bb.ask("A"))
#print(bb.list_of_clauses)