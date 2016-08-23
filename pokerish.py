from operator import attrgetter
from itertools import groupby, chain
from collections import namedtuple


# hands

class Hand(object):
    def __init__(self, cards):
        if len(cards) != 5:
            raise InvalidHand(
                "poker hands must have five cards, got %d" % len(cards))

        duplicate = find_duplicate(cards)
        if duplicate:
            raise InvalidHand(
                "poker hands can't have two of the same card: %s" % duplicate)

        self.cards = cards
        self.category, rank_within_category = evaluate_hand(self)
        self.rank = [self.category.rank] + rank_within_category

    @classmethod
    def from_string(cls, string):
        return cls(map(Card, string.split()))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        cards = ', '.join(map(str, self.cards))
        return "<hand [%s], '%s'>" % (cards, self.category.name)

    def __cmp__(self, other):
        if self.rank == other.rank:
            return 0
        elif self.rank > other.rank:
            return 1
        else:
            return -1


class InvalidHand(Exception):
    pass


# categories

Category = namedtuple('Category', 'rank name')

HIGH_CARD = Category(0, "High Card")
ONE_PAIR = Category(1, "One Pair")
TWO_PAIR = Category(2, "Two Pair")
THREE_OF_A_KIND = Category(3, "Three of a Kind")
STRAIGHT = Category(4, "Straight")
FLUSH = Category(5, "Flush")
FULL_HOUSE = Category(6, "Full House")
FOUR_OF_A_KIND = Category(7, "Four of a Kind")
STRAIGHT_FLUSH = Category(8, "Straight Flush")
ROYAL_FLUSH = Category(9, "Royal Flush")


def evaluate_hand(hand):
    """
    Return category for the hand and its rank within that category.

    Rank is a tuple of the meaningful card ranks.
    """
    cards = sorted(hand.cards, key=attrgetter('rank'), reverse=True)
    grouped_cards = group_by_rank_count(cards)
    ranks = get_ranks(iflatten(grouped_cards))

    if len(grouped_cards) == 5:
        is_five_high_straight = ranks == [12, 3, 2, 1, 0]
        if is_five_high_straight:
            ranks = [3, 2, 1, 0, -1]
            if are_all_same_suits(cards):
                return STRAIGHT_FLUSH, ranks
            else:
                return STRAIGHT, ranks
        elif are_sequential(cards):
            if are_all_same_suits(cards):
                if cards[0].is_ace():
                    return ROYAL_FLUSH, ranks
                else:
                    return STRAIGHT_FLUSH, ranks
            else:
                return STRAIGHT, ranks
        elif are_all_same_suits(cards):
            return FLUSH, ranks
        else:
            return HIGH_CARD, ranks
    elif len(grouped_cards) == 4:
        return ONE_PAIR, ranks
    elif len(grouped_cards) == 3:
        largest_group = grouped_cards[0]
        if len(largest_group) == 3:
            return THREE_OF_A_KIND, ranks
        else:
            return TWO_PAIR, ranks
    elif len(grouped_cards) == 2:
        largest_group = grouped_cards[0]
        if len(largest_group) == 4:
            return FOUR_OF_A_KIND, ranks
        else:
            return FULL_HOUSE, ranks
    else:
        raise RuntimeError("This really shouldn't be reachable.")


# card utils

def group_by_rank_count(sorted_cards):
    grouped = group_into_list(sorted_cards, attrgetter('rank'))
    return list(sorted(grouped, key=len, reverse=True))


def are_sequential(sorted_cards):
    return is_strict_sequence(reversed(get_ranks(sorted_cards)))


def are_all_same_suits(cards):
    return are_all_equal(get_suits(cards))


def get_ranks(cards):
    return map(attrgetter('rank'), cards)


def get_suits(cards):
    return map(attrgetter('suit'), cards)


# cards

CARD_SUITS = ('C', 'D', 'H', 'S')
CARD_VALUES = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')


class Card(object):
    def __init__(self, string):
        try:
            self.string = string.upper()
            self.value, self.suit = self.string
            self.rank = CARD_VALUES.index(self.value)
        except ValueError:
            raise InvalidCard("invalid card: '%s'" % string)

        if self.suit not in CARD_SUITS:
            raise InvalidCard("invalid card: '%s'" % string)

    def __repr__(self):
        return 'Card("%s")' % self.string

    def __hash__(self):
        return hash(self.string)

    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.string == other.string

    def is_ace(self):
        return self.value == 'A'


class InvalidCard(Exception):
    pass


# generic utils

iflatten = chain.from_iterable


def group_into_list(iterable, key):
    groups = []
    for k, g in groupby(iterable, key):
        groups.append(list(g))
    return groups


def is_strict_sequence(iterable_of_integers):
    iterator = iter(iterable_of_integers)
    try:
        first, second = next(iterator), next(iterator)
        while second - first == 1:
            first, second = second, next(iterator)
        return False
    except StopIteration:
        return True


def are_all_equal(iterable):
    iterator = iter(iterable)
    try:
        first = next(iterator)
        return all(first == other for other in iterator)
    except StopIteration:
        return True


def find_duplicate(iterable):
    seen = set()
    for item in iterable:
        if item in seen:
            return item
        else:
            seen.add(item)
