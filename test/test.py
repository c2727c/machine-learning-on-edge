# a = 2
# b1 = [1,2]
# b2 = [1,2]
# def func(a,b,c):
# 	a+=1
# 	b.append(3)
# 	c = [3,4]

# func(a,b1,b2)

# print a,b1,b2





# a = 3
# b = a
# a -= 1
# a = b
# print a,b
def f11():
	pass

def f12():
	print('f12!\n')
	return 'f12!\n'

def f21():
	pass

def f22():
	pass

MSG_DIC = {1:[f11,f12],2:[f21,f22]}

f = MSG_DIC[1][1]
f()