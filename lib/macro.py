def recv_all(socket, step = 2048):
	buffer = []
	while True:
		d = socket.recv(step)
		if d:
			buffer.append(d)
		else:
			break
	return b''.join(buffer)


# def receive_all(socket, buffer, step = 2048):

# 	while True:
# 		d = socket.recv(step)
# 		if d:
# 			buffer.append(d)
# 		else:
# 			break