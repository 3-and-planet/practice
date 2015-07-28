from bs4 import BeautifulSoup
import requests
r = requests.get('http://docs.python.jp/3/library/index.html')
soup = BeautifulSoup(r.content)
toctree =soup.find('div','toctree-wrapper')
links = toctree.find_all('a')
len(links)

for link in links[:5]:
	print (link.text)