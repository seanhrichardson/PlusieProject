import math
import random
import numpy as np

a = 0.5  #probabily of heads if fair
b = 0.75 #probability of heads if weighted
A0 = 0.5 #initial probability of fair
B0 = 0.5 #intial probability of weighted

#returns probability is fair. n=heads+tails, k=heads
def prob_fair(n,k):
    binom = math.comb(n,k)
    return (binom*a**k*(1-a)**(n-k)*A0)/(A0*binom*a**k*(1-a)**(n-k)+B0*binom*b**k*(1-b)**(n-k))

#STRATEGY:
#can return: True (guess fair), False (guess cheater), or flip (flip again)
def engine(heads,tails,thesh):
    # thresh = 0.75
    if prob_fair(heads+tails,heads) >= thresh:
        return True #guess is fair
    if prob_fair(heads+tails,heads) <= 1-thresh:
        return False #guess is cheat
    return "flip"

# def engine(heads,tails):
#     thresh = 0.75
#     if tails > heads+1:
#         return True
#     if heads > tails+2:
#         return False
#     return "flip"

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

#Simulates each round.
#returns: net flips, if guess was correct
def round(flips_left,thresh):
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
        action = engine(heads,tails,thresh)
        if action == True:
            return calculate_net_flips(heads+tails,action,is_fair), is_fair == True
        if action == False:
            return calculate_net_flips(heads+tails,action,is_fair), is_fair == False

#Simulates the game. Returns the score.
def game(thresh):
    flips = 100
    correct = 0
    while (flips >= 0):
        net_flips, was_correct = round(flips,thresh)
        flips += net_flips
        if (was_correct):
            correct += 1
    return correct

def game_100():
    high = 0
    for i in range(100):
        score = game()
        if score > high:
            high = score
    return high

# for thresh in np.linspace(0.86,0.86,1):
#     total_flips = 0
#     num_rounds = 100000
#     for i in range(num_rounds):
#         total_flips += round(1000,thresh)[0]
#     flips_per_round = total_flips/num_rounds
#     print(thresh, "\t", flips_per_round)

for thresh in np.linspace(0.75,0.82,8):
    goal = 4537
    num_games = 10000
    num_goal_games = 0
    for i in range(num_games):
        score = game(thresh)
        if score >= goal:
            num_goal_games += 1
    print(thresh, "\t", num_goal_games/num_games)