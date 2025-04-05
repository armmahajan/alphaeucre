import random
from typing import Callable

class Card:
    def __init__(self, value: str, suit: str) -> None:
        self.value = value
        self.suit = suit
    
    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls} ({self.value}, {self.suit})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card): 
            return False
        return True if self.value == other.value and self.suit == other.suit else False
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        nums = set(['9', '10'])
        faces = set(['J', 'Q', 'K', 'A'])

        if other.value in nums and self.value in faces:
            return True
        if other.value in faces and self.value in nums:
            return False
        if self.value in nums and other.value in nums:
            return True if int(self.value) > int(other.value) else False
        if self.value in faces and other.value in faces:
            orderedFaces = ['J', 'Q', 'K', 'A']
            selfScore, otherScore = -1, -1
            for i, val in enumerate(orderedFaces):
                if self.value == val:
                    selfScore = i
                if other.value == val:
                    otherScore = i
            return True if selfScore > otherScore else False
        raise ValueError(f'Could not compare values {other} and {self}')

    def __lt__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        nums = set(['9', '10'])
        faces = set(['J', 'Q', 'K', 'A'])

        if other.value in nums and self.value in faces:
            return False
        if other.value in faces and self.value in nums:
            return True
        if self.value in nums and other.value in nums:
            return False if int(self.value) > int(other.value) else True
        if self.value in faces and other.value in faces:
            orderedFaces = ['J', 'Q', 'K', 'A']
            selfScore, otherScore = -1, -1
            for i, val in enumerate(orderedFaces):
                if self.value == val:
                    selfScore = i
                if other.value == val:
                    otherScore = i
            return False if selfScore > otherScore else True
        raise ValueError(f'Could not compare values {other} and {self}')

