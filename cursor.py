import win32api
from time import sleep
while True:
	print(win32api.GetCursorPos())
	sleep(0.5)
	