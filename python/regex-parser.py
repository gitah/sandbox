# fred-regex.py
# Author: Fred Song, xx@uvic.ca

# This is my implementation of a regex parser in Python
# I'm doing it just for fun; do what ever you like with the code

# Here is how it works:
#   1. (<regex>, <string>) is given as input
#   2. convert <regex> to <postfix>
#   3. Build <NDFA> from <postfix>
#   4. Convert <NDFA> to <DFA>
#   5. use <DFA> to match <regex> with <string>

#TODO:
#   - Make NDFA class
#   - Finish post-> ndfa

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


#---- Classes ----#
class Vertex:
    class Edge:
        def __init__(self, target, transition):
            #transition == None means an espilon edge
            self.transition = transition
            self.target = target
        
        def __str__(self):
            return self.transition

    def __init__(self, accept=False):
        self.accept = accept
        self.edges = []

    def connect(self, v2, transition):
        edge = Vertex.Edge(v2,transition)
        self.edges.append(edge)

    def get_adj(self):
        return [e.target for e in self.edges]

class NDFA():
    """Non-deterministic finite automaton"""
    def __init__(self,start_vertex):
        self.start = start_vertex

    def get_accept(self):
        accept_vertices = []
        def count_accept(v):
            if v.accept:
                accept_vertices.append(v)

        self.dfs(count_accept)
        return accept_vertices

    def dfs(self, op):
        """Preforms depth-first search on graph and running function 'op' on
        each of the visited verticies"""
        def dfs_recur(v):
            op(v)
            v._visited = True
            for u in v.get_adj():       
                if not hasattr(u, "_visited"):
                    dfs_recur(u)

        def reset_visited(v):
            delattr(v, "_visited")
            for u in v.get_adj():
                if hasattr(u,"_visited"):
                    reset_visited(u)

        dfs_recur(self.start)
        reset_visited(self.start)

    def __str__(self):
        out = []
        def print_v(v):
            format_str = "%s (s: %s, a: %s): t[%s]"
            out.append(format_str % (v, v == self.start, v.accept, 
                ",".join([str(e.transition) for e in v.edges])))

        self.dfs(print_v)
        return "\n".join(out)

    # These are static constructor methods for building NDFAs
    # Called during postfix parsing
    @staticmethod
    def build_singleton(transition):
        """The simplest NDFA for a single character
            
            Returns NDFA
                V: {start, end}
                E: {(start, end, transition)}
        """
        start = Vertex()
        start.connect(Vertex(accept=True), transition)
        return NDFA(start)

    #Binary Operators
    @staticmethod
    def build_concat(ndfa1, ndfa2):
        """Joins two NDFA together to implement the & operator"""
        start2 = ndfa2.start
        for acc in ndfa1.get_accept():
            acc.connect(start2, None)
        return NDFA(ndfa1.start)

    @staticmethod
    def build_or(ndfa1, ndfa2):
        """Joins two NDFA together to implement the | operator"""
        start1 = ndfa1.start
        start2 = ndfa2.start

        start1.connect(start2, None)
        return NDFA(ndfa1.start)

    #Unary Operators
    @staticmethod
    def build_star(ndfa):
        """Returns a modified version of the ndfa to implement the * operator"""
        pass

    @staticmethod
    def build_plus(ndfa):
        """Returns a modified version of the ndfa to implement the + operator"""
        pass

    @staticmethod
    def build_question():
        """Returns a modified version of the ndfa to implement the ? operator"""
        pass



#---- Regex -> Postfix ----#
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

#---- Postfix -> NDFA ----#
def dfa(post_regex):
    regex_arr = regex_toarray(post_regex)
    
    stack = []
    for c in regex_arr:
        if c not in operators:
            stack.append(NDFA.build_singleton(c))
        elif c in binary_ops:
            e2 = stack.pop()
            e1 = stack.pop()

            if c == '&':
                stack.append(NDFA.build_concat(e1,e2))
            elif c == '|':
                stack.append(NDFA.build_or(e1,e2))

        elif c in unary_ops:
            e1 = stack.pop()

            if c == '*':
                stack.append(NDFA.build_star(e1))
            elif c == '+':
                stack.append(NDFA.build_plus(e1))
            elif c == '?':
                stack.append(NDFA.build_question(e1))

    return stack.pop()

#---- NDFA -> DFA ----#
def ndfa_to_dfa(ndfa):
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

    # Turn to NDFA
    ndfa = dfa(post_regex)

    # Turn to DFA
    dfa = ndfa_to_dfa(ndfa)

    # Walk DFA
    return _walk_dfa(dfa, mystr)

#---- Tests ----#
if __name__ == "__main__":
    #t1 =  r"ab"
    t2 =  r"(a|b)"
    t3 =  r"a\+"
    t4 =  r"(a|b)*cd"
    t5 =  r"(a|b)*fo\+"
    t6 =  r"((a|b)*aba*)*(a|b)(a|b)"
    t7 =  r"(a|b)+@vic\.(ca|com)"

    #print t1, ": ",  postfix(t1)
    print t2, ": ",  postfix(t2)
    #print t3, ": ",  postfix(t3)
    #print t4, ": ",  postfix(t4)
    #print t5, ": ",  postfix(t5)
    #print t6, ": ",  postfix(t6)
    #print t7, ": ",  postfix(t7)

    print "------"
    #print dfa(postfix(t1))
    print dfa(postfix(t2))
