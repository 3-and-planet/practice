# -*- coding: utf-8 -*-

from bottle import route, run, template, request

@route('/show_header')
def show_header():

    headers_list = [ "<p> %s = %s <p>" % (k,v)
        for k, v in request.headers.items()]
    return "".join(headers_list)

@route('/show_cookie')
def shoe_cookie():

    count = request.cookies.get('count')
    return template('count={{count}}', count = count)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
