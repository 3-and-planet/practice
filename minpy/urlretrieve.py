# -*-coding:utf-8 -*-
from urllib import request
from urllib import parse
import sys

url = sys.argv[1]
filename = parse.urlparse(url)[2].split('/')[-1]

print(filename)
request.urlretrieve(url,filename)

