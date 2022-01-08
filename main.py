import os
from time import sleep
import enviroment
from PIL import Image


if __name__ == "__main__":
    print("Running In Web Mode")
    env = enviroment.Env()
    img = Image.new("RGB", (296,128), "black")
    env.Screen.display_auto(img)
