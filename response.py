# -*- coding: utf-8 -*-

from bottle import get, run, response

@get('/set_response')
def set_response():
    response.status = 200

    response.set_header("Cache-Dontrol", "max-age=0")

    response.set_cookie("spam", "egg")

if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True,reloader=True)

