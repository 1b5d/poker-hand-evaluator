"""
contains definitions of helper functions to support evaluators.
"""

from collections import Counter


def count_sort(iterable, reverse=True):
    """
    sorts a list depending of the frequency of the items as a first dimension,
    then depending on the value itself as a second dimension.

    :param iterable iterable: values to be sorted.
    :param bool reverse: whether to sort in revere order or not.
    :return: new sorted list.
    """
    counts = Counter(iterable)

    def comparer(x, y):
        """
        a comparer function to be used as a basis of the sort.

        :param any x: the first item to compare
        :param any y: the second item to compare
        :return integer: negative if x<y, zero if x==y, positive if x>y.
        """
        return cmp(counts.get(x, 0), counts.get(y, 0)) or \
            cmp(x, y)
    return sorted(iterable, cmp=comparer, reverse=reverse)


def bit_sums(items):
    """
    generates an array of arithmetic sums of the bits
    of a list of integers.

    example: bit_sums([21, 28]) -> [2, 1, 2, 0, 1]
    explanation: [21, 28] -> [0b10101, 0b11100] -> [2, 1, 2, 0, 1]

    :param iterable items: list of integers
    :return iterable: list of the counts of integers' bits
    """
    def reducer(first_item, second_item):
        """
        a function that represents the calculation between only 2 items.
        :param first_item:
        :param second_item:
        :return iterable: list of the counts of integers' bits
        """
        # making both at the same length
        max_len = max(len(first_item), len(second_item))
        first_item = (max_len - len(first_item)) * ['0'] + first_item
        second_item = (max_len - len(second_item)) * ['0'] + second_item

        # summing up the bits
        return map(lambda x: int(x[0]) + int(x[1]),
                   zip(first_item, second_item))

    # generalizing the solution to more than 2 items.
    return reduce(reducer, map(lambda item: map(int, list(bin(item)[2:])), items))
