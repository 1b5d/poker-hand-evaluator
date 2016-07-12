class PokerException(Exception):
    pass


class InvalidHand(PokerException):
    pass


class InvalidCard(PokerException):
    pass


class InvalidEvaluator(PokerException):
    pass
