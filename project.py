# Michelle Lally G00351333
# Graph Theory Project 2019

def addconcat(infix):
    '''
        Function that generates updates the expression to append concatenation if it hasn't been included used
    '''
    # Special characters - 2 sets. Since there are different outcomes
    # when brackets are used there needs to be 2 different set of characters
    spec1 = ('+', '|', '?', '*', '.', '(')
    spec2 = ('+', '|', '?', '*', '.', ')')

    # temporary variable to store the updated expression in
    temp = ""
    # converting infix to an enum so it becomes iterarable
    for i, c in enumerate(infix):
        # check if the character is a special character 
        # this means it doesn't need to have the concat character appended
        if c in ('+', '|', '?', '*', '.', '('):
            temp += c
        else:
           # try to catch IndexError exception
           # needed for when it is checking the next character 
           # on last character it will search an index that is out of bounds
            try:
                # check the next character is not a special character
                if infix[i+1] not in ('+', '|', '?', '*', '.', ')'):
                    # if it isn't appened the concat character
                    temp += c + "."
                # otherwise don't appened character
                else: 
                    temp += c
            # if exception is thrown
            except IndexError:
                # add the character as it is
                temp += c
                break
    #print("temp", temp)
    return temp

def shunt(infix):
    '''
        Shunting yard algorithm to translate infix notation to infix notation
        Needed because the computer is unaware of order of precedence 
    '''
    # call the addconcat method to append implicit concatenation 
    infix = addconcat(infix) 

    # order of precendence in special characters 
    specials = {'*': 50, '.': 40, '|': 30}
    pofix = ""
    stack = ""

    for c in infix:
        if c == '(':
            stack = stack + c
        elif c == ')':
            # Check the last character in the string
            while stack[-1] != '(':
                # Pushing the operators at the end of the stack to pofix as long as it's not the open bracket
                pofix = pofix + stack[-1]
                # Remove that operator from the stack
                stack = stack[:-1]
            # Remove the ( from the stack 
            stack = stack[:-1]
        elif c in specials: 
            # Check while theres something on the stack, and c's precedence is <= the precedence on the stack
            # specials.get(c , 0) means if c is in specials, get its value from the dictionary otherwise give it the value 0
            # Then check if whats on top of the stack is in specials and get its value from the dictionary otherwise give it 0
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                # Remove the operator at the top of the stack and put it into pofix 
                pofix, stack = pofix + stack[-1], stack[:-1]
            # Push c onto the stack
            stack = stack + c
        else:
           pofix = pofix + c 

    while stack:
        # Pushing the operators at the end of the stack to pofix as long as it's not the open bracket
        pofix = pofix + stack[-1]
        # Remove that operator from the stack
        stack = stack[:-1]
        # Remove the ( from the stack 
    return pofix

# Plans for something you might create in memory 
# Can be reused
# represents a state with 2 arrows labelled by label
# use none for a label representing 'e' arrows
class state: 
    # Character 
    label = None
    # In arrow
    edge1 = None
    # Out arrow
    edge2= None

