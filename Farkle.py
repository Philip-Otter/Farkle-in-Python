# A program to play the game Farkel

name = 'Philip'
score = 0


# Draws our game board
def draw(one,two,three,four,five,six):

    # Dice art
    def dice(x):
        try:
            if x == 1:
                print('''
                 _____________
                |             |
                |             |         
                |      *      |
                |             |
                |_____________|
                ''')
            elif x == 2:
                print('''
                 _____________
                |             |
                |  *          |         
                |             |
                |          *  |
                |_____________|
                ''')
            elif x == 3:
                print('''
                 _____________
                |             |
                |  *          |         
                |      *      |
                |          *  |
                |_____________|
                ''')
            elif x == 4:
                print('''
                 _____________
                |             |
                |  *       *  |         
                |             |
                |  *       *  |
                |_____________|
                ''')
            elif x == 5:
                print('''
                 _____________
                |             |
                |  *       *  |         
                |      *      |
                |  *       *  |
                |_____________|
                ''')
            elif x == 6:
                print('''
                 _____________
                |             |
                |  *       *  |         
                |  *       *  |
                |  *       *  |
                |_____________|
                ''')
        except:
            print("Failed to render dice")

    # Prints dice based on number of remaining dice
    rollVals = {1: one, 2: two, 3: three, 4: four, 5: five, 6: six}  # Utilizes dictionary for tracking the quantity of the roles from func params    
    diceNum = one+two+three+four+five+six
    print(diceNum)
    x=1
    try:
        z = 1  # Counter for rollVals
        while x <= diceNum:
            y = 1  # Nested loop counter
            if rollVals[z] != 0:
                while y <= rollVals[z]:
                    print(z)
                    print(y)
                    print(rollVals[z])
                    dice(z)
                    y = y+1
                x = x+1
                z = z+1
            else:
                if x == diceNum:
                    z = z+1
                else:
                    x=x+1
    except:
        print('Failed to render proper dice values')

    print('|  ', name, '  |   Dice #:  ', diceNum, '  |  Score:  ', score, '  |')


# Takes care of formatting and listing scoring options for our users based on the dirty list with overlapping scores.
def scoring(dirtyList = []):  # The dirty list is an unfiltered list put together in rules()
    cleanList = []  # list with the users real scoring options (remove duplicate and useless information)
    try:
        for x in dirtyList:
            if x == 'straight':
                cleanList = []  # Removing stupid choice of not picking the straight i.e. 1 or 5.
                cleanList.append('Straight:  1500pts')
    except:
        print('Failed to parse "dirty list" to clean score list')


# Checks what scoring options are available
def rules(dice = []):

    scoreOptions = []

    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0

    try:  # Responsible for sorting dice distribution.
        for x in dice:
            if x == 1:
                one = one+1
            elif x == 2:
                two = two+1    
            elif x == 3:
                three = three+1            
            elif x == 4:
                four = four+1
            elif x == 5:
                five = five+1
            elif x == 6:
                six = six+1
    except:
        print('Failed to organize dice')


    # Checks for pairs
    def matchesCheck(one,two,three,four,five,six):
        doubleNums = 0
        rollVals = {1: one, 2: two, 3: three, 4: four, 5: five, 6: six}  # Utilizes dictionary for tracking the quantity of the roles from func params
        removableDice = []  # list to keep track of our scoring dice values

        print(rollVals)  # Testing only

        try:
            x = 1

            while x <= 6:
                val = rollVals[x]
                if val == 6:  # 6 of a kind:  3000pts
                    removableDice.append('6 dice of value:  ')
                    removableDice.append(x)
                    break
                elif val == 5: # 5 of a kind:  2000pts
                    removableDice.append('5 dice of value:  ')
                    removableDice.append(x)
                    break         
                elif val == 4:
                    doubleNums = doubleNums+2
                    removableDice.append('4 dice of value:  ')
                    removableDice.append(x)
                    x = x+1
                elif val < 4 and val > 0:
                    try:
                        if val == 3:
                            doubleNums = doubleNums+1
                            removableDice.append('2 dice of value:  ')
                            removableDice.append(x)
                            removableDice.append('3 dice of value:  ')
                            removableDice.append(x)                                                 
                            x=x+1
                        elif val == 2:
                            doubleNums = doubleNums+1
                            removableDice.append('2 dice of value:  ')
                            removableDice.append(x)                    
                            x=x+1
                        else:  # '1' case
                            x=x+1
                    except:
                        print("Failed to evaluate dice matches below a quantity of 4")
                else:  # '0' case
                    x=x+1
            return removableDice

        except:
            print('Failed to evaluate matches')


    # Checks for singles (that matter)
    def singlesCheck(one,two,three,four,five,six, removableDice):
        rollVals = {1: one, 2: two, 3: three, 4: four, 5: five, 6: six}  # Utilizes dictionary for tracking the quantity of the roles from func params

        try:
            if rollVals[1] > 0:  # 100pts each
                removableDice.append(rollVals[1])
                removableDice.append(" dice of value:  1")
            
            if rollVals[5] > 0:  # 50pts each
                removableDice.append(rollVals[5])
                removableDice.append(" dice of value:  5")             
        except:
            print('Failed to evaluate single dice values')
        
        return removableDice

    # Checks for a straight
    def straightCheck(one,two,three,four,five,six, removableDice):
        try:
            if one == 1:
                if two == 1:
                    if three == 1:
                        if four == 1:
                            if five == 1:
                                if six == 1:
                                    removableDice.append('Straight')
        except:
            print('Failed to check for straight')
        
        return removableDice

    scoreOptions=matchesCheck(one,two,three,four,five,six)
    scoreOptions=singlesCheck(one,two,three,four,five,six, scoreOptions)
    scoreOptions=straightCheck(one,two,three,four,five,six, scoreOptions)
    draw(one,two,three,four,five,six)
    print(scoreOptions)
    print(one, two, three, four, five, six)
    scoring(scoreOptions)


def main():
    #dice = [3,2,1,4,5,6]
    #dice = [1,1,1,1,1,1]
    #dice = [2,2,2,3,3,3]
    dice = [1,0,2,0,1,0]
    rules(dice)


main()