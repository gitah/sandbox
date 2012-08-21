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
        #TODO: explicit_transitions

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
        self.assertTrue(dfa.in_dfa(s1))
        self.assertFalse(dfa.in_dfa(s2))

    def test_NFA_to_DFA(self):
        nfa = self.build_nfa()
        self.fail("not implemented yet")


if __name__ == "__main__":
    unittest.main()
