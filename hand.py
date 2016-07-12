"""
contains definitions of classes that represents
Hands in a poker game and playing cards.
"""

from evaluators import *
from poker_exceptions import InvalidHand, InvalidCard, InvalidEvaluator

# contains a mapping from the binaty representation of the card
# faces to the symbols of the faces.
INVERSED_CARD_BITRANKS = {v: k for k, v in CARD_BITRANKS.items()}

# contains a mapping from the binaty representation of the card
# suits to the symbols of the suits.
INVERSED_CARD_BITSUITS = {v: k for k, v in CARD_BITSUITS.items()}


class Card(object):
    """
    Class to represents a playing card
    """
    def __init__(self, desc):
        """
        initializes the Card with the face symbol and the suit symbol.

        :param string desc: the symbols that defines a card, ex: '9S'
        :return: instance of Card
        """
        if desc is None or len(desc) != 2:
            raise InvalidCard('Invalid card initialization')

        if desc[0] is None or not len(desc[0]) or\
                desc[0] not in CARD_BITRANKS:
            raise InvalidCard('Invalid card number')

        if desc[1] is None or not len(desc[0]) or\
                desc[1] not in CARD_BITSUITS:
            raise InvalidCard('Invalid card suit')

        rank = CARD_BITRANKS.get(desc[0])
        suit = CARD_BITSUITS.get(desc[1])
        self.victor = rank | suit

    def __str__(self):
        """
        generates a string description of the card.

        :return string:
        """
        rank = INVERSED_CARD_BITRANKS.get(self.victor & RANK_BITMASK)
        suit = INVERSED_CARD_BITSUITS.get(self.victor & SUIT_BITMASK)
        return ''.join([rank, suit])

    def __cmp__(self, other):
        """
        compares the card with another Card instance.

        :param other: the other Card instance to compare with.
        :return integer: negative if self < other, zero if self==other, positive if self > other.
        """
        return cmp(self.victor & RANK_BITMASK, other.victor & RANK_BITMASK)

    def __repr__(self):
        """
        :return: string representation of the Card instance
        """
        return self.__str__()


class Hand(object):
    """
    Class to represent a Hand in a poker game.
    """
    @classmethod
    def from_string(cls, cards_str):
        """
        initializes a Hand instance using a string that represents cards.

        example: Hand.from_string('TS JS QS KS AS') -> Hand

        :param string cards_str: string that represents cards.
        :return: instance of Hand.
        """
        if cards_str is None or not len(cards_str):
            raise InvalidHand('Invalid initialization of hand')
        cards = cards_str.split()
        hand = Hand()
        hand.cards = [Card(card_str) for card_str in cards]
        evaluator = hand.get_evaluator()
        hand.value = evaluator.evaluate()
        return hand

    def __init__(self):
        """
        initializes the Hand instance with necessary attributes.
        :return: instance of Hand.
        """
        self.cards = []
        self.value = None
        self._evaluator = None

    def __str__(self):
        """
        generates a string description of the hand.

        :return string:
        """
        return '<hand %s, \'%s\'>' % (self.cards, self.get_evaluator())

    def __repr__(self):
        """
        :return: string representation of the Hand instance
        """
        return self.__str__()

    def __cmp__(self, other):
        """
        compares the hand with another Hand instance.
        this will first compare the evaluated type of the hand,
        if they are equal, then compares the values of the cards,
        taking into consideration the evaluated type during that.

        :param Hand other: the other hand instance
        :return integer: negative if self < other, zero if self==other, positive if self > other.
        """
        return cmp(self.value, other.value) or\
            cmp(self.get_evaluator(), other.get_evaluator())

    def get_evaluator(self):
        """
        returns the evaluator that matches the hand evaluated type,
        this will loop through a sorted list of evaluators and return
        the first matched one by evaluating the hand using each one of them.
        :return:
        """
        if self._evaluator is None:
            for value, obj in sorted(EVALUATORS.items(), reverse=True):
                evaluator = obj(self.cards)
                if evaluator.evaluate():
                    self._evaluator = evaluator
                    break
            if self._evaluator is None:
                raise InvalidEvaluator('Could not evaluate hand')
        return self._evaluator
