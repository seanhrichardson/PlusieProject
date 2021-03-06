from PIL import Image, ImageOps, ImageGrab
import pytesseract
import time
import re
import pyautogui
import numpy
import math

#OPTIONAL
import os

GOAL = 3500
THRESH = 0.75

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

total_guesses = 0

#GLOBAL VARIABLES:
score_image = None
flips_image = None
ht_image = None
just_guessed = False

## int n: total number of flips
## int k: number of heads
## Returns: probability that the coin was fair, given the current number of flips and heads.
def prob_fair(n,k):
    binom = math.comb(n,k)
    return (binom*a**k*(1-a)**(n-k)*A0)/(A0*binom*a**k*(1-a)**(n-k)+B0*binom*b**k*(1-b)**(n-k))

## int n: total number of flips
## int k: number of heads
## Returns: minimum number of flips before we might reach a decision.
def min_needed_flips(n,k):
    num_tails_for_fair = 1
    while prob_fair(n+num_tails_for_fair,k) < THRESH:
        num_tails_for_fair += 1
    if num_tails_for_fair == 1:
        return num_tails_for_fair

    num_heads_for_bias = 1
    while prob_fair(n+num_heads_for_bias, k + num_heads_for_bias) > 1-THRESH:
        num_heads_for_bias += 1
    return min(num_tails_for_fair, num_heads_for_bias)

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

def submit_old_run():
    pyautogui.moveTo(1420,896)
    pyautogui.click()
    time.sleep(0.5)


def text_to_heads_tails(image_text):
    result = re.findall(r'\d+', image_text)
    if len(result) < 2:
        return 0,0
    return int(result[0]), int(result[1])

def get_heads_tails():
    image = ImageGrab.grab(bbox=(ht1x, ht1y, ht2x, ht2y))
    image = numpy.invert(image)
    # image = pyautogui.screenshot(region=(ht1x,ht1y, ht2x, ht2y))
    # image = numpy.invert(image)
    #image.save("temp/image.png")
    #image = Image.open('temp/image.png')
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    return text_to_heads_tails(image_to_text)

def engine_no_flips_left(heads,tails):
    if prob_fair(heads+tails,heads) >= 0.5:
        label_as_fair()
    label_as_cheater()
    return True

def engine(heads,tails):
    just_guessed = True
    flips_used = 0
    if prob_fair(heads+tails,heads) >= THRESH:
        label_as_fair()
    elif prob_fair(heads+tails,heads) <= 1-THRESH:
        label_as_cheater()
    else:
        num_to_flip = min_needed_flips(heads+tails,heads)
        for i in range(num_to_flip):
            flips_used += 1
            flip()
            time.sleep(0.05)
        just_guessed = False
    return just_guessed, flips_used

def bad_engine(heads,tails):
    just_guessed = True
    thresh = 0.90
    if prob_fair(heads+tails,heads) >= thresh:
        label_as_cheater()
    elif prob_fair(heads+tails,heads) <= 1-thresh:
        label_as_fair()
    else:
        flip()
        just_guessed = False
    return just_guessed

def get_flips_and_score():
    image_flips = ImageGrab.grab(bbox=(fl1x, fl1y, fl2x, fl2y))
    image_score = ImageGrab.grab(bbox=(score1x, score1y, score2x, score2y))
    # image_flips.save("temp/image_flips_end.png")
    # image_score.save("temp/image_score_end.png")
    image_score = numpy.invert(image_score)
    score_text = pytesseract.image_to_string(image_score, lang='eng')
    score = int("".join(filter(str.isdigit, score_text)))
    image_flips = numpy.invert(image_flips)
    flips_text = pytesseract.image_to_string(image_flips, lang='eng')
    flips = int("".join(filter(str.isdigit, flips_text)))
    return flips, score

