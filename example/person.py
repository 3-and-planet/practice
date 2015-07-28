#-*-coding:utf-8-*-

class Person(object):
	def __init__(self,n,w):
		self.n=n
		self.w=w
	def say(self):
		print u"%sと%s" %(self.n,self.w)
