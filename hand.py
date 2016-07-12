from evaluators import *
from poker_exceptions import InvalidHand, InvalidCard, InvalidEvaluator

INVERSED_CARD_BITRANKS = {v: k for k, v in CARD_BITRANKS.items()}
INVERSED_CARD_BITSUITS = {v: k for k, v in CARD_BITSUITS.items()}


class Card(object):
    def __init__(self, desc):
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
        rank = INVERSED_CARD_BITRANKS.get(self.victor & RANK_BITMASK)
        suit = INVERSED_CARD_BITSUITS.get(self.victor & SUIT_BITMASK)
        return ''.join([rank, suit])

    def __cmp__(self, other):
        return cmp(self.victor & RANK_BITMASK, other.victor & RANK_BITMASK)

    def __repr__(self):
        return self.__str__()


class Hand(object):
    @classmethod
    def from_string(cls, cards_str):
        if cards_str is None or not len(cards_str):
            raise InvalidHand('Invalid initialization of hand')
        cards = cards_str.split()
        hand = Hand()
        hand.cards = [Card(card_str) for card_str in cards]
        evaluator = hand.get_evaluator()
        hand.value = evaluator.evaluate()
        return hand

    def __init__(self):
        self.cards = []
        self.value = None
        self._evaluator = None

    def __str__(self):
        return '<hand %s, \'%s\'>' % (self.cards, self.get_evaluator())

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(self.value, other.value) or\
            cmp(self.get_evaluator(), other.get_evaluator())

    def get_evaluator(self):
        if self._evaluator is None:
            for value, obj in sorted(EVALUATORS.items(), reverse=True):
                evaluator = obj(self.cards)
                if evaluator.evaluate():
                    self._evaluator = evaluator
                    break
            if self._evaluator is None:
                raise InvalidEvaluator('Could not evaluate hand')
        return self._evaluator
