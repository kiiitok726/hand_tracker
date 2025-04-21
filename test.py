import pyautogui
import time

for i in range(200):
    # print(time.time())
    x = time.time()
    pyautogui.moveTo(500+i, 500+i, _pause=False) 
    print(time.time()-x)