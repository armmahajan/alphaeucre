
class GameMaster:

    def CreateCardDeck(self):
        deck=[]
        deckindex=0
        for i in range(1,4):
            for k in range(1,13):
                deck[deckindex] = card(k,i)
                deckindex = deckindex +1
        return deck

    def GameMaster(self):
        deck= self.CreateCardDeck()



class card:

    def __init__(self):
        self.value = None
        self.suit = None
        self.arrSuit = ['S', 'C', 'H', 'D']

    def card(self, value, suit):
        """
        defines card
        :param value:

            A= 1
            2-10 as is.
            11 = J
            12 = Q
            13 = K
        :param suit:
            1 = spades
            2 = clubs
            3 = hearts
            4 = diamonds

        :return: card object
        """
        self.value = value;
        self.suit = suit;

    def getSuit(self):
        return self.arrSuit[self.suit - 1]

    def getValue(self):

        if self.value == 1:
            return "A"
        elif self.value <= 10:
            return str(self.value)
        else:
            arr = ["J", "Q", "K"]
            return str(arr[self.value - 11])

    def printCard(self):
        Cardstring = "("
        if self.value == 1:
            Cardstring = Cardstring + "A"
        elif self.value <= 10:
            Cardstring = Cardstring + str(self.value)
        else:
            arr = ["J", "Q", "K"]
            Cardstring = Cardstring + str(arr[self.value - 11])

        Cardstring = Cardstring + ", " + self.arrSuit[self.suit - 1] + ") "

        return Cardstring