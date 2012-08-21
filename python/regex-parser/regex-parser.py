# fred-regex.py
# Author: Fred Song, fsong@xei.ca

# This is my implementation of a regex parser in Python
# I'm doing this just for fun; do what ever you like with the code

# Here is how it works:
#   1. (<regex>, <string>) is given as input
#   2. convert <regex> to <postfix>
#   3. Build <NFA> from <postfix>
#   4. Convert <NFA> to <DFA>
#   5. use <DFA> to match <regex> with <string>

#TODO:
#   - implement NFA -> DFA algorithm
# http://web.cecs.pdx.edu/~harry/compilers/slides/LexicalPart3.pdf

from automaton import NFA, DFA

#---- Constants ----#
unary_ops = ["*","+","?"]
binary_ops = ["|", "&"]
operators = unary_ops + binary_ops
letters = [
    "a","b","c","d","e","f","g","h",
    "i","j","k","l","m","n","o","p",
    "q","r","s","t","u","v","w","y",
    "x","z"
]
digits = [0,1,2,3,4,5,6,7,8,9]
escape = "\\"
misc = ["^","$", "\\s", "\\w"]



#---- Regex -> Postfix ----#
def regex_to_array(myregex):
    """Turns regex into array and adds & operator where appropriate"""
    regex_arr = []
    # First pass turn regex to an array
    escape_flag = False
    for c in myregex:
        if escape_flag:
            regex_arr.append('\\'+c)
            escape_flag = False
        elif c == '\\':
            escape_flag = True
        else:
            regex_arr.append(c)

    return regex_arr

def postfix(myregex):
    """ Converts infix notation regex to postfix notation regex
        
        Parenthesis are removed, but the & operator is introduced for
        concatentation

        ex:
        ((a|b)*aba*)*(a|b)(a|b) -> ab|*a&b&a*&*ab|&ab|&
        (a|b)+@vic\.(ca|com) -> ab|+@&uU|&v&i&c&\.&ca&co&m&|&
    """

    regex_arr = regex_to_array(myregex)
    #print "[%s]" % ",".join(regex_arr)

    return postfix_recur(0,regex_arr)



def postfix_recur(start_index, regex_arr):
    def pop_stacks(exp_stack,op_stack):
        # Process operators
        while op_stack:
            op = op_stack.pop()
            assert op in binary_ops

            e1 = exp_stack.pop()
            e2 = exp_stack.pop()
            new_exp = e2+e1+op
            exp_stack.append(new_exp)

        # Concat remaining expressions
        while len(exp_stack) > 1:
            e2 = exp_stack.pop()
            e1 = exp_stack.pop()
            exp_stack.append(e1+e2+"&")

        assert len(op_stack) == 0
        assert len(exp_stack) == 1

        return exp_stack.pop()

    skip_flag = False
    exp_stack = []
    op_stack = []

    for i in xrange(start_index,len(regex_arr)):
        c = regex_arr[i]
        if c == ')':
            if not skip_flag:
                return pop_stacks(exp_stack, op_stack) 
            else: 
                skip_flag = False

        elif skip_flag:
            continue

        elif c == '(':
            e1 = postfix_recur(i+1,regex_arr)
            exp_stack.append(e1)
            skip_flag = True;

        elif c in operators:
            # NOTE: I'm assuming there's no precedence in regex operators
            # not sure if this is true though
            op = c
            if op in unary_ops:
                e1 = exp_stack.pop()
                new_exp = e1+op
                exp_stack.append(new_exp)
            elif op in binary_ops:
                op_stack.append(op)
        else:
            if len(exp_stack) > 1:
                e2 = exp_stack.pop()
                e1 = exp_stack.pop()
                exp_stack.append(e1+e2+'&')
            exp_stack.append(c)

    if skip_flag:
        raise Error("unmatching brackets")

    return pop_stacks(exp_stack, op_stack) 

#---- Postfix -> NFA ----#
def nfa(post_regex):
    regex_arr = regex_to_array(post_regex)
    
    stack = []
    for c in regex_arr:
        if c not in operators:
            stack.append(build_singleton_nfa(c))
        elif c in binary_ops:
            e2 = stack.pop()
            e1 = stack.pop()

            if c == '&':
                stack.append(build_concat_nfa(e1,e2))
            elif c == '|':
                stack.append(build_or_nfa(e1,e2))

        elif c in unary_ops:
            e1 = stack.pop()

            if c == '*':
                stack.append(build_star_nfa(e1))
            elif c == '+':
                stack.append(build_plus_nfa(e1))
            elif c == '?':
                stack.append(build_question_nfa(e1))

    return stack.pop()

