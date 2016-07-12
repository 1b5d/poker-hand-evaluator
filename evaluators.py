from poker_exceptions import InvalidHand
from helpers import bit_sums, count_sort

CARD_RANKS = '23456789TJQKA'
CARD_SUITS = 'CDHS'

CARD_BITRANKS = {name: 1 << index for index, name in enumerate(CARD_RANKS)}
CARD_BITSUITS = {name: 1 << index << len(CARD_RANKS)
                 for index, name in enumerate(CARD_SUITS)}

RANK_BITMASK = reduce(lambda x, y: x | y, CARD_BITRANKS.values())
SUIT_BITMASK = reduce(lambda x, y: x | y, CARD_BITSUITS.values())


class Evaluator(object):
    def __init__(self, cards):
        self.cards = cards

    def get_card_victors(self):
        return map(lambda item: item.victor, self.cards)

    def get_sorted_ranks(self):
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return sorted(ranks, reverse=True)

    def __cmp__(self, other):
        cards = self.get_sorted_ranks()
        other_cards = other.get_sorted_ranks()

        if len(cards) != len(other_cards):
            raise InvalidHand('Cannot compare hands with different card counts')

        for card, other_card in zip(cards, other_cards):
            if card == other_card:
                continue
            return cmp(card, other_card)

        return 0

    def __repr__(self):
        return self.__str__()


class HighCard(Evaluator):
    def evaluate(self):
        return True

    def __str__(self):
        return 'High Card'
    

class OnePair(Evaluator):
    def evaluate(self):
        cards = self.get_card_victors()
        total = bit_sums(map(lambda item: item & RANK_BITMASK, cards))
        return total.count(2) == 1

    def get_sorted_ranks(self):
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        return 'One Pair'


class TwoPair(Evaluator):
    def evaluate(self):
        cards = self.get_card_victors()
        total = bit_sums(map(lambda item: item & RANK_BITMASK, cards))
        return total.count(2) == 2

    def get_sorted_ranks(self):
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        return 'Two Pairs'


class ThreeOfAKind(Evaluator):
    def evaluate(self):
        cards = self.get_card_victors()
        total = bit_sums(map(lambda item: item & RANK_BITMASK, cards))
        return total.count(3) == 1

    def get_sorted_ranks(self):
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        return 'Three of a Kind'


class Straight(Evaluator):
    def evaluate(self):
        cards = self.get_card_victors()
        concat = reduce(lambda x, y: (x & RANK_BITMASK) |
                                     (y & RANK_BITMASK), cards)
        for _ in range(1, len(cards)):
            concat &= (concat << 1)
        return concat > 0

    def __str__(self):
        return 'Straight'


class Flush(Evaluator):
    def evaluate(self):
        cards = self.get_card_victors()
        return reduce(lambda x, y: (x & SUIT_BITMASK) &
                                   (y & SUIT_BITMASK), cards) > 0

    def __str__(self):
        return 'Flush'


class FullHouse(Evaluator):
    def evaluate(self):
        return OnePair(self.cards).evaluate() and \
            ThreeOfAKind(self.cards).evaluate()

    def get_sorted_ranks(self):
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        return 'Full House'


class FourOfAKind(Evaluator):
    def evaluate(self):
        cards = self.get_card_victors()
        total = bit_sums(map(lambda item: item & RANK_BITMASK, cards))
        return total.count(4) == 1

    def get_sorted_ranks(self):
        ranks = map(lambda item: item.victor & RANK_BITMASK, self.cards)
        return count_sort(ranks, reverse=True)

    def __str__(self):
        return 'Four of a Kind'


class StraightFlush(Evaluator):
    def evaluate(self):
        return Straight(self.cards).evaluate() and \
            Flush(self.cards).evaluate()

    def __str__(self):
        return 'Straight Flush'


class RoyalFlush(Evaluator):
    def evaluate(self):
        cards = self.get_card_victors()
        return Straight(self.cards).evaluate() and\
            Flush(self.cards).evaluate() and\
            any(CARD_BITRANKS[CARD_RANKS[-1]] &
                x & RANK_BITMASK for x in cards)

    def __str__(self):
        return 'Royal Flush'

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
