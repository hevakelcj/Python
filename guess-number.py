#!/usr/bin/env python
#-*-coding:gb2312-*-#

'''             **** Guess Number ****

This is a guessing number game.
At the beginning of each round, it will generate a number
range from 1 to 99. Player should guess what number it is,
then input. If the number player input is equal to what 
program generated, player win and end of this round. Else, 
program will narrow the range. Then player guess again. 
Repeat this untill player win.
This game is suitable for several players. Each of players
guesses one by one. The player who gets the right number 
will be win.
--------
Website: my.oschina.net/hevakelcj
E-mail : hevake_lcj@126.com'''

import random

def one_round(down_limit=0, up_limit=100) :
    '''One round. Input \'q\' to quit'''    

    the_number = random.randint(down_limit, up_limit)

    while True :
        range = '(' + str(down_limit) + '~' + str(up_limit) + ')'
        user_input = raw_input('Please input number' + range + ': ')
        
        if user_input == 'q' :
            print 'User cancel.'
            break

        try :
            user_input = int(user_input)
        except :
            print 'ERROR: Input invaild.'
            continue
 
        if down_limit < user_input < up_limit :
            if user_input == the_number :
                break
            else :
                if user_input > the_number :
                    up_limit = user_input
                else :
                    down_limit = user_input
                
                if up_limit - down_limit == 2 :
                    print 'The number is the other'
                    break
        else :
            print 'Out of range !'

    print 'The number is %d' % (the_number)

if __name__ == '__main__' :
    print '=' * 50
    print __doc__
    print '-' * 50

    while True :
        one_round()
        print '-' * 50
        play_again = raw_input('Play again? ([y]/n) : ')
        if play_again == 'n' or play_again == 'N' :
            break

    print 'Thank for you playing, Bye ~~'
    print '=' * 50
