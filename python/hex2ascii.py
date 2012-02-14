# hex2ascii.py
# Converts a hexstring to ascii
# 
# Author: Fred Song 

import sys
import binascii

def usage():
    print "usage: %s HEXSTRING [delimiter]" % sys.argv[0]

if len(sys.argv) < 2:
    usage()
    exit(1)

hexstr = sys.argv[1]
if len(hexstr)%2 != 0:
    hexstr = '0'+hexstr
try: 
    delim = sys.argv[2]
    if len(delim) > 1:
        raise Exception()
except:
    delim = ''

try:
    hexstr = ''.join(hexstr.split(delim))
except:
    pass

ascii_str = str(binascii.unhexlify(hexstr))

print ascii_str
