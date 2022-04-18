import math
import random
import numpy as np

a = 0.5  #probabily of heads if fair
b = 0.75 #probability of heads if weighted
A0 = 0.5 #initial probability of fair
B0 = 0.5 #intial probability of weighted

def prob_fair(n,k):
    binom = math.comb(n,k)
    return (binom*a**k*(1-a)**(n-k)*A0)/(A0*binom*a**k*(1-a)**(n-k)+B0*binom*b**k*(1-b)**(n-k))

#STRATEGY:
def engine(heads,tails):
    #actions = ["flip", "fair", "cheat"]
    thresh = 0.75
    if prob_fair(heads+tails,heads) >= thresh:
        return True #guess is fair
    if prob_fair(heads+tails,heads) <= 1-thresh:
        return False #guess is cheat
    return "flip"

#if no flips left...
def engine_no_flips_left(heads,tails):
    if prob_fair(heads+tails,heads) >= 0.5:
        return True
    return False

#GAME:
#flips coin. Returns if result is heads.
def flip_heads(is_fair):
    x = a
    if (not is_fair):
        x = b
    outputs = [True, False]
    return random.choices(outputs, weights=(x,1-x))[0]

def calculate_net_flips(flips,guess,is_fair):
    bonus = -30
    if (guess == is_fair):
        bonus = 15
    return bonus-flips

#simulates each round.
#returns: net flips, if guess was correct
def round(flips_left):
    is_fair = random.choices([True,False])[0]
    heads = 0
    tails = 0
    #start game
    while (True):
        flip = flip_heads(is_fair)
        if flip:
            heads += 1
        else:
            tails += 1
        #if no flips left:
        if flips_left-(heads+tails) <= 0:
            return -100, engine_no_flips_left(heads,tails)
        #otherwise:
        action = engine(heads,tails)
        if action == True:
            return calculate_net_flips(heads+tails,action,is_fair), is_fair == True
        if action == False:
            return calculate_net_flips(heads+tails,action,is_fair), is_fair == False

#simulates the game.
def game():
    flips = 100
    correct = 0
    while (flips >= 0):
        net_flips, was_correct = round(flips)
        flips += net_flips
        if (was_correct):
            correct += 1
    return correct

#-------------

def test2():
    for thresh in np.linspace(0.72,0.8,9):
        N = 1000000
        total = 0
        for i in range(N):
            total += round(thresh)
        print(str(thresh) + "\t" + str(total/N))

def test():
    heads = 0
    tails = 0
    for i in range(10000):
        flipped_heads = flip_heads(False)
        if flipped_heads:
            heads += 1
        else:
            tails += 1
    print(100*heads/(heads+tails))

def f(h,t):
    prob = str(prob_fair(h+t,h))
    thresh = 0.75
    if prob_fair(h+t,h) >= thresh:
        return "FAIR    " + prob
    if prob_fair(h+t,h) <= 1-thresh:
        return "CHEAT   " + prob
    return "FLIP   " + prob