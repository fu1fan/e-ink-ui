import os
from time import sleep
import enviroment
from PIL import Image
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from io import BytesIO
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# 无头模式启动
chrome_options.add_argument('--headless')

if __name__ == "__main__":
    print("Running In Web Mode")
    env = enviroment.Env()
    img = Image.open("resources/about.png")
    env.Screen.display(img)
    browser = webdriver.Chrome(options=chrome_options)

    browser.get("https://playground.xuanzhi33.cn/pi-core/main/")
    # 设置页面大小为296x128
    browser.set_window_size(296, 128)
    sleep(0.5)
    screenshot = browser.get_screenshot_as_png()

    screenshotImg = Image.open(BytesIO(screenshot))
    env.Screen.display(screenshotImg)
 
    touch_recoder_dev = enviroment.touchscreen.TouchRecoder()
    touch_recoder_old = enviroment.touchscreen.TouchRecoder()
    while 1:
        env.Touch.icnt_scan(touch_recoder_dev, touch_recoder_old)
        print(touch_recoder_dev.Touch, touch_recoder_dev.X[0], touch_recoder_dev.Y[0])