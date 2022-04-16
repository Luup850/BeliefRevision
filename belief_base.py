#%%
from xml.etree.ElementTree import tostring
import sympy.logic.boolalg as boolalg
from sympy.logic.boolalg import And

class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def add_belief(self, belief):

        belief = boolalg.to_cnf(belief, simplify=True, force=True)
        belief = str(belief).split(" & ")
        for b in belief:

            # Implement check that works with checking parenthesies
            if b not in self.beliefs:
                if (len(belief) > 1) and (b):
                    self.beliefs.append(b[1:-1])
                else:
                    self.beliefs.append(b)
        print(type(belief))

    def ask(self, query):
        pass

bb = BeliefBase()
bb.add_belief("(A >> B) & (C >> A) ")
bb.add_belief("(A & B)")
print(bb.beliefs)
#b = And().
s = str(bb.beliefs[0])
print(type(bb.beliefs))
# %%
