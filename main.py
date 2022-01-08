import os
from time import sleep
import enviroment
from PIL import Image
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from io import BytesIO
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# 无头模式启动
chrome_options.add_argument('--headless')

mousePos=[0,0]

if __name__ == "__main__":
    print("Running In Web Mode")
    env = enviroment.Env()
    img = Image.open("resources/about.png")
    env.Screen.display(img)
    browser = webdriver.Chrome(options=chrome_options)

    browser.get("https://playground.xuanzhi33.cn/pi-core/menu/")
    # 设置页面大小为296x128
    browser.set_window_size(296, 128)
    sleep(0.5)
    screenshot = browser.get_screenshot_as_png()

    screenshotImg = Image.open(BytesIO(screenshot))
    env.Screen.display(screenshotImg)
 
    touch_recoder_dev = enviroment.touchscreen.TouchRecoder()
    touch_recoder_old = enviroment.touchscreen.TouchRecoder()
    
    def touchHandler(now, old):
        # 按下
        if (old.Touch == 0 and now.Touch == 1):
            mousePos[0] = now.X[0]
            mousePos[1] = now.Y[0]

        elif (old.Touch == 1 and now.Touch == 0):
        # 抬起
            x = now.X[0]
            y = now.Y[0]
            if is_near(x,mousePos[0]) and is_near(y,mousePos[1]):
                print("click: "+str(mousePos))
                clickByXY(mousePos[0], mousePos[1])
                sleep(0.2)
                updateImage()
                sleep(0.8)
                updateImage()

            else:
                print("slide: "+str(mousePos)+" -> ["+str(x)+","+str(y)+"]")
                slideByXYZW(mousePos[0], mousePos[1], x, y)
                sleep(0.2)
                updateImage()

    # 判断两个数字是否相差5以内
    def is_near(a, b):
        return abs(a - b) < 5

    def clickByXY(x, y):
        ac = ActionChains(browser)
        ac.move_by_offset(x, y)
        ac.click()
        ac.move_by_offset(-x, -y)
        ac.perform()

    def slideByXYZW(x, y, z, w):
        ac = ActionChains(browser)
        if y>w+10:
            ac.send_keys(Keys.PAGE_DOWN)
            print("page down")
        elif y<w-10:
            ac.send_keys(Keys.PAGE_UP)
            print("page up")
            
        if x>z+10:
            ac.send_keys(Keys.RIGHT)
            print("right")
        elif x<z-10:
            ac.send_keys(Keys.LEFT)
            print("left")
        
        ac.perform()

    def updateImage():
        screenshot = browser.get_screenshot_as_png()
        screenshotImg = Image.open(BytesIO(screenshot))
        env.Screen.display_auto(screenshotImg)


    while 1:
        env.Touch.icnt_scan(touch_recoder_dev, touch_recoder_old)
        touchHandler(touch_recoder_dev, touch_recoder_old)