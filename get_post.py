# -*- coding: utf-8 -*-

from bottle import route, get, post, run, template, request

@get('show_query')
def show_query():
    keyword = request.query.leyword
    return template('keyword={{keyword}}.',keyword=keyword)

@post('show_form')
def show_form():
    name = request.forms.get('name')
    return template('name={{name}}.', name=name)

@post('show_file')
def show_file():
    upload_file = request.files.get('name')
    return template('file_name={{file_name}}.',filename=upload_file.file_name)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)

