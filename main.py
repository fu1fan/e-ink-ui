import os
from time import sleep
from time import time
import enviroment
from PIL import Image, ImageDraw, ImageFont
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from io import BytesIO
from selenium.webdriver.chrome.options import Options
import threading
chrome_options = Options()

# 无头模式启动
chrome_options.add_argument('--headless')

# 关闭沙箱以便root运行
chrome_options.add_argument("--no-sandbox")

def fileURL(path):
    return os.path.abspath(path)

mousePos=[0,0]

imgOld = [None]
imgOld[0] = Image.open("resources/about.png")

if __name__ == "__main__":
    print("主程序启动，在web模式下运行。")
    # 记录时间戳
    startTime = time()
    env = enviroment.Env()
    print("浏览器内核启动中。")
    def loadImgThread():
        env.Screen.display(Image.open("resources/start1.png"))
        sleep(1)
        env.Screen.display_auto(Image.open("resources/start2.png"))
        sleep(2)
        env.Screen.display_auto(Image.open("resources/start3.png"))
    threading.Thread(target=loadImgThread).start()
    browser = webdriver.Chrome(options=chrome_options)
    time2 = time()
    print("内核启动成功，耗时：",time2-startTime)
    # 设置页面大小为296x128
    browser.set_window_size(296, 128)

    def load_url(url):
        print("加载URL：",url)
        browser.get(url)
        print("加载成功。")
        # 判断是否支持jsbridge
        if browser.execute_script("return window.jsbridge"):
            print("页面支持jsbridge。")
        else:
            print("页面不支持jsbridge。")

    load_url("https://playground.xuanzhi33.cn/pi-core/test/")
    print("主页面渲染完成，耗时：",time()-time2)
    print("一共用时：",time()-startTime)
    def updateImage(refresh=False):
        screenshot = browser.get_screenshot_as_png()
        screenshotImg = Image.open(BytesIO(screenshot))
        # 判断是否和imgOld相同
        if imgOld[0].tobytes() != screenshotImg.tobytes():
            imgOld[0] = screenshotImg
            print("更新屏幕……")
            if refresh:
                env.Screen.display(screenshotImg)
            else:
                env.Screen.display_auto(screenshotImg)
        else:
            # print("same image")
            pass

    sleep(0.5)
    updateImage(refresh=True)
 
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

            else:
                print("slide: "+str(mousePos)+" -> ["+str(x)+","+str(y)+"]")
                slideByXYZW(mousePos[0], mousePos[1], x, y)


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
            ac.send_keys(Keys.DOWN)
            ac.send_keys(Keys.DOWN)
            print("page down")
        elif y<w-10:
            ac.send_keys(Keys.UP)
            ac.send_keys(Keys.UP)
            print("page up")
            
        if x>z+10:
            ac.send_keys(Keys.RIGHT)
            ac.send_keys(Keys.RIGHT)
            print("page right")
        elif x<z-10:
            ac.send_keys(Keys.LEFT)
            ac.send_keys(Keys.LEFT)
            print("page left")
        
        ac.perform()



    def updateImageInterval():
        while 1:
            updateImage()
            sleep(0.3)

    threading.Thread(target=updateImageInterval).start()

    while 1:
        env.Touch.icnt_scan(touch_recoder_dev, touch_recoder_old)
        touchHandler(touch_recoder_dev, touch_recoder_old)