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

    def adj(self):
        for k,v in self.transitions.items():
            yield k,v

    def get_transition(self, trans):
        return self.transitions.get(trans, None)

    def get_transition_values(self):
        return {k for k,v in self.transitions.items()}

    def set_accept(self, accept):
        self.accept = bool(accept)

    def clone(self):
        s = type(self)(self.is_start(), self.is_accept())
        self._clone = s
        for t,v in self.transitions.items():
            # this to stop back edges creating infinite recursion
            nxt = v._clone if hasattr(v,"_clone") else v.clone()
            s.add_transition(nxt,t)
        del self._clone
        return s

    def __str__(self):
        def vid(v):
            return str(id(v))[-3:]
        format_str = "%s (start: %s, accept: %s): t[%s]"

        trans = ["%s->%s"%(t,vid(n)) for t,n in self.transitions.iteritems()]
        return format_str % (vid(self),self.is_start(),self.is_accept(),
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

    def adj(self):
        for k,v in super(NFAState,self).adj():
            yield k,v
        for v in self.get_null_transitions():
            yield None,v

    def get_null_transitions(self):
        return self.null_transitions

    def clone(self):
        s = super(NFAState,self).clone()
        for v in self.get_null_transitions():
            s.add_transition(v.clone())
        return s

    def __str__(self):
        def vid(v):
            return str(id(v))[-3:]
        null_trans = "nt[%s]" % ",".join(
                [vid(v) for v in self.get_null_transitions()])
        return "%s %s" % (super(NFAState,self).__str__(), null_trans)

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

    def get_states(self):
        """returns a list of states in the Automaton"""
        states = []
        self._dfs(lambda v: states.append(v))
        return states

    def clone(self):
        """ returns another NFA that is a copy of this one """
        start = self.get_start_state().clone()
        return type(self)(start)

    def _dfs(self, op):
        # Preforms depth-first search on Automaton 
        # executes function 'op' on each of the visited states
        def dfs_recur(v):
            op(v)
            v._visited = True
            for trans,u in v.adj():       
                assert u
                if not hasattr(u, "_visited"):
                    dfs_recur(u)

        def reset_visited(v):
            delattr(v, "_visited")
            for trans,u in v.adj():
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
            curr_nfa_substates = curr_dfa_state.get_substates()
            for trans in self.transition_values(curr_nfa_substates):
                trans_nfa_substates = self.null_closure(
                    self.transition(curr_nfa_substates, trans))
                trans_dfa_state = dfa.get_state_by_substate(trans_nfa_substates)
                if not trans_dfa_state:
                    trans_dfa_state = DFAState(substates=trans_nfa_substates)
                    unmarked.append(trans_dfa_state)
                curr_dfa_state.add_transition(trans_dfa_state, trans)

        # set accept states in dfa
        for s in dfa.get_states():
            for sub in s.get_substates():
                if sub.is_accept():
                    s.set_accept(True)
                    continue
        return dfa


class DFA(Automaton):
    def __init__(self, start_state):
        super(DFA,self).__init__(start_state)

    def get_state_by_substate(self, nfa_substates):
        """ returns the state that has the given NFA substate """
        for s in self.get_states():
            if s.get_substates() == nfa_substates:
                return s
        return None