def get_score():
    image = ImageGrab.grab(bbox=(score1x, score1y, score2x, score2y))
    image = numpy.invert(image)
    # image = pyautogui.screenshot(region=(score1x,score1y, score2x, score2y))
    # image = numpy.invert(image)
    image_to_text = pytesseract.image_to_string(image, lang='eng')
    num = int("".join(filter(str.isdigit, image_to_text)))
    return num

def get_flips_left():
    image = ImageGrab.grab(bbox=(fl1x, fl1y, fl2x, fl2y))
    image = numpy.invert(image)
    # image = pyautogui.screenshot(region=(fl1x, fl1y, fl2x, fl2y))
    # image = numpy.invert(image)
    # save_name = "temp/num_flips.png"
    # image.save(save_name)
    # image = Image.open(save_name)
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

def log(is_done, flips, score, total_guesses):
    f = open("log.txt", "a")  # append mode
    f.write(str(score) + "\t")
    f.write(str(flips) + "\t")
    f.write(str(total_guesses) + "\n")
    if is_done:
        f.write("-------------------------------" + "\n")
    f.close()
    if is_done:
        f = open("log_sum.txt", "a")
        f.write("SCORE:\t" + str(score) + "\n")
        f.close()

def reset_procedure(score):
    if score < GOAL:
        click_reset()
        time.sleep(15)
        click_animate()
    else: 
        quit()
    
def reset_check(score):
    if game_is_over():
        reset_procedure(score)

def live_update(flips,score,total_guesses):
    f = open("live.txt", "w")
    f.write("SCORE:\t" + str(score) + "\n")
    f.write("FLIPS LEFT:\t" + str(flips) + "\n")
    f.write("TOTAL GUESSES:\t" + str(total_guesses) + "\n")
    f.close()
    path = "/home/sean/"
    src = path + 'Desktop/fun/primer/live.txt'
    dst = path + 'Dropbox/live.txt'
    os.popen(f"cp {src} {dst}")

def save_total_guesses(total_guesses):
    f = open("total_guesses.txt", "w")
    f.write(str(total_guesses))

def get_total_guesses():
    total_guesses = -1
    with open('total_guesses.txt') as f:
        total_guesses = int(f.readline())
    return total_guesses

def set_thresh(score, flips):
    inter = flips / (4540 - score)
    return 0.75 + 0.15 * (2 / (1 + math.exp(-0.3 * inter)) - 1)

if __name__ == "__main__":
    total_guesses = get_total_guesses()
    score = get_score()
    flips0 = 100
    flips1 = 100
    while True:
        if score >= GOAL:
            quit()
        flips0 = flips1
        flips_used = 0
        if flips0 < 0:
            reset_procedure(score)
        while True:
            #LOOP FOR EACH ROUND
            if score >= 4535:
                quit()
            ht = get_heads_tails()
            THRESH = set_thresh(score, flips0 - flips_used)
            #engine
            if flips0-flips_used <= 0:
                just_guessed = engine_no_flips_left(ht[0],ht[1])
            elif flips0-flips_used == 30:
                flip()
                flips_used += 1
            else:
                just_guessed, delta_flips = engine(ht[0],ht[1])
                flips_used += delta_flips
            if just_guessed:
                #end of round
                time.sleep(2)
                # submit_old_run()
                flips_used -= 1
                flips1 = get_flips_left()
                if flips1 < 20:
                    #if game is over
                    log(True,flips1,score,total_guesses)
                    reset_procedure(score)
                    flips1 = 100
                    score = 0
                    total_guesses = 0
                    save_total_guesses(total_guesses)
                    break
                if -1*flips_used < flips1-flips0:
                    score += 1
                total_guesses += 1
                log(False,flips1,score,total_guesses)
                save_total_guesses(total_guesses)
                live_update(flips1,score,total_guesses) #probably comment this out
                break 



# time.sleep(2)
# while True:
#     ht = screenshot_heads_tails()
#     if get_flips_left() > 0:
#         bad_engine(ht[0],ht[1])
#     else:
#         engine_no_flips_left(ht[0],ht[1])
#     #log(False)

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
