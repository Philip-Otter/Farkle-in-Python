# A program to play the dice game 'Farkle'.

import time
import numpy as np
from logging import exception


# Reset the game header.
def refresh():
    print("\033c")
    print('''                         ______         _    _      
                        |  ____|       | |  | |     
                        | |__ __ _ _ __| | _| | ___ 
                        |  __/ _` | '__| |/ / |/ _ \\
                        | | | (_| | |  |   <| |  __/
                        |_|  \__,_|_|  |_|\_\_|\___|
                     ──────────────────────────────────\n''')


# Generate a dice roll result for a given number of dice.
def roll_dice(num_dice):
    return (roll := list(np.sort(np.random.randint(1, 7, num_dice))))


# Illustrate a given dice roll and list the results.
def print_dice(roll):
    die_top    = "┌─────────┐  "
    die_blank  = "│         │  "
    die_left   = "│  ●      │  "
    die_center = "│    ●    │  "
    die_right  = "│      ●  │  "
    die_double = "│  ●   ●  │  "
    die_bottom = "└─────────┘  "

    print(die_top * len(roll))
    for i in range(1, 7):        # Print top third of each die based on each value.
        num = roll.count(i)
        if   i == 1:
            print(die_blank * num, end="")
        elif i == 2 or i == 3:
            print(die_right * num, end="")
        else:
            print(die_double * num, end="")
    print()
    
    for i in range(1, 7):        # Print center third of each die based on each value.
        num = roll.count(i)
        if   i == 1 or i == 3 or i == 5:
            print(die_center * num, end="")
        elif i == 2 or i == 4:
            print(die_blank * num, end="")
        else:
            print(die_double * num, end="")
    print()
    
    for i in range(1, 7):        # Print bottom third of each die based on each value.
        num = roll.count(i)
        if   i == 1:
            print(die_blank * num, end="")
        elif i == 2 or i == 3:
            print(die_left * num, end="")
        else:
            print(die_double * num, end="")            
    print()
    print(die_bottom * len(roll))

    print(f"Roll Result: {', '.join([str(x) for x in roll])}")


# Analyze a given roll result for possible melds and return meld type information.
def list_melds(roll):    
    roll_dist = []
    valid_melds = {}

    for i in range(1, 7):
        # Create a distribution of the dice roll.
        roll_dist.append(roll.count(i))

    if roll_dist.count(6) == 1:         # Six of a Kind (3000 pts.)
        valid_melds["6OAK"] = {"desc": "Six of a Kind", "points": 3000, "dice": 6}

    if roll_dist.count(3) == 2:         # Two Triplets (2500 pts.)
        valid_melds["2TRIP"] = {"desc": "Two Triplets", "points": 2500, "dice": 6}

    if roll_dist.count(5) == 1:         # Five of a Kind (2000 pts.)
        meld_type = roll_dist.index(5) + 1
        valid_melds["5OAK"] = {"desc": "Five of a Kind", "points": 2000, "dice": 5, "type": meld_type}

    if roll_dist.count(1) == 6:         # 1-6 Straight (1500 pts.)
        valid_melds["1-6ST"] = {"desc": "1-6 Straight", "points": 1500, "dice": 6}

    if roll_dist.count(2) == 3:         # Three Pairs (1500 pts.)
        valid_melds["3PAIR"] = {"desc": "Three Pairs", "points": 1500, "dice": 6}

    if roll_dist.count(4) == 1:         # Four of a Kind (1000 pts.)
        if roll_dist.count(2) == 1:     # Four of a Kind with a Pair (1500 pts.)
            valid_melds["4OAKP"] = {"desc": "Four of a Kind with a Pair", "points": 1500, "dice": 6}

        meld_type = roll_dist.index(4) + 1
        valid_melds["4OAK"] = {"desc": "Four of a Kind", "points": 1000, "dice": 4, "type": meld_type}

    if roll_dist.count(3) == 1:         # Three of a Kind (points vary)
        meld_type = roll_dist.index(3) + 1
        valid_melds["1TRIP"] = {"desc": f"Triplet of {meld_type}'s", "points": 300 if meld_type == 1 else (meld_type) * 100, "dice": 3, "type": meld_type}

    if roll_dist[0] != 0:       # Ones (100 pts. each)
        num_ones = roll_dist[0]
        valid_melds["ONES"] = {"desc": f"{num_ones} One" if num_ones == 1 else f"{num_ones} Ones", "points": num_ones * 100, "dice": num_ones, "type": 1}

    if roll_dist[4] != 0:       # Fives (50 pts. each)
        num_fives = roll_dist[4]
        valid_melds["FIVES"] = {"desc": f"{num_fives} Five" if num_fives == 1 else f"{num_fives} Fives", "points": num_fives * 50, "dice": num_fives, "type": 5}
    
    return valid_melds


