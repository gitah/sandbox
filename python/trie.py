# trie.py
# A implementation of the Trie data structure
# It is an efficient way of finding words starting with the same prefix
# See http://en.wikipedia.org/wiki/Trie for more details

# Adapted from this blog post:
#http://v1v3kn.tumblr.com/post/18238156967/
#roll-your-own-autocomplete-solution-using-tries

# Author: Fred Song, xx@uvic.ca

class Trie(object):
    def __init__(self, val=""):
        self.value = val
        self.children = {}
        self.flag = False

    def _add_child(self, char):
        val = self.value + char
        self.children[char] = Trie(val)

    def insert(self, word):
        """ Inserts a word into the Trie """
        node = self
        for char in word:
            if char not in node.children:
                node._add_child(char)
            node = node.children[char]
        node.flag = True

    def find(self, word):
        """ Returns True if word is in the Trie """
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def _get_all(self):
        results = set()
        if self.flag:
            results.add(self.value)
        for letter,node in self.children.iteritems():
            results = results.union(node.get_all())
        return results

    def autocomplete(self,prefix):
        """ Returns a set containing all the words in the Trie 
            with teh given prefix
        """
        node = self
        for c in prefix:
            if c not in node.children:
                return set()
            node = node.children[c]

        return node._get_all()


# run tests
if __name__ == "__main__":
    t = Trie()

    t.insert("foo")
    t.insert("bar")
    t.insert("baz")
    t.insert("foobar")

    assert t.find("foo") == True 
    assert t.find("bar") == True
    assert t.find("bat") == False

    assert "foo" in t.autocomplete("fo") 
    assert "foobar" in t.autocomplete("fo") 

    assert "bar" in t.autocomplete("ba") 
    assert "baz" in t.autocomplete("ba") 
    assert "bat" not in t.autocomplete("ba") 
