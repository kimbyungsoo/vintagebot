import threading
from bs4 import BeautifulSoup
#import urllib.request             # HTTP Request and Response
#from urllib.parse import quote    # UTF-8 to ASCII for URL
from urllib.parse import urlparse, parse_qs # URL Parsing
import requests
import re
import json
import sqlite3 as lite
import time

class AsyncWildhogsTask:
	def __init__(self):
		self.SHOP_URL = "http://m.wildhogs.co.kr"
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
		self.goods = []
	def requesUrl(self):
		list_html = requests.get(url=self.SHOP_URL, headers=self.headers).content
		list_lxml = BeautifulSoup(list_html, 'lxml', from_encoding='utf-8')
		url_list = [self.SHOP_URL+i.get('href') for i in list_lxml.select('ul.prdList.grid3 > li.xans-record- > div.description > strong.name > a')]
		img_list = ['http:'+i.get('src') for i in list_lxml.select('ul.prdList.grid3 > li.xans-record- > div.thumbnail > a > img')]
		name_list = [i.find_all(text=True)[0] for i in list_lxml.select('ul.prdList.grid3 > li.xans-record- > div.description > strong.name > a')]
		for i in range(len(name_list)):
			self.goods.append({'url' : url_list[i], 'img' : img_list[i], 'name' : name_list[i]})
		self.saveDB()

	def saveDB(self):
		if len(self.goods) == 0:
			print("goods is empty")
		else:
			database_filename = './wildhogs/wildhogs.db'
			conn = lite.connect(database_filename)
			cs = conn.cursor()
			#DROP
			query = "CREATE TABLE IF NOT EXISTS goods (name VARCHAR(255), url VARCHAR(255), img VARCHAR(255))"
			cs.execute(query)
			query = "DROP TABLE IF EXISTS old_goods"
			cs.execute(query)
			query = "ALTER TABLE goods RENAME TO old_goods"
			cs.execute(query)
			query = "CREATE TABLE IF NOT EXISTS goods (name VARCHAR(255), url VARCHAR(255), img VARCHAR(255))"
			cs.execute(query)
			for good in self.goods:
				query = "INSERT into goods (name,url,img) values (?, ?, ?)"
				cs.execute(query,(str(good['name']), str(self.SHOP_URL+good['url']),str(self.SHOP_URL+good['img'])))
			conn.commit()
			print("good is updated")
			conn.close()

def main():
	print ('wildhogs bot start')
	BT = AsyncWildhogsTask()
	BT.requesUrl()
	#threading.Timer(60, BT.requesUrl()).start() 
	return 0

if __name__ == '__main__':
	main()

