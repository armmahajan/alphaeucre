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

    def createQtable(self):
        self.QTable = Qtable.Qtable()

    def AIManager(self):
        self.createQtable()
        self.setPlayers()

    def setPlayers(self):
        for i in range(1, 4):
            self.playersArr[i] = AIPlayer.AIPlayer()
        pass

    def isTrainingComplete(self):
        # if Q-values have minimal change or if Q-values are cycling training is complete return true. else false
        return self.QTable.training

    def movePlayer(self, playerNum, state, actions):
        # state must be translated to states with ranked cards.
        if playerNum >= 4 or playerNum <= 0:
            raise Exception("Player value not in range")
        if np.random.random() < self.exploration_prob:
            # action is to explore
            self.playersArr[playerNum].move(state, True, actions)
        else:
            self.playersArr[playerNum].move(state, False, actions)

    def updateQTable(self, state, action, reward):
        oldQvalue = self.QTable.getQvalue(state, action)
        newValue = self.learning_rate * reward + self.discount_factor * self.QTable.nextStateBestValue(state,action) - oldQvalue
        self.QTable.updateQvalue(state, action, newValue)

