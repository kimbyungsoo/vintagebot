import win32gui, win32api, win32con, win32com.client
import sys, os
import bonovista.bonovista, augustshop.augustshop, matchmade.matchmade, previn.previn, oddpeople.oddpeople, rocketsalad.rocketsalad, stayfree.stayfree, festinalente.festinalente, wildhogs.wildhogs, cemeterypark.cemeterypark
from importlib import reload
import sqlite3 as lite
from time import ctime, sleep

def window_handle_Title(Title):
    handle = win32gui.FindWindow(None, Title)
    return handle

def mouse_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    return 0


def sendmsg(room, msg):
    hWnd = window_handle_Title(room)
    win32gui.SetForegroundWindow(hWnd)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hWnd)
    mouse_click(3112,896)
    sleep(1)
    shell.SendKeys(msg)
    sleep(1)
    #shell.SendKeys('{ENTER}')
    mouse_click(3155,891)
    sleep(1)
    return True


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
    	msg = name + " products have been updated : "+url
    	print(msg)
    	sendmsg(room, msg = msg)

    return True

site_list = [

    		{'room':'heavydutyclub', 'name':'bonovista', 'url':'http://www.bonovista.com/', 'module' : bonovista.bonovista}
    		, {'room':'heavydutyclub', 'name':'augustshop', 'url':'http://august-shop.kr', 'module' : augustshop.augustshop}
    		, {'room':'heavydutyclub', 'name':'matchmade', 'url':'http://match-made.co.kr/', 'module' : matchmade.matchmade}
    		, {'room':'heavydutyclub', 'name':'previn', 'url':'http://www.previn.co.kr/', 'module' : previn.previn}
    		, {'room':'heavydutyclub', 'name':'oddpeople', 'url':'http://oddpeople.kr/', 'module' : oddpeople.oddpeople}
    		#, {'room':'테스트', 'name':'rocketsalad', 'url':'http://www.rocketsalad.co.kr/', 'module' : rocketsalad.rocketsalad}
    		, {'room':'heavydutyclub', 'name':'stayfree', 'url':'http://stay-free.co.kr/', 'module' : stayfree.stayfree}
    		, {'room':'heavydutyclub', 'name':'festinalente', 'url':'http://www.festinalente.kr/', 'module' : festinalente.festinalente}
    		, {'room':'heavydutyclub', 'name':'wildhogs', 'url':'http://www.wildhogs.co.kr/', 'module' : wildhogs.wildhogs}
    		, {'room':'heavydutyclub', 'name':'cemeterypark', 'url':'http://cemeterypark.kr/', 'module' : cemeterypark.cemeterypark}
    		]


def main():
    print(ctime())
    if sys.version[0] == '2':
        reload(sys)
        sys.setdefaultencoding("utf-8")

    for site in site_list:
    	if(site['module'].main() == 0):
    		if (run(str(site['room']), site['name'], site['url'])):
    			print("SUCCESS")
    	else:
    		print( site['name'] + "ERROR")

if __name__ == '__main__':
    main()