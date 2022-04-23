from PIL import Image, ImageOps
import pytesseract
import time
import pyscreenshot as ImageGrab
import re
import pyautogui
import numpy
import math

#FOR WINDOWS
#pytesseract.pytesseract.tesseract_cmd = '<full-path-to-tesseract-executable>'

a = 0.5  #probabily of heads if fair
b = 0.75 #probability of heads if weighted
A0 = 0.5 #initial probability of fair
B0 = 0.5 #intial probability of weighted

#SETTING COORDINATES
coords = numpy.loadtxt("coords.txt")
ht1x,ht1y=      coords[0 ][0],coords[0 ][1]
ht2x,ht2y=      coords[1 ][0],coords[1 ][1]
flip1x,flip1y=  coords[2 ][0],coords[2 ][1]
fairx,fairy=    coords[3 ][0],coords[3 ][1]
cheatx,cheaty=  coords[4 ][0],coords[4 ][1]
flip5x,flip5y=  coords[5 ][0],coords[5 ][1]
fl1x,fl1y=      coords[6 ][0],coords[6 ][1]
fl2x,fl2y=      coords[7 ][0],coords[7 ][1] 
namex,namey=    coords[8 ][0],coords[8 ][1]
emailx,emaily=  coords[9 ][0],coords[9 ][1]
submitx,submity=coords[10][0],coords[10][1]
resetx,resety=  coords[11][0],coords[11][1]
animx,animy=    coords[12][0],coords[12][1]
score1x,score1y=coords[13][0],coords[13][1]
score2x,score2y=coords[14][0],coords[14][1]

#MANUAL COORDINATE ENTRY:
# ht1x,ht1y=913,467
# ht2x,ht2y=1069,542
# flip1x,flip1y=831,882
# fairx,fairy=818,1004
# cheatx,cheaty=1037,1006
# flip5x,flip5y=1041,891
# fl1x,fl1y=1053,806
# fl2x,fl2y=1207,843
# namex,namey=915,782
# emailx,emaily=931,849
# submitx,submity=927,917
# resetx,resety=86,82
# animx,animy=763,948

name_for_leaderboard = "sean"
email_for_plushie = "seanrichardson98@gmail.com"


def prob_fair(n,k):
    binom = math.comb(n,k)
    return (binom*a**k*(1-a)**(n-k)*A0)/(A0*binom*a**k*(1-a)**(n-k)+B0*binom*b**k*(1-b)**(n-k))

def type_name():
    time.sleep(.5)
    pyautogui.moveTo(namex, namey)
    time.sleep(.5)
    pyautogui.click()
    time.sleep(.5)
    pyautogui.typewrite(name_for_leaderboard)

def type_email():
    time.sleep(.5)
    pyautogui.moveTo(emailx,emaily)
    time.sleep(.5)
    pyautogui.click()
    time.sleep(.5)
    pyautogui.typewrite(email_for_plushie)

def click_submit():
    time.sleep(.5)
    pyautogui.moveTo(submitx,submity)
    time.sleep(.5)
    pyautogui.click()

def click_reset():
    time.sleep(.5)
    pyautogui.moveTo(resetx,resety)
    time.sleep(.5)
    pyautogui.click()

def click_animate():
    time.sleep(.5)
    pyautogui.moveTo(animx,animy)
    time.sleep(.5)
    pyautogui.click()

def flip5():
    pyautogui.moveTo(flip5x, flip5y)
    pyautogui.click()

def flip():
    pyautogui.moveTo(flip1x, flip1y)
    pyautogui.click()

def label_as_cheater():
    pyautogui.moveTo(cheatx, cheaty)
    pyautogui.click()

def label_as_fair():
    pyautogui.moveTo(fairx, fairy)
    pyautogui.click()

def text_to_heads_tails(image_text):
    result = re.findall(r'\d+', image_text)
    if len(result) < 2:
        return 0,0
    return int(result[0]), int(result[1])

def get_heads_tails():
    image = ImageGrab.grab(bbox=(ht1x, ht1y, ht2x, ht2y))
    image = numpy.invert(image)
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    return text_to_heads_tails(image_to_text)

def engine_no_flips_left(heads,tails):
    if prob_fair(heads+tails,heads) >= 0.5:
        label_as_fair()
    label_as_cheater()
    return True

def engine(heads,tails):
    just_guessed = True
    thresh = 0.75
    if prob_fair(heads+tails,heads) >= thresh:
        label_as_fair()
    elif prob_fair(heads+tails,heads) <= 1-thresh:
        label_as_cheater()
    else:
        flip()
        just_guessed = False
    return just_guessed

def get_score():
    image = ImageGrab.grab(bbox=(score1x, score1y, score2x, score2y))
    image = numpy.invert(image)
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    num = int("".join(filter(str.isdigit, image_to_text)))
    return num

def get_flips_left():
    image = ImageGrab.grab(bbox=(fl1x, fl1y, fl2x, fl2y))
    image = numpy.invert(image)
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    num = int("".join(filter(str.isdigit, image_to_text)))
    if not (image_to_text[0]).isdigit():
        num = -1*num
    return num

def game_is_over():
    if get_flips_left() < 0:
        return True
    elif get_flips_left() == 0 and screenshot_heads_tails() == (0,0):
        return True
    else:
        return False

def reset_procedure():
    time.sleep(5)
    type_name()
    type_email()
    click_submit()
    time.sleep(30)
    click_reset()
    time.sleep(20)
    click_animate()

def reset_check():
    if game_is_over():
        reset_procedure()

if __name__ == "__main__":
    just_guessed = False
    score = get_score()
    flips0 = 100
    flips1 = 100
    while True:
        #BEGINNING OF NEW ROUND
        flips0 = flips1
        flips_used = 0
        if flips0 < 0:
            reset_procedure()
        while True:
            #LOOP FOR EACH ROUND
            ht = get_heads_tails()
            #engine
            if flips0-flips_used <= 0:
                just_guessed = engine_no_flips_left(ht[0],ht[1])
            elif flips0-flips_used == 30:
                flip()
            else: 
                just_guessed = engine(ht[0],ht[1])
            flips_used += 1
            if just_guessed:
                #end of round
                time.sleep(1)
                flips_used -= 1
                flips1 = get_flips_left()
                if flips1 < 0:
                    #if game is over
                    reset_procedure()
                    flips1 = 100
                    score = 0
                    break
                if -1*flips_used < flips1-flips0:
                    score += 1
                break