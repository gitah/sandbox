# fred-regex.py
# Fred Song, xx@uvic.ca
# My implementation of a regex parser in Python :)
# Do what you like with the code

class Edge:
    def __init__(self, transition, begin, end):
        """None transition = espilon edge"""
        self.transition = transition
        self.begin = begin
        self.end = end

class Vertex:
    def __init__(self, edges=[], accept=False):
        self.value = value
        self.accept = accept
        self.edges = []

    def connect(self, v2, transition):
        edge = Edge(transition)
        edge.begin = self
        edge.end = v2
        self.edges.append(edge)

class DFA():
    def __init__():
        return;

class NDFA():
   """Non-deterministic finite automaton"""
   def __init__():
        return;

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

#---- Public Methods ----#
def match(myregex, mystr):
    # Convert to postfix for easier parsing
    post_regex = postfix(myregex)

    # Turn to NDFA
    ndfa = dfa(post_regex)

    # Turn to DFA
    dfa = ndfa_to_dfa(ndfa)

    # Walk DFA
    return _walk_dfa(dfa, mystr)

unary_ops = ["*","+","?"]
binary_ops = ["|", "&"]
operators = unary_ops + binary_ops
letters =   [
    "a","b","c","d","e","f",
    "g","h","i","j","k","l","m","n",
    "o","p","q","r","s","t","u","v",
    "w","y","x","z"
]
digits = [0,1,2,3,4,5,6,7,8,9]
escape = "\\"
other = ["^","$"]


def regex_toarray(myregex):
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

    regex_arr = regex_toarray(myregex)
    print "[%s]" % ",".join(regex_arr)

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

def build_state_singleton(e):
    start.connect(State(),e)
    return start

def build_state_concat(e1,e2):
    start = State()
    #start.connect 
    pass
def build_state_star():
    pass
def build_state_or():
    pass
def build_state_plus():
    build_state_star()
    pass

def dfa(post_regex):
    regex_arr = regex_toarray(post_regex)

    dfa_stack = []
    
    for c in regex_arr:
        if c not in operators:
            stack.append(build_state_singleton(c))
        elif c in binary_ops:
            e1 = dfa_stack.pop()
            e2 = dfa_stack.pop()

            elif c == '&':
                dfa_stack.append(build_state_concat(e1,e2))
            elif c == '|':
                dfa_stack.append(build_state_or(e1,e2))
                pass

        elif c in unary_ops:
            e1 = dfa_stack.pop()

            if c == '*':
                dfa_stack.append(build_state_star(e1))
            elif c == '+':
                dfa_stack.append(build_state_plus(e1))
            elif c == '?':
                dfa_stack.append(build_state_question(e1))

        return

def ndfa_to_dfa(ndfa):
    pass

if __name__ == "__main__":
    # Test postfix
    t1 =  r"ab"
    t2 =  r"(a|b)"
    t3 =  r"a\+"
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

    print t1, dfa(postfix(t1))
