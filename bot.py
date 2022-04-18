# TESSERACT
from PIL import Image, ImageOps
import pytesseract

import keyboard
import time
import pyscreenshot as ImageGrab
import re
import pyautogui

import math

a = 0.5  #probabily of heads if fair
b = 0.75 #probability of heads if weighted
A0 = 0.5 #initial probability of fair
B0 = 0.5 #intial probability of weighted

def prob_fair(n,k):
    binom = math.comb(n,k)
    return (binom*a**k*(1-a)**(n-k)*A0)/(A0*binom*a**k*(1-a)**(n-k)+B0*binom*b**k*(1-b)**(n-k))

def type_name():
    time.sleep(.5)
    pyautogui.moveTo(1000, 780)
    time.sleep(.5)
    pyautogui.click()
    time.sleep(.5)
    pyautogui.typewrite("sean")

def type_email():
    time.sleep(.5)
    pyautogui.moveTo(1000,840)
    time.sleep(.5)
    pyautogui.click()
    time.sleep(.5)
    pyautogui.typewrite("seanrichardson98@gmail.com")

def click_submit():
    time.sleep(.5)
    pyautogui.moveTo(1000,900)
    time.sleep(.5)
    pyautogui.click()

def click_reset():
    time.sleep(.5)
    pyautogui.moveTo(1000,1050)
    time.sleep(.5)
    pyautogui.click()

def flip5():
    pyautogui.moveTo(1200, 900)
    pyautogui.click()

def flip():
    pyautogui.moveTo(800, 900)
    pyautogui.click()

def label_as_cheater():
    pyautogui.moveTo(1200, 1000)
    pyautogui.click()
    time.sleep(2)

def label_as_fair():
    pyautogui.moveTo(800, 1000)
    pyautogui.click()
    time.sleep(2)

def text_to_heads_tails(image_text):
    if image_text == "":
        return 0,0
    result = re.findall(r'\d+', image_text)
    return int(result[0]), int(result[1])

def screenshot_heads_tails():
    im = ImageGrab.grab(bbox=(920, 425, 1100, 500))
    im = ImageOps.invert(im)
    im.save("temp/image.png")
    image = Image.open('temp/image.png')
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    return text_to_heads_tails(image_to_text)

def engine_no_flips_left(heads,tails):
    if prob_fair(heads+tails,heads) >= 0.5:
        label_as_fair()
    label_as_cheater()

def engine(heads,tails):
    thresh = 0.75
    if prob_fair(heads+tails,heads) >= thresh:
        label_as_fair()
    elif prob_fair(heads+tails,heads) <= 1-thresh:
        label_as_cheater()
    else:
        flip()

def bad_engine(heads,tails):
    thresh = 0.9
    if prob_fair(heads+tails,heads) >= thresh:
        label_as_cheater()
    elif prob_fair(heads+tails,heads) <= 1-thresh:
        label_as_fair()
    else:
        flip5()

def get_flips_left():
    im = ImageGrab.grab(bbox=(1060, 800, 1200, 850))
    im = ImageOps.invert(im)
    save_name = "temp/num_flips.png"
    im.save(save_name)
    image = Image.open(save_name)
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    num = int("".join(filter(str.isdigit, image_to_text)))
    if not (image_to_text[0]).isdigit():
        num = -1*num
    return num

def game_is_over():
    if get_flips_left() < 0:
        return True
    else:
        return False

def game_is_over2():
    im = ImageGrab.grab(bbox=(700, 500, 1200, 600))
    im = ImageOps.invert(im)
    save_name = "temp/game_over_check.png"
    im.save(save_name)
    image = Image.open(save_name)
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    print(image_to_text)
    print(image_to_text == "Game Over")
    if image_to_text == "Game Over\n":
        return True
    return False
    # return text_to_heads_tails(image_to_text)

# time.sleep(2)
# while True:
#     time.sleep(0.5)
#     print(get_flips_left())
#     print(game_is_over())


time.sleep(2)
while True:
    while True:
        time.sleep(0.5)
        print("click!")
        if (game_is_over()):
            break
        ht = screenshot_heads_tails()
        if get_flips_left() > 0:
            engine(ht[0],ht[1])
        else:
            engine_no_flips_left(ht[0],ht[1])

    time.sleep(5)
    type_name()
    type_email()
    click_submit()
    time.sleep(30)
    click_reset()
    time.sleep(5)


#STUFF:
# time.sleep(2)
# while True:
#     time.sleep(1)
#     if keyboard.is_pressed('q'):  # if key 'q' is pressed 
#         break  # finishing the loop
#     ht = screenshot_heads_tails()
#     engine(ht[0],ht[1])


# # ImageGrab.grab_to_file('images/im.png')

# #KEYPRESS:
# # while True:
# #     time.sleep(1)
# #     print("test1")
# #     if keyboard.is_pressed('q'):  # if key 'q' is pressed 
# #         print('You Pressed A Key!')
# #         break  # finishing the loop

# #TESSERACT:
# image = Image.open('temp/image.png')
# image_to_text = pytesseract.image_to_string(image, lang='eng')
# print(heads_tails(image_to_text))

