# -*- coding:utf-8 -*-

from datetime import datetime, timedelta

class ToDoContainer(object):
    """
    ToDo項目のリストを保存するためのクラス
    """

    def __init__(self):
        """
        インスタンス初期化
        """
        self.todos = []

    def __len__(self):
        """
        ToDo項目の数を返す
        """
        return len(self.todos)

    def sort(self):
        """
        ToDoを締切日でソートする
        """
        self.todos.sort(key = lambda x : x.duedate)

    def __add__(self, item):
        """
        +演算子をエミュレートしてToDo項目を追加する
        """
        self.todos.append(item)
        self.sort()

    def __iadd__(self, item):
        """
        +=演算子をエミュレートしてToDo項目を追加する
        """
        self.__add__(item)
        return self

    def __getitem__(self, idx):
        """
        インデックスアクセスをエミュレートする
        """
        return self.todos[idx]

    def __selfitem__(self, idex, item):
        """
        インデックスの代入をエミュレートする
        """
        self.todos[idx] = item
        self.sort()

    def __delitem__(self, idx):
        """
        インデックスを指定したdelをエミュレートする
        """
        del self.todos[idx]

    def get_remaining_todos(self):
        """
        終了していないToDo項目をリストとして返す
        """
        return [t for t in self.todos if not t.finished]

