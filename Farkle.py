# A program to play the dice game 'Farkle'.

from ctypes import alignment
import os
import time
import numpy as np
from logging import exception


# Print the current score.
def scoreboard(name, score1, score2):
    print(f"\t\t{name}'s Score: {score1}\t\tComputer's Score: {score2}\n")


# Reset the game header.
def refresh():
    os.system('cls' if os.name=='nt' else 'clear')
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


# Let the player decide which dice to meld (set aside) from a given roll.
def handle_meld_choice(roll):
    melds = list_melds(roll)
    if len(melds) == 0:
        # If no valid melds, FARKLE!
        print_dice(roll)
        print("\nFARKLE! All points gained this round are lost, and your turn is over.\n")
        time.sleep(2)
        input("Press Enter to continue.")
        return (roll_score := 0), (remaining_dice := -1)
    else:
        # Meld choice input validation loop.
        i = 0
        while i < 9001:
            print_dice(roll)
            meld_list = list(melds.values())

            if len(melds) == 1:
                print(f"\nYour only possible meld is: {meld_list[0]['desc']}\n")
            else:
                # List best possible melds from roll result.
                meld_names = [meld_list[x]['desc'] for x in range(len(meld_list))]
                print(f"\nYour highest possible melds are: {'; '.join(meld_names)}\n")
            
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
                chosen_melds = list_melds(list_chosen_melds.copy())
                chosen_melds = list(chosen_melds.values())
                if len(chosen_melds) < 1:
                    raise exception

            except:
                # Error 2: Failed to create meld list from user input.
                refresh()
                i = 2
                continue

            roll_score = 0
            remaining_melds = list_chosen_melds.copy()
            try:    
                while len(chosen_melds) > 0:
                    if chosen_melds[0] not in meld_list:
                        if chosen_melds[0]["type"] != 1 and chosen_melds[0]["type"] != 5:
                            raise exception
                        elif chosen_melds[0]["type"] == 1 and chosen_melds[0]["dice"] > roll.count(1):
                            raise exception
                        elif chosen_melds[0]["type"] == 5 and chosen_melds[0]["dice"] > roll.count(5):
                            raise exception
                    
                    roll_score += chosen_melds[0]["points"]
                    
                    if chosen_melds[0]["dice"] == len(remaining_melds):
                        remaining_melds = []
                    else:
                        for _ in range(chosen_melds[0]["dice"]):
                            remaining_melds.remove(chosen_melds[0]["type"])

                    chosen_melds = list_melds(remaining_melds)
                    chosen_melds = list(chosen_melds.values())

                remaining_dice = len(roll) - len(list_chosen_melds)
                return roll_score, remaining_dice
            
            except:
                # Error 3: One or more numbers from user input do not meld.
                refresh()
                i = 3
                continue


# Run through the player's turn and return their updated score.
def player_turn():
    # Begin Player Turn
    roll_count = 1
    turn_score = 0
    pl_roll = roll_dice(6)
    while True:
        refresh()
        time.sleep(1)
        input(f"Press Enter to roll. (Roll #{roll_count})")
        refresh()

        print("With a vigorous shake, you roll the dice across the table.")
        time.sleep(2)
        refresh()
        
        # Generate new roll with six dice, and analyze it for valid melds.
        roll_score, remaining_dice = handle_meld_choice(pl_roll)
        turn_score += roll_score
        refresh()
        if remaining_dice == -1:
            turn_score = 0
            pl_choice = 'n'
        else:
            i = 0
            while i < 9001:
                print(f"Points accumulated this turn: {turn_score}\n")
                print("You can end your turn and bank these points, or continue rolling the remaining dice for the chance to gain more!\n")
                if i == 1:
                    print("ERROR: Enter 'y' to roll again, or 'n' to end your turn.", end="")
                if remaining_dice == 0:
                    remaining_dice = 6
                    pl_choice = input(f"\nHot Dice! You gain six dice back. Do you want to roll again? (y/n): ").lower()
                else:
                    pl_choice = input(f"\nYou have {remaining_dice} remaining dice. Do you want to roll again? (y/n): ").lower()
                if pl_choice != 'y' and pl_choice != 'n':
                    refresh()
                    i = 1
                    continue
                break

        if pl_choice == 'y':
            pl_roll = roll_dice(remaining_dice)
            roll_count += 1
            continue
        else:
            refresh()
            print(f"Your turn is over, and you have banked {turn_score} points. Press Enter to continue.")
            return turn_score


