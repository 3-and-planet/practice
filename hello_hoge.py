# -*- coding: utf-8 -*-
from bottle import route,run,template

#動的ルーティング name
@route('/greeting/<name>')
def greeting(name):
    return template('Hello {{name}}',name=name)

#int
@route('/article/<id:int>')
def article(id):
    return template('id={{id}}',id=id)

#float
@route('/version/<no:float>')
def version(no):
    return template('no={{no}}',no=no)

#file_path
@route('/photo/<image_path:path>')
def photo(image_path):
    return template('image_path={{image_path}}',image_path=image_path)

#正規表現
@route('/search/<keyword:re:[a-z]+>')
def route(keyword):
    return template('keyword={{keyword}}',keyword=keyword)


#スクリプトファイルとして実行されたらサーバ起動
if __name__ == '__main__':
    run(host='localhost', port=8080,
        debug=True, reloader=True)
