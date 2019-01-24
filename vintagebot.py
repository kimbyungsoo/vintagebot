import win32gui, win32api, win32con, win32com.client
import sys, os
import time
import bonovista.bonovista, augustshop.augustshop, matchmade.matchmade, previn.previn, oddpeople.oddpeople, rocketsalad.rocketsalad, stayfree.stayfree, festinalente.festinalente
from importlib import reload
import sqlite3 as lite
from time import ctime

def window_handle_Title(Title):
    handle = win32gui.FindWindow(None, Title)
    return handle

def mouse_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def sendmsg(roomname, msg):
    hWnd = window_handle_Title(roomname)
    win32gui.SetForegroundWindow(hWnd)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hWnd)
    time.sleep(0.5)
    #win32api.SetCursorPos((904,512))
    mouse_click(3112,896)
    time.sleep(1)
    shell.SendKeys(msg)
    time.sleep(1)
    #shell.SendKeys('{ENTER}')
    mouse_click(3155,891)
    time.sleep(1)


def diff_set(filename):
    conn = lite.connect(filename)
    cs = conn.cursor()
    query = "SELECT url FROM goods WHERE img NOT IN (SELECT DISTINCT img FROM old_goods)"
    updated_goods = cs.execute(query).fetchall()
    conn.close()
    return list(updated_goods)

def run(room, name, url):
    db = './'+name+'/'+name+'.db'
    updated_goods = diff_set(db)
    if len(updated_goods) != 0:
    	msg = name + "products have been updated : "+url
    	print(msg)
    	sendmsg(room, msg = msg)

site_list = [
    		{'room':'heavydutyclub', 'name':'bonovista', 'url':'http://www.bonovista.com/'}
    		, {'room':'heavydutyclub', 'name':'augustshop', 'url':'http://august-shop.kr'}
    		, {'room':'테스트', 'name':'matchmade', 'url':'http://match-made.co.kr/'}
    		, {'room':'heavydutyclub', 'name':'previn', 'url':'http://www.previn.co.kr/'}
    		, {'room':'heavydutyclub', 'name':'oddpeople', 'url':'http://oddpeople.kr/'}
    		, {'room':'테스트', 'name':'rocketsalad', 'url':'http://www.rocketsalad.co.kr/'}
    		, {'room':'테스트', 'name':'stayfree', 'url':'http://stay-free.co.kr/'}
    		, {'room':'테스트', 'name':'festinalente', 'url':'http://www.festinalente.kr/'}
    		]


def main():
    print(ctime())
    if sys.version[0] == '2':
        reload(sys)
        sys.setdefaultencoding("utf-8")

    bonovista.bonovista.main()
    augustshop.augustshop.main()
    matchmade.matchmade.main()
    previn.previn.main()
    oddpeople.oddpeople.main()
    rocketsalad.rocketsalad.main()
    stayfree.stayfree.main()
    festinalente.festinalente.main()

    for site in site_list:
    	run(site['room'], site['name'], site['url'])

if __name__ == '__main__':
    main()