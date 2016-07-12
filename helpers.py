from collections import Counter


def count_sort(iterable, reverse=True):
    counts = Counter(iterable)

    def comparer(first_item, second_item):
        return cmp(counts.get(first_item, 0), counts.get(second_item, 0)) or \
               cmp(first_item, second_item)
    return sorted(iterable, cmp=comparer, reverse=reverse)


def bit_sums(items):
    def reducer(first_item, second_item):
        max_len = max(len(first_item), len(second_item))
        first_item = (max_len - len(first_item)) * ['0'] + first_item
        second_item = (max_len - len(second_item)) * ['0'] + second_item
        return map(lambda x: int(x[0]) + int(x[1]),
                   zip(first_item, second_item))
    return reduce(reducer, map(lambda item: map(int, list(bin(item)[2:])), items))