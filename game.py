import math, numpy, random, time, getpass
import strawberryfields as sf
from strawberryfields.ops import *
from strawberryfields.ops import Gate
from strawberryfields.utils import scale
from numpy import pi, sqrt



print("\n\n\n\n===== Welcome to Quantum Battleships! =====\n\n")
print("\n\n")
print("Press Enter to continue!")
input()
print("Grab a buddy to play with!")
input()
print("Player 1 will choose the position of a Battleship.")
input()
print("Player 2 will try to bomb it.")
input()
print("Before we begin, let's start with a quick overview of how this game works on a quantum computer.")
input()
print("This game uses Xanadu's StrawberryFields API to simulate qumodes.")
input()
print("Xanadu is working on photonic quantum computers (light based) which use photons to carry information, even at room temperature!")
input()
print("Light is a continuous physical system so qumodes are a continuous-variable model (different from qubits!) ")
input()
print("This game applies Single-Mode Gates to qumodes to put them in a superposition as the ships get destroyed.")
input()
print("Two-Single Mode Gates entangle the positions of the ships. ")
input()
print("After applying the gates we measure the Fock states of each mode to determine if the ship has sunk or stayed afloat. ")
input()
print("With a better understanding we can now resume the game, let's start with Player 1.")
input()
# get player 1 to position boat
print("Don't look Player 2!")
input()
print("The letters are all the positions you can place your ship\n")
print("|\     /|")
print("| d   b |")
print("|  \ /  |")
print("f   X   a")
print("|  / \  |")
print("| e   c |")
print("|/     \|\n")

input()

chosen = 0
while (chosen==0):
	ship = getpass.getpass("Choose a letter for your ship. (a, b, c, d, e or f)\n")
	if ship in ["a","b","c","d","e","f"]:
		chosen = 1
	else:
		print("That letter does not exist, try that again.")

# get player 2 to position three bombs
time.sleep(1)
print("\nPlayer 2: You're up!")
input()
print("The numbers are all the places your bomb can go off.\n")
print("4       0")
print("|\     /|")
print("| \   / |")
print("|  \ /  |")
print("|   2   |")
print("|  / \  |")
print("| /   \ |")
print("|/     \|")
print("3       1\n")
input()

chosen = 0
while (chosen==0):
    bomb1 = int(input("Choose a position for your first bomb. (0, 1, 2, 3 or 4)\n"))
    if ( (bomb1 >= 0) & (bomb1 < 5) ):
        chosen = 1
    else:
        print("That letter does not exist, try that again.")

chosen = 0
while (chosen==0):
    bomb2 = int(input("\nChoose a position for your second bomb. (0, 1, 2, 3 or 4)\n"))
    if ( (bomb1 >= 0) & (bomb1 < 5) ):
        if (bomb2 != bomb1):
            chosen = 1
        else:
            print("That's already been bombed. Choose again.")
    else:
        print("That letter does not exist, try that again.")

chosen = 0
while (chosen==0):
    bomb3 = int(input("\nChoose a position for your third and final bomb. (0, 1, 2, 3 or 4)\n"))
    if ( (bomb1 >= 0) & (bomb1 < 5) ):
        if bomb3 not in [bomb1,bomb2]:
            chosen = 1
        else:
            print("That's already been bombed. Choose again.")
    else:
        print("That number does not exist, try that again.")

# run the scenario on the qumodes and see what happens
print("\nWe'll now run this scenario on Strawberryfields and see what happens.")
input()

eng, q = sf.Engine(6)

battle = [0]*6
with eng:
    if (ship == "a"): # a means 0 and 1
        Dgate(2.0 + 1j) | q[0]
        CXgate(0) | (q[0], q[1])
        Xgate(0) | q[0]
        battle[0] = 1
        Rgate(0) | q[0]
    if (ship == "b"): # b means 0 and 2
        Dgate(2.0 + 1j) | q[0]
        CXgate(0) | (q[0], q[2])
        Xgate(0) | q[0]
        battle [0] = 1
        Rgate(0) | q[0]
    if (ship == "c"): # c means 1 and 2
        Dgate(2.0 + 1j) | q[1]
        CXgate(0)| (q[1], q[2])
        Xgate(0) | q[1]
        battle[1] = 1
        Rgate(0) | q[1]
    if (ship == "d"): # d means 2 and 4
        Dgate(2.0 + 1j) | q[4]
        CXgate(0) | (q[4], q[2])
        Xgate(0) | q[4]
        battle [2] = 1
        Rgate(0) | q[2]
    if (ship == "e"): # e means 2 and 3
        Dgate(2.0 + 1j) | q[3]
        CXgate(0) | (q[3], q[2])
        Xgate(0) | q[3]
        battle[2] = 1
        Rgate(0) | q[2]
    if (ship == "f"): # f means 3 and 4
        Dgate(2.0 + 1j) | q[3]
        CXgate(0) | (q[3], q[4])
        Xgate(0) | q[3]
        battle[3] = 1
        Rgate(0) | q[3]

# apply the bombs


    if (battle[bomb1]==1):
        Measure | q[1]
    else:
        Rgate(0) | q[1]
    if (battle[bomb2]==1):
        Measure | q[1]
    else:
        Rgate(0) | q[1]

# measure all in X basis
    Dgate (2.0 + 1j) | q[0]
    Measure | q[0]
    Dgate (2.0 + 1j) | q[1]
    Measure | q[1]
    Dgate (2.0 + 1j) | q[2]
    Measure | q[2]
    Dgate (2.0 + 1j)| q[3]
    Measure | q[3]
    Dgate (2.0 + 1j)| q[4]
    Measure | q[4]

state = eng.run('fock', cutoff_dim=6)  # run all gates (and execute measurements)

time.sleep(1)
print("\nNow let's see how intact the ship is.")
print("Between 1% and 100% intact means it's still afloat.")
print("Between -1% and -100% intact means the ship has sunk")
print("0% intact could go either way.")


result1 = state.fock_prob([0,1,2,3,4,5])

result2 = state.fock_prob([1,2,3,4,5,0])

result3 = state.fock_prob([2,3,4,5,0,1])

result4 = state.fock_prob([3,4,5,0,1,2])

result5 = state.fock_prob([4,5,0,1,2,3])

result6 = state.fock_prob([5,0,1,2,3,4])



# determine damage for ship
damage = 0

if (ship == "a"): 
	damage = damage + 0 + 1
if (ship == "b"): 
	damage = damage + 0 + 2
if (ship == "c"): 
	damage = damage + 1 + 2
if (ship == "d"): 
	damage = damage + 2 + 4
if (ship == "e"): 
	damage = damage + 2 + 3
if (ship == "f"): 
	damage = damage + 3 + 4


time.sleep(1)
print("\nThe ship is " + str(int( 100*(1-2*damage) )) + "% intact")

print("(which means " + str(int( -100*(1-2*damage) )) + "% broken).\n")

if (damage>0.5):
	print("It has been destroyed!\nPlayer 2 wins!\n\n")

else:
    print("It's still afloat!\nPlayer 1 wins!\n\n")

print("=====================================GAME OVER=====================================")
