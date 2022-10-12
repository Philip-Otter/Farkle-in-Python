# A program to play the dice game 'Farkle'.

import time
import numpy as np


def refresh():
    # Reset the game header.
    print("\033c")
    print('''                         ______         _    _      
                        |  ____|       | |  | |     
                        | |__ __ _ _ __| | _| | ___ 
                        |  __/ _` | '__| |/ / |/ _ \\
                        | | | (_| | |  |   <| |  __/
                        |_|  \__,_|_|  |_|\_\_|\___|
                     ──────────────────────────────────\n''')


def roll_dice(num_dice):
    # Generate a dice roll result for a given number of dice.
    roll = list(np.sort(np.random.randint(1, 7, num_dice)))
    return roll


def print_dice(roll):
    # Illustrate a given dice roll and list the results.
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

    str_roll = [str(x) for x in roll]
    print(f"Roll Result: {', '.join(str_roll)}")


def list_melds(roll):
    # Analyze a given roll result for possible melds.
    
    roll_dist = []
    valid_melds = []

    for i in range(1, 7):
        # Create a distribution of the dice roll.
        roll_dist.append(roll.count(i))

    if roll_dist.count(6) == 1:         # Six of a Kind (3000 pts.)
        valid_melds.append("Six of a Kind")

    if roll_dist.count(3) == 2:         # Two Triplets (2500 pts.)
        valid_melds.append("Two Triplets")

    if roll_dist.count(5) == 1:         # Five of a Kind (2000 pts.)
        valid_melds.append("Five of a Kind")

    if roll_dist.count(1) == 6:         # 1-6 Straight (1500 pts.)
        valid_melds.append("1-6 Straight")

    if roll_dist.count(2) == 3:         # Three Pairs (1500 pts.)
        valid_melds.append("Three Pairs")

    if roll_dist.count(4) == 1:
        if roll_dist.count(2) == 1:     # Four of a Kind with a Pair (1500 pts.)
            valid_melds.append("Four of a Kind with Pair")
            valid_melds.append("Four of a Kind")
        else:       # Four of a Kind (1000 pts.)
            valid_melds.append("Four of a Kind")

    if roll_dist.count(3) == 1:         # Three of a Kind (points vary)
        valid_melds.append("Three of a Kind")

    if roll_dist[0] != 0:       # Ones (100 pts. each)
        valid_melds.append(f"{roll_dist[0]} One" if roll_dist[0] == 1 else f"{roll_dist[0]} Ones")

    if roll_dist[4] != 0:       # Fives (50 pts. each)
        valid_melds.append(f"{roll_dist[4]} Five" if roll_dist[4] == 1 else f"{roll_dist[4]} Fives")
    
    return valid_melds


def main():
    #@TODO - Clean up and comment main and create player turn function.
    refresh()
    # Player starts their turn by throwing all six dice.
    # Generate player's first dice throw
    pl_roll = roll_dice(6)
    time.sleep(1)
    print("With a vigorous shake, you roll the dice across the table.\n")
    time.sleep(1)
    refresh()
    print_dice(pl_roll)
    pl_melds = list_melds(pl_roll)
    if len(pl_melds) == 0:
        print("FARKLE! All points gained this round are lost, and your turn is over.\n")
    elif len(pl_melds) == 1:
        print(f"\nYour only possible meld is: {'; '.join(pl_melds)}\n")
    else:
        print(f"\nYour highest possible melds are: {'; '.join(pl_melds)}\n")
    while True:
        meld_choice = input("Enter the dice values you would like to meld (1, 2, 3, etc.): ")
        meld_choice = meld_choice.split(", ")
        meld_choice = [int(x) for x in meld_choice]
        choice_melds = list_melds(meld_choice)
        if len(choice_melds) > 0 and choice_melds[0] in pl_melds:
            print(choice_melds[0])
            break
        refresh()
        print_dice(pl_roll)
        if len(pl_melds) == 0:
            print("FARKLE! All points gained this round are lost, and your turn is over.")
        elif len(pl_melds) == 1:
            print(f"\nYour only possible meld is: {'; '.join(pl_melds)}")
        else:
            print(f"\nYour highest possible melds are: {'; '.join(pl_melds)}")
        #@TODO - Actual input validation.
        print("\nERROR: Entered values do not meld.")
        

main()