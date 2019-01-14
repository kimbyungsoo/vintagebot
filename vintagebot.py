import win32gui, win32api, win32con, win32com.client
import sys
import time
import bonovista.bonovista
from importlib import reload
import sqlite3 as lite

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
    #shell.SendKeys('%')
    win32gui.SetForegroundWindow(hWnd)
    time.sleep(0.5)
    #win32api.SetCursorPos((904,512))
    mouse_click(904,512)
    time.sleep(1)
    shell.SendKeys(msg)
    time.sleep(1)
    #shell.SendKeys('{ENTER}')
    mouse_click(1199,512)
    time.sleep(1)


def diff_set(filename):
    conn = lite.connect(filename)
    cs = conn.cursor()
    query = "SELECT url FROM goods WHERE name NOT IN (SELECT DISTINCT name FROM old_goods)"
    updated_goods = cs.execute(query).fetchall()
    return list(updated_goods)

def main():
    if sys.version[0] == '2':
        reload(sys)
        sys.setdefaultencoding("utf-8")
    
    bonovista.bonovista.main()

    updated_goods = diff_set('./bonovista/bonovista.db')
    for good in updated_goods:
    	print(good[0])
    	sendmsg('테스트', good[0])

   

if __name__ == '__main__':
    main()