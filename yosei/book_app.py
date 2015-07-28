#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import bottle
from bottle import get, post, run
from bottle import request, template, redirect
from bottle import HTTPError

from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, UnicodeText
from sqlalchemy.ext.declarative import declarative_base

from bottle.ext import sqlalchemy

from wtforms.form import Form
from wtforms import validators
from wtforms import StringField, IntegerField, TextAreaField


#bottle-sqlalchemy設定

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

plugin = sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',     #関数内で挿入される場合の変数名
    create=True,      #テーブルを作成するか
    commit=True,      #関数終了時にトランザクションをコミットするか
    use_kwargs=False
)

bottle.install(plugin)

#セッションインスタンスの挿入
#@post('/books/add')
#def create(db):       #引数dbにセッションインスタンスが自動で挿入される


#テーブルのモデル作成
class Book(Base):

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(100), nullable=False)
    price = Column(Integer, nullable=False)
    memo = Column(UnicodeText)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return "<Book('%s','%s','%s','%s')>" % (self.title, self.price, self.memo, self.created_at)


#フォームの作成
class BookForm(Form):
    
    title = StringField('タイトル',[
        validators.required(message="入力してください"),
        validators.length(min=1, max=100, message="100文字以下で入力してください")
    ])

    price = IntegerField('価格',[
        validators.required(message="数値で入力してください")
    ])

    memo = TextAreaField('memo',[
        validators.required(message="入力してください")
    ])


#書籍登録画面の表示
@get('/books/add')
def new(db):

    #BookFormインスタンスの作成
    form = BookForm()

    #edit.tplの描画
    return template('edit', form=form, request=request)

#書籍の登録処理
@post('/books/add')
def create(db):

    #bookformインスタンスの生成
    form = BookForm(request.forms.decode())

    #フォームのバリデーション
    if form.validate():

        #bookインスタンスの作成
        book = Book(
            title=form.title.data,
            price=form.price.data,
            memo=form.memo.data
        )

        #bookの保存
        db.add(book)

        #一覧画面へリダイレクト
        redirect("/books")
    else:
        return template('edit', books=books, request=request)

#書籍の一覧画面の表示
@get('/books')
def index(db):

    # booksテーブルから全件取得
    books = db.query(Book).all()

    # index,tplの描画
    return template('index', books=books, request=request)


#書籍の編集画面の表示
@get('/books/<id:int>/edit')
def edit(db, id):

    book = db.query(Book).get(id)

    if not book:
        return HTTPError(404, 'Book is not found.')

    form = BookForm(request.POST, book)

    return template('edit', book=book, form=form, request=request)


#書籍の更新処理
@post('/books/<id:int>/edit')
def update(db, id):

    book = db.query(Book).get(id)

    if not book:
        return HTTPError(404, 'Book is not found.')

    form = BookForm(request.forms.decode())

    if form.validate():

        book.title = form.title.data
        book.price = form.price.data
        book.memo = form.memo.data

        redirect("/books")

    else:
        return template('edit', form=form, request=request)


#書籍の削除処理
@post('/books/<id:int>/delete')
def destroy(db, id):

    book = db.query(Book).get(id)

    if not book:
        return HTTPError(404, 'Book is not found.')

    db.delete(book)

    redirect("/books")


#サーバ起動
if __name__ == '__main__':
        run(host='localhost', port=8080, debug=True, reloader=True)



