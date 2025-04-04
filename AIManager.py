import AIPlayer
import numpy as np
import Qtable


class AIManager:
    """
    self.state = {
            'phase': 'trumpFaceUp', # One of: trumpFaceUp, dealerDiscard, trumpFaceDown, trick
            'trump': None, # Hack: If trump is a single value it is face up naming, if it is a list, it is face down and the items are the options
            'dealer': 3,
            'cards': {
                0: [],
                1: [],
                2: [],
                3: []
            },
            'current_trick': [], # Each index represents that players cards
            'cards_played': [], #TODO:
            'trick_points' : { #
                0: 0,
                1: 0,
                2: 0,
                3: 0,
    }
    """

    # constants for learning
    learning_rate: int = 0.8
    discount_factor: int = 0.95
    exploration_prob: int = 0.2
    epochs: int = 1000

    def __init__(self):
        self.playersArr = None
        self.QTable = None
        self.QTable = Qtable.Qtable()
        self.setPlayers()
        print('players are set')

    def AIManager(self):
        pass

    def setPlayers(self):
        for i in range(0, 3):
            self.playersArr= [AIPlayer.AIPlayer(self.QTable) for i in range(4)]
        #pass

    def isTraining(self):
        # if Q-values have minimal change or if Q-values are cycling training is complete return true. else false
        return self.QTable.training

    def getQtable(self):
        return self.QTable


    def movePlayer(self, state,playerNum):
        # state must be translated to states with ranked cards.
        actions = state["cards"]
        # In Game Engine Pindex makes sure player O is always the first to go
        print(type(playerNum))
        explore =  np.random.random() < self.exploration_prob
            # action is to explore
        return self.playersArr[playerNum].move(state, explore, actions, playerNum)

    def updateQTable(self, playNum, reward):
        self.playersArr[playNum].updateQtable(reward,self.learning_rate)

