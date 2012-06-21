#Answer: 
#a=200 b=375 c=425
#abc = 31,875,000

import math
for a in xrange(0,1000):
    for b in xrange(0,1000):
        for c in xrange(0,1000):
            if a >= b or a >= c or b >= c:
                continue
            if a**2 + b**2 != c**2:
                continue
            if a + b + c == 1000:
                print a*b*c
                exit(0)
