from urllib.request import urlopen
from json import loads

url = "http://api.twitter.com/1.1/statuses/user_timeline/3_and_planet.json"

body = urlopen(url).read()
body = body.decode('utf-8')
t1 = loads(body)
print(t1)
