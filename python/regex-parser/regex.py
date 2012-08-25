# fred-regex.py
# Author: Fred Song, fsong@xei.ca

# This is my implementation of a regex parser in Python
# I'm doing this just for fun; do what ever you like with the code

# Here is how it works:
#   1. (<regex>, <string>) is given as input
#   2. convert <regex> to <postfix>
#   3. Build <NFA> from <postfix>
#   4. Convert <NFA> to <DFA>
#       see: http://web.cecs.pdx.edu/~harry/compilers/slides/LexicalPart3.pdf
#   5. use <DFA> to match <regex> with <string>

#TODO:
#   implement ^/$
#   implement regex.search (along with ^/$ symbols)
#   implement regex.findall
#   think about greedy/non-greedy match
from automaton import NFAState, NFA, DFA

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
misc = ["^","$"]
char_class_map = {
    "\\s": "[ \t]",
    "\\w": "[0-9a-zA-Z_]"
}



#---- Regex -> Postfix ----#
def postfix(myregex):
    """ Converts infix notation regex to postfix notation regex
        
        Parenthesis are removed, but the & operator is introduced for
        concatentation

        ex:
        ((a|b)*aba*)*(a|b)(a|b) -> ab|*a&b&a*&*ab|&ab|&
        (a|b)+@vic\.(ca|com) -> ab|+@&uU|&v&i&c&\.&ca&co&m&|&
    """
    regex_arr = regex_to_array(myregex)
    return postfix_recur(regex_arr)[0]

def postfix_recur(arr,start=0,in_brackets=False):
    stack = [] # stores subexpressions
    def stack_to_postfix():
        while len(stack) > 1:
            e2, e1 = stack.pop(), stack.pop()
            e = e1 + e2 + "&" 
            stack.append(e)
        return stack.pop()

    i = start  # the current token we're on
    # iterate through each token of the regex
    while i < len(arr):
        tok = arr[i]
        # do different things depending on the type of token
        if tok in binary_ops:
            if len(stack) == 0:
                raise ValueError("bad regex: %s" % "".join(arr))
            e1 = stack_to_postfix()
            e2, i2 = postfix_recur(arr, i+1, in_brackets)
            if not e1 or not e2:
                raise ValueError("bad regex: %s" % "".join(arr))
            stack.append(e1 + e2 + tok)
            i = i2-1 # we want to revisit the token we terminated at
        elif tok in unary_ops:
            if len(stack) == 0:
                raise ValueError("bad regex: %s" % "".join(arr))
            e = stack.pop()
            stack.append(e+tok)
        elif tok == "(":
            e, i2 = postfix_recur(arr, i+1, True)
            stack.append(e)
            i = i2
        elif tok == ")":
            if not in_brackets:
                raise ValueError("bad regex: %s" % "".join(arr))
            return stack_to_postfix(), i
        else: #normal character
            stack.append(tok)
        i += 1

    return stack_to_postfix(), i


#---- Postfix -> NFA ----#
def postfix_to_nfa(post_regex):
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
    start = NFAState(start=True)
    acc = NFAState(accept=True)
    start.add_transition(acc, transition)
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
    plus_nfa = build_plus_nfa(nfa)
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
    opt_state = NFAState(accept=True)
    nfa.get_start_state().add_transition(opt_state, None)
    return NFA(nfa.start)

#---- Utility ----#
def _tokenize(s):
    """ A generator for a regex that yields a token 
    
        A token is a sequence of characters in the regex
    """
    def get_escape_token(s,j):
        try:
            return s[j] + s[j+1], j+1
        except IndexError:
            raise ValueError("Not character found following \\")

    def get_char_class_token(s,j):
        tok = []
        try:
            while True:
                if s[j] == "]":
                    tok.append(s[j])
                    return "".join(tok), j
                else:
                    tok.append(s[j])
                j += 1
        except IndexError:
            raise ValueError("character class not ended")

    i = 0
    while i < len(s):
        c = s[i]
        if c == '[':
            tok, inew = get_char_class_token(s,i)
            yield tok
            i = inew
        elif c == '\\':
            tok, inew = get_escape_token(s,i)
            yield tok
            i = inew
        else:
            yield c
        i += 1

def regex_to_array(myregex):
    """Turns regex into array"""
    return list(_tokenize(myregex))

def _in_character_class(cc, c):
    """ Returns true if character c is in character class cc """
    def sequence_gen(seq):
        assert len(seq) == 3
        digits = "0123456789"
        letters = "abcdefghijklmnopqrstuvwxyz"
        beg,end = seq[0], seq[2]

        if beg in digits and end in digits:
            gen = digit_gen
        elif beg.lower() in letters and end.lower() in letters:
            gen = letter_gen

        for i in gen(beg,end):
            yield i

    def digit_gen(start,end):
        for i in xrange(int(start),int(end)+1):
            yield str(i)

    def letter_gen(start,end):
        letter_range = ord(end)-ord(start)
        for i in range(0,letter_range+1):
            yield chr(ord(start)+i)

    assert cc[0] == "[" and cc[-1] == "]"
    # strip [ and ]
    cc = cc[1:-1]

    negate = False
    if cc[0] == "^":
        negate = True
        cc = cc[1:]

    inclass = False
    i = 0
    while i < len(cc):
        sym = cc[i]
        if sym == "-":
            seq = "%s%s%s" % (cc[i-1],cc[i],cc[i+1])
            if c in list(sequence_gen(seq)):
                inclass = True
                break
        elif sym == c:
            inclass = True
            break
        i += 1

    inclass = not(inclass) if negate else inclass
    return inclass

def _get_transition(state, c):
    """ returns a transition of the given state that matches character c """
    trans_values = state.get_transition_values()
    for tv in trans_values:
        if tv == ".":
            return tv
        if tv.startswith("["):
            if _in_character_class(tv,c):
                return tv
        if tv.startswith("\\"):
            cc = char_class_map.get(tv)
            if cc and _in_character_class(cc,c):
                return tv
        if tv == c:
            return tv
    return None

def _walk_dfa(dfa, inp):
    """ Tranverses dfa with the given input
        
        returns True if traversal ended on an accept state
    """
    curr_state = dfa.get_start_state()
    for c in _tokenize(inp):
        trans = _get_transition(curr_state,c)
        if not trans:
            return False
        next_state = curr_state.get_transition(trans)
        curr_state = next_state
    return curr_state.is_accept()

#---- Public Interface ----#
def match(myregex, inp):
    # Convert to postfix for easier parsing
    post_regex = postfix(myregex)

    # Turn to NFA
    nfa = postfix_to_nfa(post_regex)

    # Turn to DFA
    dfa = nfa.to_dfa()

    # Walk DFA
    return _walk_dfa(dfa, inp)
