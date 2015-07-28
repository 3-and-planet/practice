#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

class Birthday:
	def birth(self,name,day):

		self.name=name
		self.birthday=datetime(day)
		print "誕生日が登録されました"

		tenthou=self.birthday+datetime.timedelta(10000)
		week=self.birthday.weekday()
		print week+"が貴方の生まれた曜日です。"
		print tenthou+"が貴方の誕生１万日記念日です"





