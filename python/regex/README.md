Introduction
============
This is my implementation of a Regular Expression (regex) parser in Python. It
is implemented using a Discrete Finite Automaton

Here is how it works:
    1. (<regex>,<string>) is given as input
    2. Convert <regex> to <postfix> form
    3. Build <NFA> from <postfix>
    4. Convert <NFA> to <DFA>
           see: http://web.cecs.pdx.edu/~harry/compilers/slides/LexicalPart3.pdf
    5. use <DFA> to match <regex> with <string>

Currently the parser supports:
    - quantity operators like: * + ?
    - the or operator: |
    - character classes: [abc], [^abc], \w, \s

Terminology
===========
Regex Terminology

    Character: a normal symbol like "a" or "b"

    Operator: a symbol with a special meaning
        - Divided into unary (ex. ?) and binary operators (ex. + |)

    Character Class: specifies a group of symbols
        - ex. . [abc] \w

    Escape: the '\' symbol
        - turns a special symbol into a character when paried
        - ex. \+ \[ \\

How to use
==========
Public Interfaces:

##regex.match(regex, string)
    - Searches <string> from the begining for the given <regex>
    - Returns true if the begining of the <string> matches the <regex>  
    - NOTE: the match starts at the begining of <string>

Example

    import regex as re
    re.match("www\.\w*\.(ca|com|net)", "www.example.com is my website") # returns true
    re.match("www\.\w*\.(ca|com|net)", "my website is www.example.com") # returns false

##regex.search(regex, string)
    - Searches any substring of <string> to see if it matches the <regex>
    - NOTE: the match can be anywhere in <string>

Example

    import regex as re
    re.match("www\.\w*\.(ca|com|net)", "www.example.com is my website") # returns true
    re.match("www\.\w*\.(ca|com|net)", "my website is www.example.com") # returns true

License
=======
I'm doing this just for fun; do what ever you like with the code

TODO
====
Implement capturing groups

Implment some sort of way to select greedy/non-greedy match

Implement regex.findall
