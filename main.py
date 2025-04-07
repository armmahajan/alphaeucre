# This is a sample Python script.
from GameEngine import Euchre



def main():
    euchre = Euchre()
    euchre.gameLoop()

def AITraining():
    euchre = Euchre(AI=True) # create the game
    euchre.gameLoopAI()

if __name__ == "__main__":
    print("Hello")
    if input("0 for human players, 1 for AI training: ")=='1':
        AITraining()
    else:
        main()







