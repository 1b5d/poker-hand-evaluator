from hand import Hand, Card
from poker_exceptions import PokerException

if __name__ == '__main__':
    try:
        print Hand.from_string('TS JS QS KS AS')
        print Hand.from_string('5S 6S 7S 8S 9S')
        print Hand.from_string('7S TC TH TS TD')
        print Hand.from_string('5H 5C QD QC QS')
        print Hand.from_string('2D 3D 7D QD AD')
        print Hand.from_string('4D 5D 6D 7H 8D')
        print Hand.from_string('7S TC TH 8S 8D')

        royal_flush = Hand.from_string('TS JS QS KS AS')
        four_of_a_kind = Hand.from_string('7S TC TH TS TD')

        two_pairs = Hand.from_string('7S TC TH 6S 6D')
        other_two_pairs = Hand.from_string('7S TC TH 5S 5D')

        print two_pairs > other_two_pairs
        print royal_flush > four_of_a_kind

        flush = Hand.from_string('2D 3D 7D QD AD')
        straight = Hand.from_string('4D 5D 6D 7H 8D')

        print flush < four_of_a_kind

        print Card('KS') > Card('TS')

    except PokerException, e:
        print 'Error: %s' % e.message