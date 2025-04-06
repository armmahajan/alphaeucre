import numpy as np
from card import Card
from collections import Counter
from itertools import combinations

class AIPlayer:

    def __init__(self, QTable):
        self.QTable = QTable
        self.threshold = 0.40
        self.QCellToUpdate = None
        pass

    def move(self, state, explore, actions, playerNum):
        ## add game play methods
        if not state['makers']:
            # defending
            playerNum = playerNum + 4
        if explore == True:
            #to random action
            if playerNum ==0 or playerNum==4:
                options = np.array([0,1,2])
                np.random.permutation(options)
                for act in options:
                    if act == 0 :
                        result = self.tryLeadHighOffSuit(state, actions)
                        if result[0]:
                            self.QCellToUpdate=(playerNum,0,0)
                            return result[1]
                    elif act == 1:
                        result = self.trysetupPartner(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, 0, 1)
                            return result[1]
                    elif act == 2:
                        result = self.tryTrumpShowDown(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, 0, 2)
                            return result[1]
            else:
                stateValue = self.winProbability(state,playerNum)
                actionNum = None
                if stateValue >= self.threshold:
                    actionNum = 0
                elif stateValue >= 0:
                    actionNum = 1
                elif stateValue >= -self.threshold:
                    actionNum = 2
                else:
                    actionNum = 3
                options = np.array([0, 1, 2,3])
                np.random.permutation(options)
                for act in options:
                    if act == 0:
                        result = self.tryUseTrump(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, actionNum, 0)
                            return result[1]
                    elif act == 1:
                        result = self.tryUseLedSuit(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, actionNum, 1)
                            return result[1]
                    elif act == 2:
                        result = self.tryThrowAwayTrump(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, actionNum, 2)
                            return result[1]
                    elif act == 3:
                        result= self.tryThrowAwaySuitLed(state, actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, actionNum, 4)
                            return result[1]
        else:
            #do action with the highest Q-value
            if playerNum == 0 or playerNum==4:
                acts = np.argsort(self.QTable.table[playerNum, 0, :])[::-1] #sort arr max to min
                for act in acts:
                    if act == 0:
                        result = self.tryLeadHighOffSuit(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, 0, 0)
                            return result[1]
                    elif act == 1:
                        result = self.trysetupPartner(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, 0, 1)
                            return result[1]
                    elif act == 2:
                        result=self.tryTrumpShowDown(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, 0, 2)
                            return result[1]
            else:
                stateValue = self.winProbability(state,playerNum)
                actionNum=None
                if stateValue >=self.threshold:
                    actionNum=0
                elif stateValue >=0:
                    actionNum=1
                elif stateValue >=-self.threshold:
                    actionNum=2
                else:
                    actionNum=3
                acts = np.argsort(self.QTable.table[playerNum, actionNum, :])[::-1]
                for act in acts:
                    if act == 0:
                        result = self.tryUseTrump(state, actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, actionNum, 0)
                            return result[1]
                    elif act == 1:
                        result = self.tryUseLedSuit(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, actionNum, 1)
                            return result[1]
                    elif act == 2:
                        result = self.tryThrowAwayTrump(state, actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, actionNum, 2)
                            return result[1]
                    elif act == 3:
                        result = self.tryThrowAwaySuitLed(state,actions)
                        if result[0]:
                            self.QCellToUpdate = (playerNum, actionNum, 3)
                            return result[1]

    def getLeftBower(self, trump_suit):
        if trump_suit == 'diamonds':
            left_bower = 'hearts'
        if trump_suit == 'hearts':
            left_bower = 'diamonds'
        if trump_suit == 'spades':
            left_bower = 'clubs'
        if trump_suit == 'clubs':
            left_bower = 'spades'
        if left_bower == None:
            raise ValueError('Left bower could not be assigned.')
        return left_bower
    # For First player only _____________________________________________
    def tryLeadHighOffSuit(self,state, actions):
        index =0;# todo Include edge case where Q,K,A is used J or lower is high card
        for card in actions:
            if not (card.suit ==state['trump']):
                if card.value in set(['Q','K','A']) or card.value == 'J' and card.suit==self.getLeftBower(state['trump']):
                    #play that index
                    return True, index
            index = index+1
        # else return false
        return False, index


    def trysetupPartner(self,state, actions):
        # if possible play card to set up partner
        # else return false
        # should cover areas the other 2 do not cover.
        index = 0;
        for card in actions:
            if not (card.suit == state['trump']) or card.value == 'J' and card.suit == self.getLeftBower(state['trump']):
                if not card.value in set(['Q', 'K', 'A']):
                    # play that index
                    return True, index
            index = index + 1
        return False, index

    def tryTrumpShowDown(self,state,actions):
        #If possible to play trump do it
        # else return false
        index = 0; #todo play high trump or low trump
        for card in actions:
            if  (card.suit == state['trump']):
                    # play that index
                    return True, index
            index = index + 1
        return False, index

    # For players 1-3 ____________________________________________________

    def tryUseTrump(self,state,actions):
        index = 0; #plays high trump
        actions = sorted(actions, reverse=True)
        for card in actions:
            if  (card.suit == state['trump']):
                    # play that index
                    return True, index
            index = index + 1
        return False, index

    def tryUseLedSuit(self,state,actions):
        index = 0;  # play high led suit
        actions = sorted(actions, reverse=True)
        for card in actions:
            if not (card.suit == state['trump']):
                # play that index
                return True, index
            index = index + 1
        return False, index

    def tryThrowAwayTrump(self, state,actions):
        index = 0;  # plays low trump
        actions.sort()
        for card in actions:
            if (card.suit == state['trump']):
                # play that index
                return True, index
            index = index + 1
        return False, index

    def tryThrowAwaySuitLed(self,state, actions):
        index = 0;  # play low led suit
        actions.sort()
        for card in actions:
            if not (card.suit == state['trump']):
                # play that index
                return True, index
            index = index + 1
        return False, index

    #other functions ______________________________________________________
    def winProbability(self,state,playerNum):
        suits = ['diamonds', 'clubs', 'spades', 'hearts']
        values = ['9', '10', 'J', 'Q', 'K', 'A']
        cards= [Card(value, suit) for suit in suits for value in values]
        trickCards = self.getTrickcards(state['current_trick'])
        known_cards=  state['cards_played'] + trickCards + state['playerCards']
        unknowncards = [card for card in cards if card not in known_cards]
        BestCardOfTrick =None
        i=0
        while BestCardOfTrick == None:
            BestCardOfTrick = state['current_trick'][i]
            i=i+1
        BestCardPlayer =0
        playerindex=0

        trump_suit = state['trump']
        left_bower = None
        if trump_suit == 'diamonds':
            left_bower = 'hearts'
        if trump_suit == 'hearts':
            left_bower = 'diamonds'
        if trump_suit == 'spades':
            left_bower = 'clubs'
        if trump_suit == 'clubs':
            left_bower = 'spades'

        for trickCard in state["current_trick"].values():
            if trickCard == None:
                break
            if trickCard.suit== state['trump']:
                if trickCard.value == 'J': #top card
                    BestCardOfTrick = trickCard
                    BestCardPlayer = playerindex
                elif BestCardOfTrick.suit==state['trump']and trickCard > BestCardOfTrick and not BestCardOfTrick.value=='J':
                    #higher trump than best card
                    BestCardOfTrick = trickCard
                    BestCardPlayer=playerindex
                elif not BestCardOfTrick.suit==state['trump']:
                    #Trump of trick
                    BestCardOfTrick = trickCard
                    BestCardPlayer=playerindex
            elif trickCard.suit== left_bower and trickCard.value=='J'and not BestCardOfTrick.suit== trump_suit and not BestCardOfTrick.value=='J':
                #is the left boweler without the right boweler played
                BestCardOfTrick = trickCard
                BestCardPlayer = playerindex
            elif not BestCardOfTrick.suit==state['trump'] and BestCardOfTrick.suit == trickCard.suit and trickCard>BestCardOfTrick:
                BestCardOfTrick = trickCard
                BestCardPlayer = playerindex
            playerindex = playerindex + 1

        betterCards =[]
        for card in unknowncards:
            if BestCardOfTrick.suit==trump_suit and card.suit==trump_suit and card.value>BestCardOfTrick.value or card.value=='J':
                betterCards.append(card)
            elif card.suit==left_bower and card.value==trump_suit and not BestCardOfTrick.suit==trump_suit and not BestCardOfTrick.value =='J':
                betterCards.append(card)
            elif BestCardOfTrick.suit == card.suit and card.value>BestCardOfTrick.value:
                betterCards.append(card)

        prob = (len(betterCards)/len(unknowncards)) #Prob of getting a better card

        if playerNum==1 or playerNum ==2: # still has one round of the enemy
            prob = 1-(1-prob)**len(state['playerCards']) # chance enemy has a better card
        prob = prob*(-1)
        if playerNum==2 and BestCardPlayer==0 or playerNum==3 and BestCardPlayer==1:
            #player's team is winning
            prob = prob * (-1)
        return prob
        # if % is + winning, if neg. Losing
        #find who has best card in trick
        # find all cards higher that still have to be played and you don't have

    def updateQtable(self,reward,learning_rate):
        oldQvalue = self.QTable.table[self.QCellToUpdate[0],self.QCellToUpdate[1],self.QCellToUpdate[2]]
        newValue = learning_rate * reward - oldQvalue
        self.QTable.table[self.QCellToUpdate[0],self.QCellToUpdate[1],self.QCellToUpdate[2]] = newValue

    def getTrickcards(self, dic):
        return [dic[i] for i in range(4) if dic[i] is not None]