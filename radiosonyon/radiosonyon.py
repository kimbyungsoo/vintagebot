import threading, os
from bs4 import BeautifulSoup
#import urllib.request             # HTTP Request and Response
#from urllib.parse import quote    # UTF-8 to ASCII for URL
from urllib.parse import urlparse, parse_qs # URL Parsing
import requests
import re
import json
import sqlite3 as lite
import time

class AsyncRadiosonyonTask:
	def __init__(self):
		self.SHOP_URL = 'http://m.radiosonyon.com/product/list.html'
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
	def requesUrl(self, next_url, goods = []):
		next_url = next_url
		while(True):
			list_html = requests.get(url=self.SHOP_URL+next_url, headers=self.headers).content
			list_lxml = BeautifulSoup(list_html, 'lxml', from_encoding='utf-8')
			url_list = [self.SHOP_URL+i.get('href') for i in list_lxml.select('#contents > div.xans-element-.xans-product.xans-product-listnormal.typeThumb > ul > li > div > a')]
			img_list = ['http:'+i.get('src') for i in list_lxml.select('#contents > div.xans-element-.xans-product.xans-product-listnormal.typeThumb > ul > li > div > a > img')]
			name_list = [i.find_all(text=True)[0] for i in list_lxml.select('#contents > div.xans-element-.xans-product.xans-product-listnormal.typeThumb > ul > li > p.name')]
			for i in range(len(url_list)):
				goods.append({'url' : url_list[i], 'img' : img_list[i], 'name' : name_list[i]})

			next_url = list_lxml.select('#contents > div.xans-element-.xans-product.xans-product-normalpaging.paginate.typeList > p.next > a')[0].get('href')
			if(next_url == '#none'):
				print(len(goods))
				return goods


	def saveDB(self, goods = []):
		if len(goods) == 0:
			print("goods is empty")
		else:
			database_filename = './radiosonyon/radiosonyon.db'
			conn = lite.connect(database_filename)
			cs = conn.cursor()
			#DROP
			query = "CREATE TABLE IF NOT EXISTS goods (name VARCHAR(255), url VARCHAR(255), img VARCHAR(255));"
			cs.execute(query)
			query = "DROP TABLE IF EXISTS old_goods;"
			cs.execute(query)
			query = "ALTER TABLE goods RENAME TO old_goods;"
			cs.execute(query)
			query = "CREATE TABLE IF NOT EXISTS goods (name VARCHAR(255), url VARCHAR(255), img VARCHAR(255));"
			cs.execute(query)
			for good in goods:
				query = "INSERT into goods (name,url,img) values (?, ?, ?);"
				cs.execute(query,(str(good['name']), str(self.SHOP_URL+good['url']),str(self.SHOP_URL+good['img'])))
			conn.commit()
			conn.close()

def main():
	print ('Radiosonyon bot start')
	BT = AsyncRadiosonyonTask()
	url_list = ['?cate_no=7'
				,'?cate_no=12' 
				,'?cate_no=4'
				,'?cate_no=24'
				,'?cate_no=43'
				,'?cate_no=39'
				,'?cate_no=32'
			]

	goods = []
	for next_url in url_list:
		goods = BT.requesUrl(next_url, goods)
	BT.saveDB(goods = goods)
	#threading.Timer(60, BT.requesUrl()).start() 

if __name__ == '__main__':
	main()