# an nfa
class nfa: 
    initial = None
    accept = None

    # Constructor in python starts and ends in 2 underscores
    # Every function must also has to have self as its first parameter 
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    # Stack of NFA's 
    nfastack = []

    for c in pofix: 
        # Catenation
        if c == '.':
            nfa2 =  nfastack.pop()
            nfa1 = nfastack.pop()
            # take an edge from the accept state of nfa1 and let it 
            # equal to nfa2's initial state 
            # this joins the 2 nfa's together
            nfa1.accept.edge1 = nfa2.initial
            # newnfa's initial state is nfa1
            # and its accept state is equal to nfa2's accept state
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)

        # Alternation
        elif c == '|':
            # pop 2 nfa's off the stack
            nfa2 =  nfastack.pop()
            nfa1 = nfastack.pop()
            # creating an instance of state and connect it to
            # the initial states of the nfa's popped from the stack
            initial = state()
            # creating an instance of state and connect it to
            # the accept states of the nfa's popped from the stack
            accept = state()
            # join new initial state to the inital state of nfa1
            initial.edge1 = nfa1.initial
            # join new initial state to the inital state of nfa2
            initial.edge2 = nfa2.initial
            # nfa1 and nfa2 initial states are no longer initial states 
            # nfa1 accept state to point at the new accept state
            nfa1.accept.edge1 = accept
            # nfa2 accept state to point at the new accept state
            nfa2.accept.edge1 = accept
            # push new nfa to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

        # Zero or more
        elif c == '*':
            # pop single nfa from the stack 
            nfa1 = nfastack.pop()
            # create new initial and accept states
            # creating an instance of state
            accept = state()
            # creating an instance of state
            initial = state()
            # join the new initial state to nfa1's initial state
            # take an edge from the initial state and let it equal an accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # join the old accept state to nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            # take an edge from nfa1's initial state and join it to the new accept state
            nfa1.accept.edge2 = accept
            # push new nfa to the stack 
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

        # Zero or one
        elif c == '?':
             # pop single nfa from the stack 
            nfa1 = nfastack.pop()
            # create new initial and accept states
            # creating an instance of state
            accept = state()
            # creating an instance of state
            initial = state()
            # join the new initial state to nfa1's initial state
            # take an edge from the initial state and let it equal an accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # join the old accept state to the new accept state
            nfa1.accept.edge1 = accept
            # push new nfa to the stack 
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        
        # One or more
        elif c == '+':
            # pop single nfa from the stack 
            nfa1 = nfastack.pop()
            # create new initial and accept states
            # creating an instance of state
            accept = state()
            # creating an instance of state
            initial = state()
            # join the new initial state to nfa1's initial state 
            initial.edge1 = nfa1.initial
            # join the new initial state to nfa1's initial state
            # take an edge from the initial state and let it equal an accept state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # push new nfa to the stack 
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

        else:
            # creating an instance of state
            accept = state()
            # creating an instance of state
            initial = state()
            # label of arrow coming out of the initial state is going to be c
            initial.label = c
            # edge1 points to the accept state
            initial.edge1 = accept
            # creates a new instance of the NFA class and set the initial state to the initial state just created and the same with accept
            nfastack.append(nfa(initial, accept))
    
    # nfastack should only have a single nfa at the end
    return nfastack.pop()

def followes(state):
    """ Return the set of states that can be reached from states following the e arrows """
    # Create a new set, with state as its only member 
    states = set()
    states.add(state)

    # check id the state that has arrows e from it 
    if state.label is None:
        # check if edge1 is a state
        if state.edge1 is not None:
        # if theres an edge 1, follow it 
            states |= followes(state.edge1)
        # check if edge2 is a state
        if state.edge2 is not None:
        # if theres an edge 2 follow it
            states |= followes(state.edge2)

    # Return the set of states
    return states



def match(infix, string):
    """ Matches the string to the infix regular expression"""

    # shunt and compile the regular epxression 
    # turn infix into postfix
    postfix = shunt(infix)
    # print("postfix: " ,postfix)
    # compile the postfix expression into an nfa
    nfa = compile(postfix)

    #the currrent states and the next states
    current = set()
    next = set()

    # Add the initial state to the current set
    current |= followes(nfa.initial)

    # loop through each character in the string
    for s in string:
        # loop through the current set of states 
        for c in current:
            # check if that state is labelled s 
            if c.label == s: 
                # add the edg1 state to the next set 
                next |= followes(c.edge1)
        #set current to next, and clear out next
        current = next
        next = set()

    #check is the accept state is in the currect states
    return (nfa.accept in current)

print("===Regular Expression Matching Console Application===")

inifixes = ["(abc)?","abc*", "a(b|d)c*", "(a(b|d))*", "a(b)c", "a|bc+"]
strings = ["", "abc", 'bcc', "abbc", "daab", "abcc", "abd", "abbc"]

for i in inifixes:
    print('==================================================')
    print('\tExpression : ', i)
    for s in strings:
        print('{0}\t|| {1}\t||\t{2}'.format(match(i, s), i, s))
print('==================================================')

#print("Please choose from one of the following options: ")
#print("\t1. Enter a regex and string manually")
#print("\t2. Check a regex using the built in test data")
#print("\t3. To exit")
#option = input()
#while option != 3:
#   menu(option)    

def menu(option):

    if option == 1:
        print("=== Manual Matching ===")
        s = input("Enter the string you want to want to check matches a regular expression: ")
        i = input("Enter the infix expression that you want the string to be checked ")
        print('==================================================')
        print('\tExpression : ', i)
        print('{0}\t|| {1}\t||\t{2}'.format(match(i, s), i, s))
        print('==================================================')

    elif option == 2:
        for i in inifixes:
            print('==================================================')
            print('\tExpression : ', i)
            for s in strings:
                print('{0}\t|| {1}\t||\t{2}'.format(match(i, s), i, s))
            print('==================================================')

    else:
        print("Invalid input. Please try again")




