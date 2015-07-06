# -*- coding: utf-8 -*-
from bottle import route,run,template

#静的ルーティング
@route('/hello')
def hello():
    return template('Hello {{string}}',string='World')

#スクリプトファイルとして実行されたらサーバ起動
if __name__ == '__main__':
    run(host='localhost', port=8080,
        debug=True, reloader=True)
