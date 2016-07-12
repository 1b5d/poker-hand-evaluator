"""
contains definitions for all the evaluators used to evaluate
the different types of hands.
"""

from poker_exceptions import InvalidHand
from helpers import bit_sums, count_sort

# all the possible faces of the cards.
CARD_RANKS = '23456789TJQKA'

# all the possible suits of the cards.
CARD_SUITS = 'CDHS'

# a map from faces' symbols of the cards to their bit representations
CARD_BITRANKS = {name: 1 << index for index, name in enumerate(CARD_RANKS)}

# a map from suits' symbols of the cards to their bit representations
CARD_BITSUITS = {name: 1 << index << len(CARD_RANKS)
                 for index, name in enumerate(CARD_SUITS)}

# a bit mask to define the length of a card face representation
RANK_BITMASK = reduce(lambda x, y: x | y, CARD_BITRANKS.values())

# a bit mask to define the length of a card suit representation
SUIT_BITMASK = reduce(lambda x, y: x | y, CARD_BITSUITS.values())


class Evaluator(object):
    """
    represents a general evaluator of a hand type.
    contains the common methods for all evaluators.
    """
    def __init__(self, cards):
        """
        initializes an instance of Evaluator

        :param iterable cards: a list of cards
        :return: instance of Evaluator
        """
        self.cards = cards

    def get_card_victors(self):
        """
        returns a list of bit representations of the cards.

        :return iterable:
        """
        return map(lambda item: item.victor, self.cards)

    def get_sorted_ranks(self):
        """
        returns the cards faces' representations sorted according to the evaluator type.

        :return iterable:
        """
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return sorted(ranks, reverse=True)

    def __cmp__(self, other):
        """
        compares the evaluator with another Evaluator instance.

        :param Evaluator other: the other Evaluator instance to compare with.
        :return integer: negative if self < other, zero if self==other, positive if self > other.
        """
        cards = self.get_sorted_ranks()
        other_cards = other.get_sorted_ranks()

        if len(cards) != len(other_cards):
            raise InvalidHand('Cannot compare hands with different card counts')

        # compare highest cards in each hand, if they tie,
        # if the highest cards tie then the next highest cards are compared, and so on.
        for card, other_card in zip(cards, other_cards):
            if card == other_card:
                continue
            return cmp(card, other_card)

        # all cards are equal.
        return 0

    def __repr__(self):
        """
        :return: string representation of the Evaluator instance (the hand type).
        """
        return self.__str__()


class HighCard(Evaluator):
    """
    defines an Evaluator for the 'High Card' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'High Card' type, once the evaluation reaches here,
        then we can assume that the hand is definitely a 'High Card',
        since it has the lowest type value.

        :return bool: whether it matches the evaluator type or not.
        """
        return True

    def __str__(self):
        """
        :return string:
        """
        return 'High Card'
    

class OnePair(Evaluator):
    """
    defines an Evaluator for the 'One Pair' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'One Pair' hand type.
        this will validate that the bit counts
        of the cards has one '2' among them.

        :return bool: whether it matches the evaluator type or not.
        """
        cards = self.get_card_victors()
        total = bit_sums(map(lambda item: item & RANK_BITMASK, cards))
        return total.count(2) == 1

    def get_sorted_ranks(self):
        """
        returns the cards faces' representations sorted according to the 'One Pair' type.
        the duplicated cards are sorted first, then comes the rest of the cards.

        :return iterable:
        """
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        """
        :return string:
        """
        return 'One Pair'


class TwoPair(Evaluator):
    """
    defines an Evaluator for the 'Two Pairs' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'Two Pairs' hand type.
        this will validate that the bit counts
        of the cards has two '2' among them.

        :return bool: whether it matches the evaluator type or not.
        """
        cards = self.get_card_victors()
        total = bit_sums(map(lambda item: item & RANK_BITMASK, cards))
        return total.count(2) == 2

    def get_sorted_ranks(self):
        """
        returns the cards faces' representations sorted according to the 'Two Pairs' type.
        the duplicated cards are sorted first, then comes the rest of the cards.

        :return iterable:
        """
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        """
        :return string:
        """
        return 'Two Pairs'


class ThreeOfAKind(Evaluator):
    """
    defines an Evaluator for the 'Three of a Kind' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'Three of a Kind' hand type.
        this will validate that the bit counts
        of the cards has one '3' among them.

        :return bool: whether it matches the evaluator type or not.
        """
        cards = self.get_card_victors()
        total = bit_sums(map(lambda item: item & RANK_BITMASK, cards))
        return total.count(3) == 1

    def get_sorted_ranks(self):
        """
        returns the cards faces' representations sorted according to the 'Three of a Kind' type.
        the duplicated cards are sorted first, then comes the rest of the cards.

        :return iterable:
        """
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        """
        :return string:
        """
        return 'Three of a Kind'