def main():
    #@TODO - Create player turn function.
    refresh()
    time.sleep(1)

    # Begin Player Turn
    print("It is your turn!")
    input("Press Enter to roll.")
    refresh()

    print("With a vigorous shake, you roll the dice across the table.")
    time.sleep(2)
    refresh()
    
    # Generate new roll with six dice, and analyze it for valid melds.
    pl_roll = roll_dice(6)
    pl_melds = list_melds(pl_roll)

    if len(pl_melds) == 0:
        # If no valid melds, FARKLE!
        print_dice(pl_roll)
        print("\nFARKLE! All points gained this round are lost, and your turn is over.\n")
    else:
        # Meld choice input validation loop.
        i = 0
        while i < 9001:
            print_dice(pl_roll)
            pl_meld_list = list(pl_melds.values())

            if len(pl_melds) == 1:
                print(f"\nYour only possible meld is: {pl_meld_list[0]['desc']}\n")
            else:
                # List best possible melds from roll result.
                pl_meld_desc = [pl_meld_list[x]['desc'] for x in range(len(pl_meld_list))]
                print(f"\nYour highest possible melds are: {'; '.join(pl_meld_desc)}\n")
            
            if i == 1:
                print("ERROR: Please enter numbers separated by commas. (1, 1, 5, etc.)", end="")
            
            if i == 2:
                print("ERROR: Entered values do not meld. Try again.", end="")

            if i == 3:
                print("ERROR: One or more entered values do not meld. Try again.", end="")

            chosen_melds = input("\nEnter the dice values you would like to meld: ")
            chosen_melds = chosen_melds.split(", ")

            try:
                # Convert user input to an integer list.
                list_chosen_melds = [int(x) for x in chosen_melds]
            
            except:
                # Error 1: User did not input a comma-separated list of integers.
                refresh()
                i = 1
                continue
            
            try:
                # Analyze the entered values for valid melds.
                chosen_melds = list_melds(list_chosen_melds)
                chosen_melds = list(chosen_melds.values())

            except:
                # Error 2: Failed to create meld list from user input.
                refresh()
                i = 2
                continue

            roll_score = 0
            try:
                while len(chosen_melds) > 0:
                    if chosen_melds[0] not in pl_meld_list:
                        if chosen_melds[0]["type"] != 1 and chosen_melds[0]["type"] != 5:
                            raise exception
                        elif chosen_melds[0]["type"] == 1 and chosen_melds[0]["dice"] > pl_roll.count(1):
                            raise exception
                        elif chosen_melds[0]["type"] == 5 and chosen_melds[0]["dice"] > pl_roll.count(5):
                            raise exception
                    
                    roll_score += chosen_melds[0]["points"]
                    if chosen_melds[0]["dice"] == len(list_chosen_melds):
                        list_chosen_melds = []
                    else:
                        for _ in range(chosen_melds[0]["dice"]):
                            list_chosen_melds.remove(chosen_melds[0]["type"])

                    chosen_melds = list_melds(list_chosen_melds)
                    chosen_melds = list(chosen_melds.values())

                break
            
            except:
                # Error 3: One or more numbers from user input do not meld.
                refresh()
                i = 3
                continue
    
    print(f"Roll Score: {roll_score}")
        

main()