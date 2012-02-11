# rot.py
# Preforms a caeser cipher

def rot_char(c,d):
    num = ord(c)
    if num >= ord('a') and num <= ord('z'):
        return chr(ord('a') + (num-ord('a')+d)%26)
    if num >= ord('A') and num <= ord('Z'):
        return chr(ord('A') + (num-ord('a')+d)%26)
    return c

def rot(msg,d=13):
    """Preforms a rotational cipher on a message
        
       msg - the message to encrypt
       d - rotation size, 13 by default
    """
    arr = list(msg)
    for i,c in enumerate(arr):
        arr[i] = rot_char(c,d)
    return ''.join(arr)


if __name__ == "__main__":
    # do tests
    print rot("a", 13)
    print rot("z", 13)
    print rot("a y z", 13)
    print rot("foo bar baz", 13)
