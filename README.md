# E-Ink UI web

## 介绍

这是一个由python编写，基于树莓派Zero W的水墨屏天气时钟。
这个仓库是対原仓库[eink-clock-mP](https://gitee.com/fu1fan/eink-clock-mP)的重构，提高了运行效率和代码规范。

## 关于web分支
这个分支与Master分支有所不同，虽然主程序仍然使用Python编写，但是在UI层面采用了**HTML+js**开发，所以采用了chromium内核。原本以为树莓派zero w跑不动chromium，但是尝试了之后感觉体验还挺好，就开了个新分支。因为使用HTML+js开发界面比纯python写要简单（反正我是这么认为的），而且可以直接在电脑浏览器上调试，所以开发效率和调试效率都大大提升了。不足之处也是显而易见的，那就是开机会有点慢（与master分支相比慢了约13s），占用内存会有一点大，但是还是可以接受的。

## 如何体验

### 没有相关硬件

因为UI层面是基于html+js的，所以在没有硬件的情况下，可以直接在电脑浏览器上运行。
你只需要克隆本仓库并用浏览器打开根目录下的**simulator.html**，就可以快速的体验了。

![gkuho2_20220123](https://gitee.com/xuanzhi33/files/raw/master/files/gkuho2_20220123.png)

### 有相关硬件

和master分支相比，需要额外安装一个依赖：
```
pip3 install selenium
```
还得安装chromium：
```
sudo apt-get install chromium-browser
```
接下来就可以运行了：
```
sudo python3 main.py
```
