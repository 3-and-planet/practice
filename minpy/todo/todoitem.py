# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

class ToDoItem(object):
    """
    TODO項目を保村するためのクラス
    """

    def __init__(self, title, description, duedate, addeddate=None):

        if not addeddate:
            addeddate = datetime.now()

        self.title = title
        self.description = description
        self.duedate = duedate
        self.addeddate = addeddate
        self.finished = False
        self.finisheddate = None

    def finish(self, date = None):
        self.finished = True
        if not date:
            date = datetime.now()
            self.finisheddate = date

    def __repr__(self):
        """
        TODO項目の表示形式文字列を作る
        """
        return "<ToDoItem {}, {}>".format(self.title, self.duedate.strftime('%Y/%m/%d %H:%M'))


