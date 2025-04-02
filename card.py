

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
