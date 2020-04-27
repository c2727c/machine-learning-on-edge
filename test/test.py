
import struct
import os
from lib.TLV import *
from lib.macro import *
import pickle

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


#
# def f11():
# 	pass
#
# def f12():
# 	print('f12!\n')
# 	return 'f12!\n'
#
# def f21():
# 	pass
#
# def f22():
# 	pass
#
# MSG_DIC = {1:[f11,f12],2:[f21,f22]}
#
# f = MSG_DIC[1][1]
# f()


#
#
#
# SEND_DATA_REQ=100
# STRUCTMAP = {SEND_DATA_REQ:'10sl'}
#
# FILEPATH = '2727c.html'
# print("file name :{}\nfile size:{}\n".format(FILEPATH,os.stat(FILEPATH).st_size))
# buf = struct.pack(STRUCTMAP[SEND_DATA_REQ],bytes(FILEPATH, encoding = "utf-8"),
# 							os.stat(FILEPATH).st_size)
# print("data---(10sl)pack---> buf:\n{}".format(buf))
#
# tlv_obj = TLV(t_ext=7, l_ext=7)
# tlv_obj.add(SEND_DATA_REQ,str(buf, encoding = "utf-8"))
# print("\nbuf---wrap--->tlv:\n{}".format(tlv_obj.buffer))
#
# tlvp = TLVParser(tlv_obj.buffer, t_ext=7, l_ext=7)
# print("\ntlv---unwrap--->t,l,v_buf:")
# for avp in tlvp.parse():
# 	print(avp)
# 	filename,filesize = struct.unpack(STRUCTMAP[SEND_DATA_REQ],bytes(avp['value'], encoding = "utf-8"))
# 	filename = filename.strip(b'\00')
# 	print("(12sl)upacked data:\n{},{}".format(filename, filesize))
#
#
#
# print("(12sl)unwrap tlv:\n{}".format(buf))
# filename,filesize = struct.unpack('12sl',buf)
# filename = filename.strip(b'\00')
# filename = str(filename,encoding='utf-8')
# print("(12sl)upacked data:\n{},{}".format(filename,filesize))



# s = '2727c.html'
# bs = b'2727c.html'
# l = 100
# print(s,bytes(s,encoding='utf-8'),bs,str(bs,encoding='utf-8'))
#
# # struct.pack('10sl',bstr,100)
# pk = struct.pack('10sl',bs,l)
# print(pk)
# upk = struct.unpack('10sl',pk)
# print(upk)
# print(upk[0])
# print(str(upk[0],encoding='utf-8'))

#
# amap = {1:"20000000000",2000:"10000000000",333:3300}
# print(amap)
# print(type(amap))
# print(sys.getsizeof(amap))
# print('-----------')
# pkd = pickle.dumps(amap)
# print(b_str(pkd))
# print(type(pkd))
# print(len(pkd))
# print(sys.getsizeof(pkd))
# print('-----------')
# pkl = pickle.loads(pkd)
# print(pkl)
# print(type(pkl))


# import logging
# logging.basicConfig(level=logging.NOTSET)
# logging.debug(u"ZZZZZZZZZZ")


# d = {('107.0.0.1',9000):0}
# print(d.has_key(('107.0.0.1',9000)))
# print(d.has_key(('107.0.0.2',9000)))
# print(d[('107.0.0.2',9000)])



class A:
	def __init__(self,aa):
		self.a = aa

	def print_f(self):
		print('A:',self.a)

class B(A):
	def __init__(self,aa,bb):
		A.__init__(self,aa)
		self.b = bb

	def print_f(self):
		print('A:',self.a)
		print('B:', self.b)

a = A(3)
a.print_f()

b = B(1,2)
b.print_f()