class Euchre:
    def __init__(self) -> None:
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
            0: self._humanPlayer,
            1: self._humanPlayer,
            2: self._humanPlayer,
            3: self._humanPlayer
        }
        self.current_turn = 0
        self.deck = self._createCards()
        self.rankedCards = []

    def registerCallback(self, playerID, callback):
        '''
        Register a different callback for the player with playerID. A sample callback function
        is self._humanPlayer.
        '''
        self.players[playerID] = callback

    def _humanPlayer(self, state) -> int | bool | str:
        match state['phase']:
            case 'trumpFaceUp':
                print(f'Your hand: {state["cards"]}')
                print(f'Trump Offering (faceup): {state['trump']}')
                complete = False
                while not complete:
                    res = input('Take the trump offering (y/n): ')
                    if res.upper() not in ['Y', 'N']:
                        print('Invalid input. Please enter y or n.')
                        continue
                    else:
                        return True if res.lower() == 'y' else False
            # case 'trumpFaceDown':
            #     options = state['trump']
            #     print(f'Your hand: {state["cards"]}')
            #     print(f'Trump suit options: {state['trump']}')
            #     # If not dealer
            #     res = input('Would you like to choose one of the trump options? (<SUIT>, n)')
            #     # TODO: handle input
            #     return False
            case 'makeTrump':
                if self._validOrderUp(0):
                    # Discard for flipped trump card
                    self.state['cards'][self.state['dealer']] = self._discard()
                # Checking if the third player wants to order up the dealer
                elif self._validOrderUp(2):
                    # Discard for flipped trump card
                    self.state['cards'][self.state['dealer']] = self._discard()
                # Else the dealer picks up the card
                else:
                    # Discard for flipped trump card
                    self.state['cards'][self.state['dealer']] = self._discard()
                return True
            case 'trick':
                print(f'Your hand: {state['cards']}')
                print(f'Current Trick: {state['current_trick']}')
                complete = False
                while not complete:
                    res = input(f'Which card would you like to play (0-indexed)? ')
                    if int(res) > len(state['cards']) - 1 or int(res) < 0:
                        print('Invalid input. Please enter a valid card index.')
                        continue
                    else:
                        return int(res)
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

        print(f"Cards Dealt: {self.state['cards']}")

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
            'trump': self.state['trump'],
            'dealer' : self.state['dealer'],
            'cards': playableCards,
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


    def _validOrderUp(self, index):
        count = 0
        score = 0
        ranks = [["9", 1], ["10", 2], ["J", 8], ["Q", 4], ["K", 5], ["A", 6]]

        # Iterate through players cards
        for card in self.state['cards'][index]:
            # If matched trump suit score the card
            if card.suit == self.state['trump']:
                for rank in ranks:
                    if card.value == rank[0]:
                        score += rank[1]
                        count += 1
            # If matched the left bower score it
            elif card == self.get_left_bower():
                score += 7
                count += 1

        # If hand has at least 2 trump cards that total to a score of 16
        if count >= 2 and score >= 16:
            return True
        else:
            return False


    def get_left_bower(self):
        # Hearts: Left bower is Jack of Diamonds
        if self.state['trump'] == 'hearts':
            return 'Card (J diamonds)'
        # Diamonds: Left bower is Jack of Hearts
        elif self.state['trump'] == 'diamonds':
            return 'Card (J hearts)'
        # Spades: Left bower is Jack of Clubs
        elif self.state['trump'] == 'spades':
            return 'Card (J clubs)'
        # Clubs: Left bower is Jack of Spades
        elif self.state['trump'] == 'clubs':
            return 'Card (J spades)'
        return None


    def _discard(self):
        hand = [[], [], [], []]
        ranks = [["9", 1], ["10", 2], ["J", 3], ["Q", 4], ["K", 5], ["A", 6]]
        makes = list({"hearts", "diamonds", "spades", "clubs"} - {self.state['trump']})
        low_one_suit = ["", 10]
        low = ["", 10]
        low_trump = ["", 10]

        # Iterating through dealers cards
        for card in self.state['cards'][self.state['dealer']]:
            # Matching suits togethers
            if card.suit != self.state['trump']:
                if card.suit == makes[0]:
                    hand[0].append(card)
                elif card.suit == makes[1]:
                    hand[1].append(card)
                elif card.suit == makes[2]:
                    hand[2].append(card)
            else:
                hand[3].append(card)
        # Iterating through collections of suits
        for suit in hand:
            # If there is exactly one card of a suit
            if len(suit) == 1 and suit[0].suit != self.state['trump']:
                for value in ranks:
                    if suit[0].value == value[0]:
                        # If card value is lower than previously saved value
                        if value[1] < low_one_suit[1]:
                            low_one_suit = [suit[0], value[1]]
            # If there exists cards in suit
            elif len(suit) != 0:
                for card in suit:
                    # Iterate through card ranks to match card
                    for value in ranks:
                        # Keep trump suit separate
                        if suit != hand[3]:
                            # If card value is lower than previously saved value
                            if card.value == value[0]:
                                if value[1] < low[1]:
                                    low = [card, value[1]]
                        # If card value is lower than previously saved value
                        elif card.value == value[0] and card.suit == self.state['trump']:
                            low_trump = [card, value[1]]
        # If card of single suit is lower than a King, discard -> add trump -> return hand
        if low_one_suit[1] <= 4:
            new_hand = list(self.state['cards'][self.state['dealer']])
            new_hand.append(self.state['cards_played'][0])
            new_hand.remove(low_one_suit[0])
            return new_hand
        # Else lowest card of non-trump suit, discard -> add trump -> return hand
        elif low[1] < 8:
            new_hand = list(self.state['cards'][self.state['dealer']])
            new_hand.append(self.state['cards_played'][0])
            new_hand.remove(low[0])
            return new_hand
        # Else lowest trump card, discard -> add trump -> return hand
        else:
            new_hand = list(self.state['cards'][self.state['dealer']])
            new_hand.append(self.state['cards_played'][0])
            new_hand.remove(low_trump[0])
            return new_hand


    def _rankCards(self):
        trumpValues = ['9', '10', 'Q', 'K', 'A', 'J', 'J']
        # values = ['9', '10', 'J', 'Q', 'K', 'A']
        trump_suit = self.state['trump']
        left_bower = None
        if trump_suit == 'diamonds':
            left_bower = 'hearts'
        elif trump_suit == 'hearts':
            left_bower = 'diamonds'
        elif trump_suit == 'spades':
            left_bower = 'clubs'
        elif trump_suit == 'clubs':
            left_bower = 'spades'
        elif left_bower == None:
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
            # The Second player cannot order the dealer up as they are teammates
            # Checking if the first player wants to order up the dealer
            if self._validOrderUp(0):
                # Discard for flipped trump card
                self.state['cards'][self.state['dealer']] = self._discard()
            # Checking if the third player wants to order up the dealer
            elif self._validOrderUp(2):
                # Discard for flipped trump card
                self.state['cards'][self.state['dealer']] = self._discard()
            # Else the dealer picks up the card
            else:
                # Discard for flipped trump card
                self.state['cards'][self.state['dealer']] = self._discard()
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

####################################################

def main():
    euchre = Euchre()
    euchre.gameLoop()
    
if __name__ == "__main__":
    main()

