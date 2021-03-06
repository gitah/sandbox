import unittest
from automaton import State, NFAState, NFA, DFAState, DFA
import regex as re

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
        self.assertEquals(set(s1.adj()), {("a",s3),(None,s2)})

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

        # clone
        new_nfa = nfa.clone()
        p1 = new_nfa.get_start_state()
        p2 = p1.get_transition("a")
        p3 = p1.get_null_transitions()[0]
        p4 = p3.get_transition("b")
        p5 = p4.get_transition("a")
        p6 = p4.get_null_transitions()[0]
        p7 = p6.get_transition("b")
        self.assertTrue(p1 and p2 and p3 and p4 and p6)
        self.assertTrue(p1.is_start())

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

class RegexParserTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def get_input_cases(self):
        t1 = r"ab"
        t2 = r"(a|b)"
        t3 = r"(a|b)a+"
        t4 = r"(a|b)*cd"
        t5 = r"(a|b)*fo\+"
        #t6 = r"((a|b)*aba*)*(a|b)(a|b)"
        t6 = r"\w\w\s[+*]?[5-9]"
        t7 = r"(a|b)+@vic\.(ca|com)"
        t8 = r"(abc)(def)+"
        t9 = r"^(ab){3,5}$"
        return (t1,t2,t3,t4,t5,t6,t7,t8,t9)

    def test_postfix(self):
        t1,t2,t3,t4,t5,t6,t7,t8,t9 = self.get_input_cases()
        self.assertEquals(re.postfix(t1), "ab&")
        self.assertEquals(re.postfix(t2), "ab|")
        self.assertEquals(re.postfix(t3), "ab|a+&")
        self.assertEquals(re.postfix(t4), "ab|*cd&&")
        self.assertEquals(re.postfix(t5), "ab|*fo\+&&&")
        self.assertEquals(re.postfix(t6), "\w\w\s[+*]?[5-9]&&&&")
        self.assertEquals(re.postfix(t7), "ab|+@vic\\.ca&com&&|&&&&&&")
        self.assertEquals(re.postfix(t8), "abc&&def&&+&")
        self.assertEquals(re.postfix(t9), "^ab&{3,5}$&&")

    def test_nfa(self):
        t1,t2,t3,t4,t5,t6,t7,t8,t9 = self.get_input_cases()
        nfa1 = re.postfix_to_nfa(re.postfix(t1))
        nfa2 = re.postfix_to_nfa(re.postfix(t2))
        nfa3 = re.postfix_to_nfa(re.postfix(t3))
        nfa4 = re.postfix_to_nfa(re.postfix(t4))
        nfa5 = re.postfix_to_nfa(re.postfix(t5))

        self.assertEquals(len(nfa1.get_accept_states()), 1)
        self.assertEquals(len(nfa2.get_accept_states()), 2)
        self.assertEquals(len(nfa3.get_accept_states()), 1)
        self.assertEquals(len(nfa4.get_accept_states()), 1)
        self.assertEquals(len(nfa5.get_accept_states()), 1)

    def test_match(self):
        t1,t2,t3,t4,t5,t6,t7,t8,t9 = self.get_input_cases()
        self.assertTrue(re.match(t1, "ab"))
        self.assertFalse(re.match(t1, "ba"))

        self.assertTrue(re.match(t2, "a"))
        self.assertTrue(re.match(t2, "b"))
        self.assertTrue(re.match(t2, "af"))
        self.assertFalse(re.match(t2, "fa"))

        self.assertTrue(re.match(t3, "aa"))
        self.assertTrue(re.match(t3, "ba"))
        self.assertTrue(re.match(t3, "aaaaaaaaaaaaa"))
        self.assertTrue(re.match(t3, "aaaaafoobar"))
        self.assertFalse(re.match(t3, "foobaraaaaa"))
        self.assertFalse(re.match(t3, "a"))

        self.assertTrue(re.match(t4, "aabababbacd"))
        self.assertTrue(re.match(t4, "cd"))
        self.assertFalse(re.match(t4, "abaa"))
        self.assertFalse(re.match(t4, "bbbbc"))

        self.assertTrue(re.match(t5, r"baafo\+"))
        self.assertFalse(re.match(t5, "baafo+"))

        self.assertTrue(re.match(t6, "xy +7"))
        self.assertTrue(re.match(t6, "02 *8"))
        self.assertTrue(re.match(t6, "_D 9"))
        self.assertFalse(re.match(t6, "Tz +1"))
        self.assertFalse(re.match(t6, "@y +9"))

        self.assertTrue(re.match(t7, r"ab@vic\.ca"))

        self.assertTrue(re.match(t9, r"ababab"))
        self.assertTrue(re.match(t9, r"abababab"))
        self.assertTrue(re.match(t9, r"ababababab"))
        self.assertFalse(re.match(t9, r"ab"))
        self.assertFalse(re.match(t9, r"abab"))
        self.assertFalse(re.match(t9, r"abababababab"))
        self.assertFalse(re.match(t9, r"abababababt"))
        self.assertFalse(re.match(t9, r"tababababab"))

    def test_search(self):
        t1,t2,t3,t4,t5,t6,t7,t8,t9 = self.get_input_cases()
        self.assertTrue(re.search(t4, "abcdfoobar"))
        self.assertTrue(re.search(t4, "foobarabcdfoobar"))
        self.assertTrue(re.search(t4, "__arabcd"))
        self.assertFalse(re.search(t4, "zarafce"))

        self.assertTrue(re.search(t8, "xzvfabcdefdefdeffffff"))
        self.assertFalse(re.search(t8, "xzvfabc"))

        self.assertTrue(re.search(t9, "ababab"))
        self.assertFalse(re.search(t9, "ttttabababzzzz"))


if __name__ == "__main__":
    unittest.main()