# These are static constructor methods for building NFAs
def build_singleton_nfa(transition):
    """The simplest NFA for a single character
        
        Returns NFA
            V: {start, end}
            E: {(start, end, transition)}
    """
    start = State(start=True)
    acc = State(accept=True)
    start.connect(acc, transition)
    return NFA(start)

#Binary Operators
def build_concat_nfa(nfa1, nfa2):
    """Joins two NFA together to implement the & operator"""
    start2 = nfa2.start
    for acc in nfa1.get_accept_states():
        acc.add_transition(start2, None)
        acc.set_accept(False)
    return NFA(nfa1.start)

def build_or_nfa(nfa1, nfa2):
    """Joins two NFA together to implement the | operator"""
    start1 = nfa1.start
    start2 = nfa2.start
    start1.add_transition(start2, None)
    return NFA(nfa1.start)

#Unary Operators
def build_star_nfa(nfa):
    """Returns a modified version of the nfa to implement the * operator"""
    plus_nfa = NFA.build_plus_nfa(nfa)
    nfa.start.accept = True    
    return NFA(nfa.start)

def build_plus_nfa(nfa):
    """Returns a modified version of the nfa to implement the + operator"""
    # get all accept vertices V_a
    # for v_a in V_a: add edge from v_a to v_start
    for acc in nfa.get_accept_states():
        acc.add_transition(nfa.start, None)
    return NFA(nfa.start)

def build_question_nfa(nfa):
    """Returns a modified version of the nfa to implement the ? operator"""
    opt_node = Vertex(accept=True)
    nfa.start.add_transition(opt_node, None)
    return NFA(nfa.start)

#---- NFA -> DFA ----#
#TODO
def nfa_to_dfa(nfa):
    start = null_closure(nfa.start)
    for inp in inputs:
        start.add_transition(null_set_closure(nfa_transition(start, inp)))

    pass

def set_trans(states, alph):
    """returns list of states Q where for 
        q in Q, and s in states,
        
    # Called during postfix parsing
    # Called during postfix parsing
    # Called during postfix parsing
        Tr_nfa(s,alph) = q
    """
    pass

def nfa_transition(states, inp):
    """Takes a set of states and a input and returns the set of next states states"""
    new_states = set()
    for v in states:
        for e in v.edges:
            if e.transition == inp:
                new_states.add(e.target)
    return new_states


def null_closure(state):
    """state is a vertex from NFA, returns null_closure of state"""
    pass

def null_set_closure(states):
    """states set of substates from NFA, returns null_closure of states"""
    pass

#---- Utility ----#
def _walk_dfa(dfa, mystr):
    curr_node = dfa.start
    curr_letter = 0         # Letter in mystring
    while not curr_node.accept:
        transition_flag = False
        for edge in curr_node.edges:
            if edge.transition == mystr[curr_letter]:
                curr_node = edge.end
                curr_letter += 1
                transition_flag = True
                break

        if not transition_flag:
            return False
        if curr_letter == len(mystr)-1:
            return curr_node.accept

#---- Public Interface ----#
def match(myregex, mystr):
    # Convert to postfix for easier parsing
    post_regex = postfix(myregex)

    # Turn to NFA
    nfa = dfa(post_regex)

    # Turn to DFA
    dfa = nfa_to_dfa(nfa)

    # Walk DFA
    return _walk_dfa(dfa, mystr)

#---- Tests ----#
if __name__ == "__main__":
    #t1 =  r"ab"
    t2 =  r"(a|b)"
    t3 =  r"(a|b)a+"
    t4 =  r"(a|b)*cd"
    t5 =  r"(a|b)*fo\+"
    t6 =  r"((a|b)*aba*)*(a|b)(a|b)"
    t7 =  r"(a|b)+@vic\.(ca|com)"

    #print t1, ": ",  postfix(t1)
    #print t2, ": ",  postfix(t2)
    #print t3, ": ",  postfix(t3)
    #print t4, ": ",  postfix(t4)
    #print t5, ": ",  postfix(t5)
    #print t6, ": ",  postfix(t6)
    #print t7, ": ",  postfix(t7)

    print "------"
    #print nfa(postfix(t1))
    print nfa(postfix(t2))
