class State(object):
    """A state in the automaton"""
    def __init__(self, start=False, accept=False):
        self.start = start
        self.accept = accept
        self.transitions = {}

    def add_transition(self, v2, trans=None):
        self.transitions[trans] = v2

    def is_start(self):
        return self.start

    def is_accept(self):
        return self.accept

    def get_adj(self):
        return {v for k,v in self.transitions.items()}

    def get_transition_values(self):
        return {k for k,v in self.transitions.items()}

    def set_accept(self, accept):
        self.accept = bool(accept)

    def __str__(self):
        def vid(v):
            return str(id(v))[-3:]
        format_str = "%s (start: %s, accept: %s): t[%s]"

        trans = ["%s->%s"%(t,vid(n)) for t,n in self.transitions.iteritems()]
        return format_str % (vid(self),self.is_accept(),self.is_start(),
                ",".join(trans))

class NFAState(State):
    """Represents a state in a NFA"""
    def __init__(self, start=False, accept=False):
        super(NFAState, self).__init__(start,accept)
        self.null_transitions = []

    def add_transition(self, v2, trans=None):
        if not trans:
            self.null_transitions.append(v2)
        else:
            super(NFAState, self).add_transition(v2,trans)

    def get_adj(self):
        return super(NFAState,self).get_adj() | \
                set(self.get_null_transitions())

    def get_transition(self, trans):
        return self.transitions.get(trans, None)

    def get_null_transitions(self):
        return self.null_transitions

class DFAState(State):
    """Represents a state in a DFA"""
    def __init__(self, start=False, accept=False, substates=None):
        super(DFAState, self).__init__(start,accept)
        self.substates = set(substates) if substates else set()

    def get_substates(self):
        """ returns the set of DFASubstates represented by this DFAstate """
        return self.substates

class Automaton(object):
    """ Represents and Automaton"""
    def __init__(self, start_state):
        self.start = start_state

    def get_start_state(self):
        """Returns the start state"""
        return self.start

    def get_accept_states(self):
        """Returns a list of the accept states"""
        accept_states = []
        def count_accept(v):
            if v.is_accept():
                accept_states.append(v)
        self._dfs(count_accept)
        return accept_states

    def _dfs(self, op):
        # Preforms depth-first search on Automaton 
        # executes function 'op' on each of the visited states
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
        def vid(v):
            return str(id(v))[-3:]

        def print_v(v):
            out.add(str(v))
        self._dfs(lambda v: out.append(str(v)))
        return "\n".join(out)

class NFA(Automaton):
    """Non-deterministic finite automaton"""
    def __init__(self, start_state):
        super(NFA,self).__init__(start_state)

    def null_closure(self, states):
        """returns the null-closure of a set of state in the NFA"""
        # returns the null-closure of a single state
        def null_closure_single(state):
            nc = set()
            def null_closure_recur(v):
                nc.add(v)
                for u in v.get_null_transitions():
                    null_closure_recur(u)
            null_closure_recur(state)
            return nc

        nc = set()
        for s in states:
            nc |= null_closure_single(s)
        return nc

    def transition(self, states, trans):
        """ Given a set of states S and a transition t in the NFA returns a
            set of next states that would be reached from S via transition t 
        """
        next_states = set()
        for s in states:
            nxt = s.get_transition(trans)
            if nxt:
                next_states.add(nxt)
        return next_states

    def transition_values(self, states):
        """ returns all alphabet values that have transitions defined in the
        given set of NFAStates"""
        vals = set()
        for s in states:
            vals |= s.get_transition_values()
        return vals

    def to_dfa(self):
        """converts this NFA to a DFA and returns it"""
        #TODO: get test_NFA_to_DFA to pass
        # get start state
        start_substates = self.null_closure({self.get_start_state()})
        dfa_start = DFAState(start=True, accept=False, substates=start_substates)

        # create dfa with start state
        dfa = DFA(dfa_start)
        unmarked = [dfa_start]

        #add transitions to DFA
        while unmarked:
            curr_dfa_state = unmarked.pop()
            print curr_dfa_state
            curr_nfa_substates = curr_dfa_state.get_substates()
            for trans in self.transition_values(curr_nfa_substates):
                trans_nfa_states = self.null_closure(
                    self.transition(curr_nfa_substates, trans))
                
                if not dfa.in_dfa(trans_nfa_states):
                    trans_dfa_state = DFAState(substates=curr_nfa_substates)
                    curr_dfa_state.add_transition(trans_dfa_state, trans)
                    unmarked.append(trans_dfa_state)

        # set accept states in dfa
        for s in nfa.get_states():
            for sub in s.get_substates():
                if sub.is_accept():
                    s.set_accept(True)
                    continue
        return dfa

class DFA(Automaton):
    def __init__(self, start_state):
        super(DFA,self).__init__(start_state)

    def in_dfa(self, nfa_states):
        """ true if the DFA has a state that represents the given set of
        NFAStates"""
        # don't understand fully how closures work in python, 
        # so I'm resorting to this shameful hack
        match = []
        def find_match(v):
            if v.get_substates() == nfa_states:
                match.append(True)
        self._dfs(find_match)
        return bool(match)
