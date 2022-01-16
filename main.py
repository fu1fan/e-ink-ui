import os, json, socket, sys, signal
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

def runCmd(cmd):
    pipe = os.popen(cmd)
    text = pipe.read()
    pipe.close()
    return text

def fileURL(path):
    return "file://"+os.path.abspath(path)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def getInfo():
    info = {}
    info["ip"] = get_host_ip()
    wifistr = runCmd("sudo iwlist wlan0 scan | grep ESSID")
    info["WIFI"] = wifistr.replace("ESSID:", "").replace("\"", "").replace("\n", ", ").replace("\\x00", "")
    return json.dumps(info)

mousePos=[0,0]

imgOld = [None]
imgOld[0] = Image.open("resources/about.png")

if __name__ == "__main__":
    print("主程序启动，在web模式下运行。")
    # 记录时间戳
    startTime = time()
    env = enviroment.Env()
    print("内核启动中...")
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

    def pi_api_handler():
        msg = browser.execute_script("return window.piapi.msg")
        if (msg != "okk") and (msg != None):
            print("收到API消息：",msg)
            if msg == "updateImage":
                print("即将更新屏幕...")
                updateImage()
            elif msg == "getInfo":
                print("传入设备信息...")
                print(getInfo())
                jsonMsg = {}
                jsonMsg["msg"] = "getInfo"
                jsonMsg["data"] = getInfo()
                jsonMsg = json.dumps(jsonMsg)
                browser.execute_script("window.piapi.piCallback("+jsonMsg+")")
            elif msg == "log":
                print("接受到js的log消息：",end="")
                print(browser.execute_script("return window.piapi.logmsg"))
            elif msg == "stop":
                print("接受到stop指令，即将关闭程序...")
                pid = os.getpid()
                print('pid : ',pid)
                env.Screen.display(Image.open("resources/terminated.png"))
                browser.quit()
                os.kill(pid,signal.SIGKILL)
            elif msg == "reboot":
                print("接受到reboot指令，即将重启...")
                env.Screen.display(Image.open("resources/poweroff.png"))
                browser.quit()
                os.system("sudo reboot")
            elif msg == "poweroff":
                print("接受到poweroff指令，即将关机...")
                env.Screen.display(Image.open("resources/poweroff.png"))
                browser.quit()
                os.system("sudo poweroff")
            elif msg == "runCmd":
                cmdText = browser.execute_script("return window.piapi.cmd")
                print("接受到runCmd指令，即将执行命令：",cmdText)
                cmdResult = runCmd(cmdText)
                print("命令执行结果：",cmdResult)
                jsonMsg = {}
                jsonMsg["msg"] = "runCmd"
                jsonMsg["data"] = cmdResult
                jsonMsg = json.dumps(jsonMsg)
                browser.execute_script("window.piapi.piCallback("+jsonMsg+")")
            elif msg == "refreshScreen":
                print("接受到refreshScreen指令，即将全局刷新屏幕...")
                updateImage(refresh=True)


            browser.execute_script("window.piapi.msg = 'okk'")


    def pi_api_interval():
        while 1:
            sleep(0.05)
            try:
                pi_api_handler()
            except:
                print("api出了点小问题，但关系不是很大。")



    pi_api_thread = threading.Thread(target=pi_api_interval, daemon=True)
    pi_api_thread.start()

    def load_url(url):
        print("加载URL：",url)
        browser.get(url)
        print("加载成功。")

    def load_local_url(url):
        print("加载本地文件：",url)
        load_url(fileURL(url))

    load_local_url("pages/main.html")
    print("主页面渲染完成，耗时：",time()-time2)
    print("一共用时：",time()-startTime)
    def updateImage(refresh=False):
        try:
            screenshot = browser.get_screenshot_as_png()
            screenshotImg = Image.open(BytesIO(screenshot))
            # 判断是否需要全局刷新
            if refresh:
                # 全局刷新
                print("屏幕全局刷新...")
                env.Screen.display(screenshotImg)
            else:
                # 局部刷新
                # 判断是否和imgOld相同
                if imgOld[0].tobytes() != screenshotImg.tobytes():
                    # 需要局部刷新
                    imgOld[0] = screenshotImg
                    print("屏幕局部刷新...")
                    env.Screen.display_auto(screenshotImg)
                else:
                    print("屏幕未变化，不刷新。")

        except:
            print("屏幕更新出错，可能是因为网络原因。")


    updateImage(refresh=True)
 
    touch_recoder_dev = enviroment.touchscreen.TouchRecoder()
    touch_recoder_old = enviroment.touchscreen.TouchRecoder()
    
    def touchHandler(now, old):
        # 按下
        if old.Touch == 0 and now.Touch == 1:
            mousePos[0] = now.X[0]
            mousePos[1] = now.Y[0]

        elif old.Touch == 1 and now.Touch == 0:
        # 抬起
            x = now.X[0]
            y = now.Y[0]
            if is_near(x,mousePos[0]) and is_near(y,mousePos[1]):
                print("屏幕点击事件: "+str(mousePos))
                clickByXY(mousePos[0], mousePos[1])

            else:
                print("屏幕滑动事件: "+str(mousePos)+" -> ["+str(x)+","+str(y)+"]")
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
            print("向下翻页")
        elif y<w-10:
            ac.send_keys(Keys.UP)
            ac.send_keys(Keys.UP)
            print("向上翻页")
            
        if x>z+10:
            ac.send_keys(Keys.RIGHT)
            ac.send_keys(Keys.RIGHT)
            print("向右翻页")
        elif x<z-10:
            ac.send_keys(Keys.LEFT)
            ac.send_keys(Keys.LEFT)
            print("向左翻页")
        
        ac.perform()


    while 1:
        env.Touch.icnt_scan(touch_recoder_dev, touch_recoder_old)
        touchHandler(touch_recoder_dev, touch_recoder_old)