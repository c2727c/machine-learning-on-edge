#coding:utf-8
#python 3.5

import time
class A:
	def __init__(self):
		self.a = 0
	def update_pro(self,num):
		self.a=num


number = 1

def start():
	global number
	while(True):
		number+=1
		time.sleep(1)
