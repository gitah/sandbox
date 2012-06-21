# Answer:
# 1 + 1 + 5 + 3 + 7 + 2 + 1 = 20

def int_gen():
    i = 1
    while True:
        yield i
        i += 1;

def frac_gen():
    for i in int_gen():
        digits = str(i) #str() method deals with radix trickery
        for d in digits:
            yield int(d)

sum = 0
operands = [10**i for i in xrange(0,7)]
num = 1
for d in frac_gen():
    if num in operands:
        print d
        sum += d
    if num > 10**6:
        break
    num+=1

print sum
