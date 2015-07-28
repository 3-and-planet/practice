# coding=utf-8

# モジュールをインポート
from datetime import datetime, timedelta

class ToDoContainer(object):
    """
    ToDo項目のリストを保存するためのクラス
    """

    def __init__(self):
        """
        ToDo項目のリストのインスタンスを初期化する
        """
        self.todos = []

    def __len__(self):
        """
        ToDo項目の数を返す
        """
        return len(self.todos)

    def sort(self):
        """
        ToDoを締め切り日でソートする
        """
        self.todos.sort(lambda x,y : cmp(x.duedate, y.duedate))

    def __add__(self, item):
        """
        「+」演算子をエミュレートして，ToDo項目を追加する
        """
        self.todos.append(item)
        self.sort()

    def __iadd__(self, item):
        """
        「+=」演算子をエミュレートして，ToDo項目を追加する
        """
        self.__add__(item)
        return self

    def __getitem__(self, idx):
        """
        インデックスアクセスをエミュレートする
        """
        return self.todos[idx]

    def __setitem__(self, idx, item):
        """
        インデックスの代入ををエミュレートする
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


