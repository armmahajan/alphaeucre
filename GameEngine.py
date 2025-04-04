import random
from card import Card
from typing import Callable
from AIManager import AIManager
class Euchre:
    def __init__(self, AI = False) -> None:
        if AI:
            self.AI_Manager = AIManager()  # create the AI players
        else:
            self.AI_Manager = None
        self.state = {
            'phase': 'trumpFaceUp', # One of: trumpFaceUp, dealerDiscard, trumpFaceDown, trick
            'trump': None, # Hack: If trump is a single value it is face up naming, if it is a list, it is face down and the items are the options
            'dealer': 3,
            'leader': 0,
            'lead_suit': None, 
            'cards': {
                0: [],
                1: [],
                2: [],
                3: []
            },
            'current_trick': {
                0: None,
                1: None,
                2: None,
                3: None,
            }, # Each index represents that players cards
            'cards_played': [], #TODO:
            'trick_points' : { # 
                0: 0,
                1: 0,
                2: 0,
                3: 0,
            },
            'makers': set(),
            'defenders': set()
        }
        self.points = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
        }
        self.players: dict[int, Callable[[dict], int | bool | str]] = {
            0: self._AIPlayer if AI else self._humanPlayer,
            1: self._AIPlayer if AI else self._humanPlayer,
            2: self._AIPlayer if AI else self._humanPlayer,
            3: self._AIPlayer if AI else self._humanPlayer
        }
        self.current_turn = 0
        self.deck = self._createCards()
        self.rankedCards = []
        self.Pindex=0

    def registerCallback(self, playerID, callback):
        '''
        Register a different callback for the player with playerID. A sample callback function
        is self._humanPlayer.
        '''
        self.players[playerID] = callback

    def _humanPlayer(self, state) -> int | bool | str:
        print("\n\n")
        match state['phase']:
            case 'trumpFaceUp':
                print(f'Your hand: {state["cards"]}')
                print(f'Trump Offering (faceup): {state['trump']}')
                res = input('Take the trump offering (y/n): ')
                return True if res == 'y' else False
            # case 'trumpFaceDown':
            #     options = state['trump']
            #     print(f'Your hand: {state["cards"]}')
            #     print(f'Trump suit options: {state['trump']}')
            #     # If not dealer
            #     res = input('Would you like to choose one of the trump options? (<SUIT>, n)')
            #     # TODO: handle input
            #     return False
            case 'dealerDiscard':
                return False
            case 'trick':
                print("\n\n",state['PlayerID'])
                print(f'Your hand: {state['cards']}')
                print(f'Your hand2: {state['playerCards']}')
                print(f'Current Trick: {state['current_trick']}')
                res = input(f'Which card would you like to play (0-indexed)? ')
                return int(res)
            case _:
                raise ValueError('Game state phase has an invalid value.')

    def _AIPlayer(self, state) -> int | bool | str:
        match state['phase']:
            case 'trumpFaceUp':
                return True
                #print(f'Your hand: {state["cards"]}')
                #print(f'Trump Offering (faceup): {state['trump']}')
                #res = input('Take the trump offering (y/n): ')
                #return True if res == 'y' else False
            # case 'trumpFaceDown':
            #     options = state['trump']
            #     print(f'Your hand: {state["cards"]}')
            #     print(f'Trump suit options: {state['trump']}')
            #     # If not dealer
            #     res = input('Would you like to choose one of the trump options? (<SUIT>, n)')
            #     # TODO: handle input
            #     return False
            case 'dealerDiscard':
                return False
            case 'trick':
                res = self.AI_Manager.movePlayer(state,self.Pindex)
                print("\n\n", state['PlayerID'])
                print(f'Your hand: {state['cards']}')
                print(f'Current Trick: {state['current_trick']}')
                print(f"AI picked: {res}")
                #res = input(f'Which card would you like to play (0-indexed)? ')
                self.Pindex = self.Pindex+1
                if self.Pindex >3:
                    self.Pindex=0
                return int(str(res))
            case _:
                raise ValueError('Game state phase has an invalid value.')

    def _createCards(self) -> list[Card]:
        suits = ['diamonds', 'clubs', 'spades', 'hearts']
        values = ['9', '10', 'J', 'Q', 'K', 'A']
        return [Card(value, suit) for suit in suits for value in values]

    def _deal(self) -> None:
        random.shuffle(self.deck)
        for i in range(4):
            players_cards = []
            for _ in range(3):
                players_cards.append(self.deck.pop())
            self.state['cards'][(self.state['dealer']+i+1)%4].extend(players_cards)
        for i in range(4):
            players_cards = []
            for _ in range(2):
                players_cards.append(self.deck.pop())
            self.state['cards'][(self.state['dealer']+i+1)%4].extend(players_cards)

    def _gameStatePlayersView(self, playerID: int) -> dict:
        # Filter cards
        playersCards: list[Card] = self.state['cards'][playerID]

        playableCards = []
        for card in playersCards:
            if card.suit == self.state['lead_suit']:
                playableCards.append(card)
        if len(playableCards) == 0:
            playableCards = playersCards

        playerState = {
            'phase' : self.state['phase'],
            'makers': True if playerID in self.state['makers'] else False,
            'PlayerID': playerID,
            'trump': self.state['trump'],
            'dealer' : self.state['dealer'],
            'cards': playableCards,
            'playerCards': self.state['cards'][playerID],
            'current_trick': self.state['current_trick'],
            'cards_played': self.state['cards_played']
        }
        return playerState

    def _trumpNamingFaceUp(self) -> tuple[bool, int]:
        self.state['trump'] = self.deck.pop()
        self.state['cards_played'].append(self.state['trump'])
        for i in range(4):
            if self.players[(self.state['leader']+i)%4](self._gameStatePlayersView(i)):
                self.state['trump'] = self.state['trump'].suit
                return (True, i)
        return (False, -1)

    # def _trumpNamingFaceDown(self):
    #     options = ['diamonds', 'spades', 'hearts', 'clubs']
    #     options.remove(self.state['trump'])
    #     self.state['trump'] = options
    #     for i in range(4):
    #         res = self.players[(self.state['leader']+i+1)%4](self._gameStatePlayersView(i))
    #         # TODO: handle res and force the dealer
    
    def _rankCards(self):
        trumpValues = ['9', '10', 'Q', 'K', 'A', 'J', 'J']
        # values = ['9', '10', 'J', 'Q', 'K', 'A']
        trump_suit = self.state['trump']
        left_bower = None
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
        orderedCards: list[Card] = [Card(value, trump_suit) for value in trumpValues] 
        orderedCards[-2].suit = left_bower
        self.rankedCards = orderedCards

    def _trick(self):
        for i in range(4):
            # Get player to choose card
            playerID = (self.state['leader']+i)%4
            playersState = self._gameStatePlayersView(playerID)
            res = self.players[playerID](playersState)
            chosenCard: Card = playersState['cards'][res]
            # Delete card from players hand
            for j in range(len(self.state['cards'][playerID])):
                if self.state['cards'][playerID][j] == chosenCard:
                    self.state['cards'][playerID].pop(j)
                    break
            # Set led suit
            if playerID == self.state['leader']:
                self.state['lead_suit'] = chosenCard.suit
            self.state['current_trick'][playerID] = chosenCard
    
    # TODO: handle edge cases
    # Trump -> lead suit -> in order
    def _evaluateTrick(self):
        playerScores = [-1, -1, -1, -1]
        winnerFound = False
        winner = -1
        # Check for trump suit cards
        for score, rankedCard in enumerate(self.rankedCards):
            for id, card in self.state['current_trick'].items():
                if card == rankedCard:
                    playerScores[id] = score
                    winnerFound = True
        # If no trump cards, handle based on lead card
        if not winnerFound:
            winningCard = None
            for id, card in self.state['current_trick'].items():
                if card.suit == self.state['lead_suit']:
                    if winningCard == None:
                        winningCard = card
                        winner = id
                    elif card > winningCard:
                        winningCard = card
                        winner = id
        else:
            winningScore = -1
            for idx, score in enumerate(playerScores):
                if score > winningScore:
                    winningScore = score
                    winner = idx
        self.state['trick_points'][winner] += 1
        return winner

    def _resetGameState(self):
        self.state = {
            'phase': 'trumpFaceUp', # One of: trumpFaceUp, dealerDiscard, trumpFaceDown, trick
            'trump': None, # Hack: If trump is a single value it is face up naming, if it is a list, it is face down and the items are the options
            'dealer': 3,
            'leader': 0,
            'lead_suit': None, 
            'cards': {
                0: [],
                1: [],
                2: [],
                3: []
            },
            'current_trick': {
                0: None,
                1: None,
                2: None,
                3: None,
            }, # Each index represents that players cards
            'cards_played': [], #TODO:
            'trick_points' : { # 
                              0: 0,
                              1: 0,
                              2: 0,
                              3: 0,
                              },
            'makers': set(),
            'defenders': set()
        }
        self.deck = self._createCards()
    
    def _isGameOver(self):
        makerPoints = sum([self.state['trick_points'][i] for i in self.state['makers']])
        defenderPoints = sum([self.state['trick_points'][i] for i in self.state['makers']])
        if makerPoints == 5:
            return True
        if defenderPoints == 3:
            return True
        if makerPoints == 3 and defenderPoints == 2:
            return True
        return False
    
    def _assignPoints(self):
        makerPoints = sum([self.state['trick_points'][i] for i in self.state['makers']])
        defenderPoints = sum([self.state['trick_points'][i] for i in self.state['makers']])
        if makerPoints == 5:
            print('Makers get 2 points!')
            for maker in self.state['makers']:
                self.points[maker] += 2
        elif makerPoints == 4 or makerPoints == 3:
            print('Makers get 1 point!')
            for maker in self.state['makers']:
                self.points[maker] += 1
        elif defenderPoints == 3:
            print('Defenders get 2 points!')
            for defender in self.state['defenders']:
                self.points[defender] += 2

    def _nextTrick(self):
        pass

    def gameLoop(self):
        while True:
            self._deal()

            res, player_id = self._trumpNamingFaceUp()
            if res:
                self.state['phase'] = 'trick'
                self.state['makers'].add(player_id)
                self.state['makers'].add((player_id+2)%4)
                self.state['defenders'].add((player_id+1)%4)
                self.state['defenders'].add((player_id+3)%4)
            self._rankCards()
            print(self.rankedCards)
            for _ in range(5):
                self._trick()
                trick_winner = self._evaluateTrick()
                self.state['leader'] = trick_winner
                print(f"Trick winner is {trick_winner}")
                print(f"Current Points:\n{self.state['trick_points']}")
                # Move played cards to the cards_played and reset current_trick
                self.state['cards_played'].extend([v for _, v in self.state['current_trick'].items()])
                for k in self.state['current_trick']:
                    self.state['current_trick'][k] = None
                if self._isGameOver(): 
                    break
            print('Games Over!')
            self._assignPoints()
            self._resetGameState()

    def gameLoopAI(self):

        while True:
            self._deal()
            res, player_id = self._trumpNamingFaceUp()
            if res:
                self.state['phase'] = 'trick'
                self.state['makers'].add(player_id)
                self.state['makers'].add((player_id + 2) % 4)
                self.state['defenders'].add((player_id + 1) % 4)
                self.state['defenders'].add((player_id + 3) % 4)
            self._rankCards()
            print()
            for _ in range(5):
                self._trick()
                trick_winner = self._evaluateTrick()
                pwin = (trick_winner-self.state['leader'])%4
                for i in range(4):
                    reward=0
                    if i ==pwin:
                        reward = 10
                    else:
                        reward = -10
                    self.AI_Manager.updateQTable(i,reward)
                self.AI_Manager.getQtable().updateCounter()
                self.state['leader'] = trick_winner
                print(f"Trick winner is {trick_winner}")
                print(f"Current Points:\n{self.state['trick_points']}")
                # Move played cards to the cards_played and reset current_trick
                self.state['cards_played'].extend([v for _, v in self.state['current_trick'].items()])
                for k in self.state['current_trick']:
                    self.state['current_trick'][k] = None
                if self._isGameOver():
                    break
            print('Games Over!')
            print(self.AI_Manager.getQtable().getTable())
            if not self.AI_Manager.isTraining():
                exit(0)
            self._assignPoints()
            self._resetGameState()


####################################################
        def movePlayer(state):
            match state['phase']:
                case 'trick':
                    playableCards = state['cards']  # this is the array of playable cards for the current trick
                    currentTrick = state[
                        'current_trick']  # this is an array of cards that have been played in the current trick
                    # The logic for choosing one of the cards in playable cards goes here
                    cardToPlay = ...  # this would be the index of the card you want to play out of playableCards
                    return cardToPlay
