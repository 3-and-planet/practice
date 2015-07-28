#!/usr/bin/env python
# coding=utf-8

# 標準ライブラリをインポート
from datetime import datetime
from pickle import dump, load

# GUIライブラリをインポート
from Tkinter import *
import tkMessageBox

# データ用のクラスをインポート
from todoitem import ToDoItem
from todocontainer import ToDoContainer

# データ保存用ファイル名
DUMPFILE = 'todo.dat'

class ToDoApp(Frame):
    """
    ToDo GUIアプリ用のクラス
    """
    def __init__(self, master=None):
        """
        初期化メソッド - ウィジェットやToDoのデータを初期化
        """
        Frame.__init__(self, master, padx=8, pady=4)
        self.pack()
        self.createwidgets()        # ウィジェットを作る
        t = self.winfo_toplevel()
        t.resizable(False, False)   # Windowをサイズ変更できなくする
        self.load()                 # データをロードする
        sec = datetime.now().second # タイマーを設定
        self.after((60-sec)*1000, self.refreshitems)
        self.sel_index = -1

    def createwidgets(self):
        """
        ボタンなどウインドウの部品を作る
        """
        # スクロールバーつきListboxを作る
        self.frame1 = Frame(self)
        frame = self.frame1

        self.listbox = Listbox(frame, height=10, width=30,
                               selectmode=SINGLE, takefocus=1)
        self.yscroll = Scrollbar(frame, orient=VERTICAL)

        # 配置を決める
        self.listbox.grid(row=0, column=0, sticky=NS)
        self.yscroll.grid(row=0, column=1, sticky=NS)

        # 動きとコードをつなげる
        self.yscroll.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.yscroll.set)
        self.listbox.bind("<ButtonRelease-1>", self.selectitem)

        self.frame1.grid(row=0, column=0)

        # 予定編集エリア，ボタンを作る
        self.frame2 = Frame(self)
        frame = self.frame2
        self.title_l = Label(frame, text="タイトル")
        self.description_l = Label(frame, text="詳細")
        self.duedate_l = Label(frame, text="締め切り")
        self.title_e = Entry(frame, justify=LEFT, width=20)
        self.description_e = Entry(frame, justify=LEFT, width=20)
        self.duedate_e = Entry(frame, justify=LEFT, width=20)
        self.finished_v = IntVar()
        self.finished_c = Checkbutton(frame, justify=LEFT, text=u"終了",
                                      variable=self.finished_v)
        self.update_button = Button(frame, text=u"更新", state=DISABLED,
                                    command=self.updateitem)
        self.delete_button = Button(frame, text=u"削除", state=DISABLED,
                                    command=self.deleteitem)
        self.new_button = Button(frame, text=u"新規",
                                 command=self.createitem)

        # 配置を決める
        self.title_l.grid(row=0, column=0, columnspan=2)
        self.title_e.grid(row=1, column=0, columnspan=2)
        self.description_l.grid(row=2, column=0, columnspan=2)
        self.description_e.grid(row=3, column=0, columnspan=2)
        self.duedate_l.grid(row=4, column=0, columnspan=2)
        self.duedate_e.grid(row=5, column=0, columnspan=2)
        self.finished_c.grid(row=6, column=0, columnspan=2)
        self.update_button.grid(row=7, column=0)
        self.delete_button.grid(row=7, column=1)
        self.new_button.grid(row=8, column=0, columnspan=2)

        self.frame2.grid(row=0, column=1)

    def load(self):
        """
        ToDoのデータをファイルから読み込む
        """
        try:
            f = open(DUMPFILE, 'r')
            self.todos = load(f)
        except IOError:
            self.todos = ToDoContainer()

    def save(self):
        """
        ToDoのデータをファイルに書き出す
        """
        f = open(DUMPFILE, 'w')
        dump(self.todos, f)

    def setlistitems(self):
        """
        ToDoのうち未消化分をリストに表示する
        """
        self.listbox.delete(0, END)
        for todo in self.todos.get_remaining_todos():
            d = todo.duedate
            t = todo.title.ljust(20)
            if todo.duedate < datetime.now():
                t = '* '+t      # ToDoの期限が過ぎていたら*を前につける
            item = "%s %4d/%02d/%02d %02d:%02d" % (
                t, d.year, d.month, d.day, d.hour, d.minute)
            self.listbox.insert(END, item)

    def refreshitems(self):
        """
        タイマーで定期的に呼び出されるメソッド
        ToDoのうち時間になったものがあればダイアログで知らせる
        """
        dirty = False
        for todo in self.todos.get_remaining_todos():
            td = datetime.now()
            d = todo.duedate
            if (d.year == td.year == td.year and d.month == td.month and
                d.day == td.day and d.hour == td.hour and
                d.minute == td.minute):
                msg = u"%sの時間です。\n %s\n %s" % (
                        todo.title, todo.description,
                        todo.duedate.strftime('%Y/%m%d %H:%M'))
                tkMessageBox.showwarning(u"時間です", msg)
                dirty = True
        sec = datetime.now().second
        self.after((60-sec)*1000, self.refreshitems)

        if dirty:
            self.setlistitems()

    def clearentries(self):
        """
        予定入力フィールドを消去する
        """
        self.title_e.delete(0, END)
        self.description_e.delete(0, END)
        self.duedate_e.delete(0, END)
        self.finished_c.deselect()

    def selectitem(self, event):
        """
        Listboxで項目が選択されたときに呼ばれるメソッド
        入力フィールドに選択された項目を反映する
        """
        self.delete_button.config(state=NORMAL)
        self.update_button.config(state=NORMAL)
        for idx in self.listbox.curselection():
            i = int(idx)
            self.sel_index = i
            td = self.todos.get_remaining_todos()[i]
            self.clearentries()
            self.title_e.insert(0, td.title)
            self.description_e.insert(0, td.description)
            ddtxt = td.duedate.strftime('%Y/%m/%d %H:%M')
            self.duedate_e.insert(0, ddtxt)
            if td.finished:
                self.finished_c.select()
            else:
                self.finished_c.deselect()

    def refrectententries(self, todo):
        """
        フィールドに入力された文字列をToDoItemインスタンスに反映する
        """
        todo.title = self.title_e.get()
        todo.description = self.description_e.get()
        dt = datetime.strptime(self.duedate_e.get()+':00',
                               '%Y/%m/%d %H:%M:%S')
        todo.duedate = dt
        if self.finished_v.get() != 0:
            todo.finish()

    def createitem(self):
        """
        新しいToDOアイテムを作る
        """
        todo = ToDoItem('', '', datetime.now())
        self.refrectententries(todo)
        self.todos += todo
        self.clearentries()
        self.setlistitems()
        self.sel_index = -1
        self.save()

    def updateitem(self):
        """
        入力フィールドの情報を選択中のToDOアイテムに反映する
        """
        if self.sel_index != -1:
            i = self.sel_index
            todo = self.todos.get_remaining_todos()[i]
            self.todos.sort()
            self.refrectententries(todo)
            self.sel_index = -1
            self.clearentries()
            self.setlistitems()
            self.save()

    def deleteitem(self):
        """
        Listboxで選択されているToDoのアイテムを消去する
        """
        for idx in self.listbox.curselection():
            i = int(idx)
            todo = self.todos.get_remaining_todos()[i]
            real_idx = self.todos.todos.index(todo)
            del self.todos[real_idx]
            self.todos.sort()
            self.clearentries()
            self.setlistitems()
            self.save()


def main():
    """
    アプリケーションを動かす関数
    """
    root = Tk()
    app = ToDoApp()         # ToDoAppインスタンスを作る
    
    app.setlistitems()      # Listboxの項目を揃える
    app.mainloop()          # アプリケーションの処理を開始する
    root.destroy()

if __name__ == '__main__':
    main()

