import logging



def b_str(bytes):
    l = [hex(ord(i)) for i in bytes]
    b_str = ""
    for i in l:
        b_str += "<"+i+">"
    return b_str
