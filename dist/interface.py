import keyboard
import os
import sys



class ui:
    def __init__(self):
        pass



    
first_in = input(os.getcwd() + "> ")
working_dir = os.getcwd()

if first_in == "dir":
    print(os.listdir())


if first_in == "tutor":
    print("Welcome To Tutorial of Finder_CLI \n")
    print("Finder_CLI is a command line based file explorer, thought and made for programmers. \n")
    print("To be more productive, keyboard is the choice, and a keyboard based full finder is not there; yet. \n")
    print("Meet Finder_CLI, the best cli finder you can get. \n")
    print('Welcome, to use Finder_CLI at its utmost efficiency, you must learn some basic commands, and some advanced commands')
    print('When it shows you the path, it expects you to do something about it... \n')
    print('For this, you need to learn basic cd, dir, find, cd.., move, move_dir, rem_dir, rem... and much more, but for right now, this is basics.')
    print("We'll start with normal commands. ")



