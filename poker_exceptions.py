"""
contains definitions of the different exceptions that can occur
during the application execution.
"""


class PokerException(Exception):
    """
    a parent of all the exceptions that happens in the app.
    """
    pass


class InvalidHand(PokerException):
    """
    an exception that happens upon creating an invalid Hand.
    """
    pass


class InvalidCard(PokerException):
    """
    an exception that happens upon creating an invalid Card.
    """
    pass


class InvalidEvaluator(PokerException):
    """
    an exception that happens upon an error while evaluating the Hand.
    """
    pass
