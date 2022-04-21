from PIL import Image, ImageOps
import pytesseract
import time
import pyscreenshot as ImageGrab
import re
import pyautogui
import numpy
import math

ht1x,ht1y=913,467
ht2x,ht2y=1069,542

times = []

def text_to_heads_tails(image_text):
    result = re.findall(r'\d+', image_text)
    if len(result) < 2:
        return 0,0
    return int(result[0]), int(result[1])

def screenshot_heads_tails():
    times.append(time.time()) #1
    image = ImageGrab.grab(bbox=(ht1x, ht1y, ht2x, ht2y))
    times.append(time.time()) #2
    image = numpy.invert(image)
    times.append(time.time()) #3 
    #image.save("temp/image.png")
    #image = Image.open('temp/image.png')
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    times.append(time.time()) #4
    return text_to_heads_tails(image_to_text)

time.sleep(2)
screenshot_heads_tails()
print(numpy.diff(times))