# CPU meld choice AI.
def cpu_meld_choice(roll):
    melds = list_melds(roll)
    if len(melds) == 0:
        # If no valid melds, FARKLE!
        print_dice(roll)
        print("\nThe Computer FARKLED! It loses all points gained this round, and its turn is over.\n")
        time.sleep(2)
        input("Press Enter to continue.")
        return (roll_score := 0), (remaining_dice := -1)
    else:
        print_dice(roll)
        meld_list = list(melds.values())
        time.sleep(1)

        if len(melds) == 1:
            print(f"\nThe Computer's only possible meld is: {meld_list[0]['desc']}\n")
        else:
            # List best possible melds from roll result.
            meld_names = [meld_list[x]['desc'] for x in range(len(meld_list))]
            print(f"\nThe Computer's highest possible melds are: {'; '.join(meld_names)}\n")
        time.sleep(1)

        if meld_list[0]["dice"] == 6:
            chosen_melds = roll
        else:
            chosen_melds = [meld_list[0]["type"] for _ in range(meld_list[0]["dice"])]

        chosen_melds = list_melds(chosen_melds)
        chosen_melds = list(chosen_melds.values())

        print(f"The Computer has chosen to meld {chosen_melds[0]['desc']}.")
        time.sleep(2)

        roll_score = 0
        remaining_melds = chosen_melds.copy()

        while len(chosen_melds) > 0:
            if chosen_melds[0] not in meld_list:
                if chosen_melds[0]["type"] != 1 and chosen_melds[0]["type"] != 5:
                    raise exception
                elif chosen_melds[0]["type"] == 1 and chosen_melds[0]["dice"] > roll.count(1):
                    raise exception
                elif chosen_melds[0]["type"] == 5 and chosen_melds[0]["dice"] > roll.count(5):
                    raise exception
            
            roll_score += chosen_melds[0]["points"]
            
            if chosen_melds[0]["dice"] == len(remaining_melds):
                remaining_melds = []
            else:
                remaining_melds = []

            chosen_melds = list_melds(remaining_melds)
            chosen_melds = list(chosen_melds.values())

        remaining_dice = len(roll) - meld_list[0]["dice"]
        return roll_score, remaining_dice


# Run through The Computer's turn and return its updated score.
def computer_turn():
    # Begin Computer Turn
    turn_score = 0
    cpu_roll = roll_dice(6)
    while True:
        refresh()
        time.sleep(1)
        print("The Computer pulls fresh entropy from the OS, and rolls the dice.")
        time.sleep(2)
        refresh()
        
        # Generate new roll with six dice, and analyze it for valid melds.
        roll_score, remaining_dice = cpu_meld_choice(cpu_roll)
        turn_score += roll_score
        refresh()
        if remaining_dice == -1:
            turn_score = 0
            cpu_choice = 0
        else:
            print(f"Points accumulated by The Computer this turn: {turn_score}\n")
            time.sleep(1)
            if remaining_dice == 0:
                remaining_dice = 6
                print(f"Hot Dice! The Computer gains six dice back. It will definitely roll again. :)")
                cpu_choice = 1
            elif remaining_dice > 2 and turn_score < 500:
                print(f"The Computer has {remaining_dice} remaining dice. It will roll again.")
                cpu_choice = 1
            else:
                print(f"The Computer has {remaining_dice} remaining dice. It will play it safe and bank its points.")
                cpu_choice = 0
            time.sleep(2)

        if cpu_choice == 1:
            cpu_roll = roll_dice(remaining_dice)
            continue
        else:
            refresh()
            input(f"The Computer's turn is over, and it has banked {turn_score} points. Press Enter to continue.")
            return turn_score


def main():
    refresh()
    pl_name = input("Welcome to Farkle! Please enter your name: ")
    pl_name = "Player" if pl_name == "" else pl_name
    pl_score, cpu_score = 0, 0

    while True:
        # Begin Player Turn
        refresh()
        scoreboard(pl_name, pl_score, cpu_score)
        input("It is your turn! Press Enter to continue.")
        pl_score += player_turn()

        # Begin Computer Turn
        refresh()
        scoreboard(pl_name, pl_score, cpu_score)
        input("It is the Computer's turn! Press Enter to continue.")
        cpu_score += computer_turn()

        if pl_score < 10000 and cpu_score < 10000:
            continue
        elif pl_score >= 10000:
            refresh()
            scoreboard(pl_name, pl_score, cpu_score)
            print("YOU WON!!! Thank you for playing Farkle. :)")
            break
        elif cpu_score >= 10000:
            refresh()
            scoreboard(pl_name, pl_score, cpu_score)
            print("...you lost. Thanks for playing though I guess. :/")
            break
            

main()