class Straight(Evaluator):
    """
    defines an Evaluator for the 'Straight' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'Straight' hand type.
        this will shift all the bit representations (combined into one value using bitwise OR)
        once for each card to the left then do bitwise AND with the same value before shifting,
        then checks of any bit remains in at the end.

        :return bool: whether it matches the evaluator type or not.
        """
        cards = self.get_card_victors()
        concat = reduce(lambda x, y: (x & RANK_BITMASK) |
                                     (y & RANK_BITMASK), cards)
        for _ in range(1, len(cards)):
            concat &= (concat << 1)
        return concat > 0

    def __str__(self):
        """
        :return string:
        """
        return 'Straight'


class Flush(Evaluator):
    """
    defines an Evaluator for the 'Flush' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'Flush' hand type.
        this will do a bitwise AND between all suit representations of the cards,
        then if the result is not 0, its a Flush.

        :return bool: whether it matches the evaluator type or not.
        """
        cards = self.get_card_victors()
        return reduce(lambda x, y: (x & SUIT_BITMASK) &
                                   (y & SUIT_BITMASK), cards) > 0

    def __str__(self):
        """
        :return string:
        """
        return 'Flush'


class FullHouse(Evaluator):
    """
    defines an Evaluator for the 'Full House' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'Full House' hand type.
        this will check if the hand is both 'One Pair' and 'Three if a Kind'.

        :return bool: whether it matches the evaluator type or not.
        """
        return OnePair(self.cards).evaluate() and \
            ThreeOfAKind(self.cards).evaluate()

    def get_sorted_ranks(self):
        """
        returns the cards faces' representations sorted according to the 'Full House' type.
        the three matched cards come first, then the pair.

        :return iterable:
        """
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        """
        :return string:
        """
        return 'Full House'


class FourOfAKind(Evaluator):
    """
    defines an Evaluator for the 'Four of a Kind' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'Four of a Kind' hand type.
        this will validate that the bit counts
        of the cards has one '4' among them.

        :return bool: whether it matches the evaluator type or not.
        """
        cards = self.get_card_victors()
        total = bit_sums(map(lambda item: item & RANK_BITMASK, cards))
        return total.count(4) == 1

    def get_sorted_ranks(self):
        """
        returns the cards faces' representations sorted according to the 'Four of a Kind' type.
        the four matched cards come first, then other card.

        :return iterable:
        """
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        """
        :return string:
        """
        return 'Four of a Kind'


class StraightFlush(Evaluator):
    """
    defines an Evaluator for the 'Straight Flush' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'Straight Flush' hand type.
        this will check if the hand is both 'Straight' and 'Flush'.

        :return bool: whether it matches the evaluator type or not.
        """
        return Straight(self.cards).evaluate() and \
            Flush(self.cards).evaluate()

    def __str__(self):
        """
        :return string:
        """
        return 'Straight Flush'


class RoyalFlush(Evaluator):
    """
    defines an Evaluator for the 'Royal Flush' hand type.
    """
    def evaluate(self):
        """
        evaluates the 'Royal Flush' hand type.
        this will check if the hand 'Straight Flush'
        and also has a King card.

        :return bool: whether it matches the evaluator type or not.
        """
        cards = self.get_card_victors()
        return StraightFlush(self.cards).evaluate() and\
            any(CARD_BITRANKS[CARD_RANKS[-1]] &
                x & RANK_BITMASK for x in cards)

    def __str__(self):
        """
        :return string:
        """
        return 'Royal Flush'

# values of the hands
ROYAL_FLUSH = 1 << 9
STRAIGHT_FLUSH = 1 << 8
FOUR_OF_A_KIND = 1 << 7
FULL_HOUSE = 1 << 6
FLUSH = 1 << 5
STRAIGHT = 1 << 4
TREE_OF_A_KIND = 1 << 3
TWO_PAIR = 1 << 2
ONE_PAIR = 1 << 1
HIGH_CARD = 1 << 0

# a mapping between the values of the hands and
# the matching evaluator class for each one.
EVALUATORS = {
    ROYAL_FLUSH: RoyalFlush,
    STRAIGHT_FLUSH: StraightFlush,
    FOUR_OF_A_KIND: FourOfAKind,
    FULL_HOUSE: FullHouse,
    FLUSH: Flush,
    STRAIGHT: Straight,
    TREE_OF_A_KIND: ThreeOfAKind,
    TWO_PAIR: TwoPair,
    ONE_PAIR: OnePair,
    HIGH_CARD: HighCard,
}
