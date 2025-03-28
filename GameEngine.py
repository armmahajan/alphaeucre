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

class Euchre:
    def __init__(self) -> None:
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
        }
        self.points = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
        }
        self.players: dict[int, Callable[[dict], Card | bool | str]] = {
            0: self._humanPlayer,
            1: self._humanPlayer,
            2: self._humanPlayer,
            3: self._humanPlayer
        }
        self.current_turn = 0
        self.deck = self._createCards()

    def _humanPlayer(self, state) -> Card | bool | str:
        match state['phase']:
            case 'trumpFaceUp':
                print(f'Your hand: {state["cards"]}')
                print(f'Trump Offering (faceup): {state['trump']}')
                res = input('Take the trump offering (y/n): ')
                return True if res == 'y' else False
            case 'trumpFaceDown':
                options = state['trump']
                print(f'Your hand: {state["cards"]}')
                print(f'Trump suit options: {state['trump']}')
                # If not dealer
                res = input('Would you like to choose one of the trump options? (<SUIT>, n)')
                # TODO: handle input
                return False
            case 'dealerDiscard':
                return False
            case 'trick':
                return False
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
            self.state['cards'][i].extend(players_cards)
        for i in range(4):
            players_cards = []
            for _ in range(2):
                players_cards.append(self.deck.pop())
            self.state['cards'][i].extend(players_cards)

    def _gameStatePlayersView(self, playerID: int) -> dict:
        playerState = {
            'started' : self.state['started'],
            'trump': self.state['trump'],
            'dealer' : self.state['dealer'],
            'cards': self.state['cards'][playerID],
        }
        return playerState

    def _trumpNamingFaceUp(self) -> tuple[bool, int]:
        self.state['trump'] = self.deck.pop()
        for i in range(4):
            if self.players[i](self._gameStatePlayersView(i)):
                return (True, i)
        return (False, -1)

    def _trumpNamingFaceDown(self):
        options = ['diamonds', 'spades', 'hearts', 'clubs']
        options.remove(self.state['trump'])
        self.state['trump'] = options
        for i in range(4):
            res = self.players[i](self._gameStatePlayersView(i))
            # TODO: handle res and force the dealer
            
    def _trick(self):
        for i in range(4):
            res = self.players[i](self._gameStatePlayersView(i))

    def _evaluateTrick(self):
        pass

    def gameLoop(self):
        pass

def main():
    euchre = Euchre()
    euchre._deal()
    print(euchre.state)
    
if __name__ == "__main__":
    main()

