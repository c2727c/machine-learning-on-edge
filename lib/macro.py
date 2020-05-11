import logging
def recv_file(socket, filename, filesize, step=2048):
    recvsize = 0
    fp = open(filename, 'wb')
    while not recvsize == filesize:
        if filesize - recvsize > step:
            data = socket.recv(step)
        else:
            data = socket.recv(filesize - recvsize)
        recvsize += len(data)
        fp.write(data)
    fp.close()


def b_str(bytes):
    l = [hex(ord(i)) for i in bytes]
    b_str = ""
    for i in l:
        b_str += "<"+i+">"
    return b_str
