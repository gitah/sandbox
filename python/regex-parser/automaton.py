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
        def __init__(self, start=False, accept=False, substates=None):
            super(DFAState, self).__init__(start,accept)
            self.substates = substates if substates else []

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
        self.__dfs(count_accept)
        return accept_states

    def __dfs(self, op):
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
        self.__dfs(lambda v: out.append(str(v)))
        return "\n".join(out)

class NFA(Automaton):
    """Non-deterministic finite automaton"""
    def __init__(self, start_state):
        self.start = start_state

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
            nc = nc | null_closure_single(s)
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

class DFA(object):
    pass
