#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from nose.tools import *

from todoitem import ToDoItem
from todocontainer import ToDoContainer

todos = ToDoContainer()

for d in range(19, 0, -1):
    td = ToDoItem('title %d' % d, 'desc %d' % d, datetime(2009, 10, d))
    todos += td

assert_equal(len(todos), 19)
assert_equal(todos[0].duedate.year, 2009)
assert_equal(todos[0].duedate.day, 1)
assert_equal(todos[5].duedate.day, 6)
del todos[5]
assert_equal(todos[5].duedate.day, 7)

assert_equal(len(todos.get_remaining_todos()), 18)

print todos.todos.index(todos.get_remaining_todos()[2])

todos[2].finish()
todos[3].finish()
todos[4].finish()

assert_equal(len(todos.get_remaining_todos()), 15)

start = datetime(2009, 10, 2)
end = datetime(2009, 10, 5)

assert_equal(len(todos.get_todo_in_date(start, end)), 4)

