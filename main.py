# User Interface for the BELIEF REVISION ENGINE
#
#
# =============================================================================
#                       IMPORTS
# =============================================================================
import os

from belief_base_v2 import BeliefBase

# =============================================================================
#                       FUNCTIONS
# =============================================================================
belief_base = BeliefBase()
def ASK(sent):
    return belief_base.ask(sent)

def TELL(sent):
    belief_base.tell(sent)

def main_menu():
    # MAIN_MENU Display the MAIN MENU.

    choice = 0
    while True : 
        inp=input("\nInsert here:")
        inp = inp.strip()
        temp = inp.split(" ")
        sent = " ".join(temp[1:])
        choice = temp[0].upper()
        
        # CHOICE 1: "Ask a question."
        if choice== "ASK":
            print("Finding answer by pl-resolution...")
            answer = ASK(sent)
            print("\nThe question is: {0}".format(answer))

        # CHOICE 2: "Tell new information."     
        elif choice== "TELL":
            TELL(sent)

        # CHOICE 3: "See current information."     
        elif choice== "BELIEF":
            belief_base.debug_print()
             
        # CHOICE 4: "Exit."
        elif choice== "EXIT":
            os.system('cls' if os.name=='nt' else 'clear')
            print("\n• Thank you for using the Belief Revision Engine. See you soon!.")
            print("\n Authors:")
            print("\n   • Cem Rizalar - s212383")
            print("\n   • Daniel Schober - s212599")
            print("\n   • Marcus Christiansen - s213424")
            print("\n   • Maria Carmela Mas Marhuenda - s212488\n")
            break

        # If it is no a valid choice
        else:
            print("\nPlease remember, command must start with 'ASK' or 'TELL' and be followed by a space")
             


# =============================================================================
#                       MAIN
# =============================================================================

if __name__ == '__main__':
    os.system('cls' if os.name=='nt' else 'clear')
    # Displays the WELCOME only the first time the program runs
    print("\n~~~~ BELIEF REVISION ENGINE ~~~~")
    print("\nWelcome to ""The Belief Revision Engine""!!\n")
    #print("\n")
    print("\nPlease, pay attention to the User's Guide:")
    print("\n   • Start each sentence with either ASK or TELL followed by a space.")
    print("\n   • Use ASK to ask a question")
    print("\n   • Use TELL to tell new information")
    print("\n   • Use BELIEF to see the current belief base")
    print("\n   • All letters can be used as literals except: [E, S, Q]")
    print("\n   • Use Logical Expressions like: & | ~  << >> ")
    print("\n   • You are allowed to use brakets ()")
    print("\n   • Type EXIT to Exit\n")
    
    # Display MAIN MENU
    main_menu()
      