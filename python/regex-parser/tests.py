import unittest
from automaton import State, NFAState, NFA, DFAState, DFA

class TestAutomaton(unittest.TestCase):
    def setUp(self):
        pass

    def test_State(self):
        s1 = State()
        self.assertFalse(s1.is_start())
        self.assertFalse(s1.is_accept())

        s1.set_accept(True)
        self.assertTrue(s1.is_accept())

    def test_NFAState(self):
        s1 = NFAState()
        s2 = NFAState()
        s3 = NFAState()
        s1.add_transition(s2)
        s1.add_transition(s3, "a")

        self.assertTrue(s1.get_null_transitions()[0] == s2)
        self.assertTrue(s1.get_transition("a") == s3)
        self.assertEquals(s1.get_adj(), {s3,s2})

    def build_nfa(self):
        # ( a+ | b(a|b) )
        s1 = NFAState(start=True, accept=False)
        s2 = NFAState(start=False, accept=True)
        s3 = NFAState(start=False, accept=False)
        s4 = NFAState(start=False, accept=False)
        s5 = NFAState(start=False, accept=True)
        s6 = NFAState(start=False, accept=False)
        s7 = NFAState(start=False, accept=True)

        s1.add_transition(s2,"a")
        s1.add_transition(s3)
        s2.add_transition(s2,"a")
        s3.add_transition(s4,"b")
        s4.add_transition(s5,"a")
        s4.add_transition(s6)
        s6.add_transition(s7,"b")

        nfa = NFA(s1)
        return nfa

    def test_NFA(self):
        nfa = self.build_nfa()

        s1 = nfa.get_start_state()
        s2 = s1.get_transition("a")
        s3 = s1.get_null_transitions()[0]
        s4 = s3.get_transition("b")
        s5 = s4.get_transition("a")
        s6 = s4.get_null_transitions()[0]
        s7 = s6.get_transition("b")

        # ensure nfa setup properly
        self.assertTrue(s1 and s2 and s3 and s4 and s6)
        self.assertTrue(s1.is_start())

        # getters + setters
        self.assertEquals(len(nfa.get_accept_states()), 3)

        # null closure methods
        self.assertEquals(nfa.null_closure({s1}), {s1,s3})
        self.assertEquals(nfa.null_closure({s1,s4}), {s1,s3,s4,s6})

        # transition methods
        self.assertEquals(nfa.transition({s1},"a"), {s2})
        self.assertEquals(nfa.transition({s1,s2,s3,s4},"a"), {s2,s5})
        self.assertEquals(nfa.transition_values({s1,s2,s3}), {"a","b"})

    def test_DFA(self):
        s1 = NFAState()
        s2 = NFAState()
        s3 = NFAState()
        s4 = NFAState()
        s1.add_transition(s2)
        s1.add_transition(s3, "a")

        t = DFAState(substates={s1,s2,s3})
        self.assertEquals(t.get_substates(), {s1,s2,s3})

        dfa = DFA(t)
        self.assertFalse(dfa.get_state_by_substate({s1,s2}))
        self.assertTrue(dfa.get_state_by_substate({s1,s2,s3}), t)

    def test_NFA_to_DFA(self):
        nfa = self.build_nfa()
        s1 = nfa.get_start_state()
        s2 = s1.get_transition("a")
        s3 = s1.get_null_transitions()[0]
        s4 = s3.get_transition("b")
        s5 = s4.get_transition("a")
        s6 = s4.get_null_transitions()[0]
        s7 = s6.get_transition("b")

        dfa = nfa.to_dfa()
        d1 = dfa.get_start_state()
        d2 = d1.get_transition("a")
        d3 = d1.get_transition("b")
        d4 = d3.get_transition("a")
        d5 = d3.get_transition("b")

        self.assertTrue(d1 and d2 and d3 and d4 and d5)
        self.assertEquals(d2.get_transition("a"), d2)
        self.assertEquals(d1.get_substates(), {s1,s3})
        self.assertEquals(d2.get_substates(), {s2})
        self.assertEquals(d3.get_substates(), {s4,s6})
        self.assertEquals(d4.get_substates(), {s5})
        self.assertEquals(d5.get_substates(), {s7})


if __name__ == "__main__":
    unittest.main()
