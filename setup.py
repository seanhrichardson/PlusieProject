import pyautogui
import numpy as np

things = [
["top left of heads-tails:", "ht1"],
["bottom right of heads-tails", "ht2"],
["1 flip", "flip1"],
["guess fair", "fair"],
["guess cheater", "cheat"],
["5 flips", "flip5"],
["top of flips left", "fl1"],
["bottom of flips left", "fl2"],
["name for leaderboard coordinates", "name"],
["email for plushie drawing coordinates", "email"],
["submit coords", "submit"],
["REFRESH coords", "reset"],
["animation", "anim"],
["Score top left", "score1"],
["Score bottom right", "score2"]
]

coords = []

ret = ""
for field in things:
    input(field[0])
    pos = pyautogui.position()
    varx, vary = str(pos[0]), str(pos[1])
    coords.append((pos[0],pos[1]))
    ret += field[1] + "x" + "," + field[1] + "y" + "=" + varx + "," + vary + "\n"

print(coords)

np.savetxt("coords.txt", coords)

print("\nCOPY AND PASE THE BELOW INTO BOT CODE")
print(ret)

input("enter to exit")


# str1 = "top left of heads-tails:"
# input(str1)
# ret = str1 + "\t" + str(pyautogui.position()) + "\n"

# str2 = "bottom right of heads-tails:"
# input(str2)
# ret += str2 + "\t" + str(pyautogui.position()) + "\n"

# str3 = "1 flip\t\t\t"
# input(str3)
# ret += str3 + "\t" + str(pyautogui.position()) + "\n"

# str4 = "guess fair\t\t"
# input(str4)
# ret += str4 + "\t" + str(pyautogui.position()) + "\n"

# str5 = "guess cheater\t\t"
# input(str5)
# ret += str5 + "\t" + str(pyautogui.position()) + "\n"

# str6 = "5 flips\t\t\t"
# input(str6)
# ret += str6 + "\t" + str(pyautogui.position()) + "\n"

# str7 = "top of flips left\t"
# input(str7)
# ret += str7 + "\t" + str(pyautogui.position()) + "\n"

# str8 = "bottom of flips left\t"
# input(str8)
# ret += str8 + "\t" + str(pyautogui.position()) + "\n"

# str9 = "name for leaderboard coordinates"
# input(str9)
# ret += str9 + "\t" + str(pyautogui.position()) + "\n"

# str10 = "email for plushie drawing coordinates"
# input(str10)
# ret += str10 + "\t" + str(pyautogui.position()) + "\n"

# str11 = "submit coordinates"
# input(str11)
# ret += str11 + "\t" + str(pyautogui.position()) + "\n"

# str12 = "reset game"
# input(str12)
# ret += str12 + "\t" + str(pyautogui.position()) + "\n"

# print(ret)