from operator import attrgetter
from itertools import groupby, chain
from collections import namedtuple


# hands

class Hand(tuple):
    def __init__(self, cards):
        super(Hand, self).__init__(cards)

        if len(self) != 5:
            raise InvalidHand(
                "poker hands must have five cards, got %d" % len(self))

        if are_any_equal(self):
            raise InvalidHand(
                "poker hands can't have two of the same card")

        self.category = decide_category(self)

    @classmethod
    def from_string(cls, string):
        return cls(map(Card, string.split()))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        cards = ', '.join(map(str, self))
        return "<hand [%s], '%s'>" % (cards, self.category.name)


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


def decide_category(hand):
    cards = sorted(hand, key=attrgetter('rank'))
    grouped_cards = group_by_rank_count(cards)

    if len(grouped_cards) == 5:
        if are_sequential(cards):
            if are_all_same_suits(cards):
                if cards[-1].is_ace():
                    return ROYAL_FLUSH
                else:
                    return STRAIGHT_FLUSH
            else:
                return STRAIGHT
        elif are_all_same_suits(cards):
            return FLUSH
        else:
            return HIGH_CARD
    elif len(grouped_cards) == 4:
        return ONE_PAIR
    elif len(grouped_cards) == 3:
        largest_group = grouped_cards[-1]
        if len(largest_group) == 3:
            return THREE_OF_A_KIND
        else:
            return TWO_PAIR
    elif len(grouped_cards) == 2:
        largest_group = grouped_cards[-1]
        if len(largest_group) == 4:
            return FOUR_OF_A_KIND
        else:
            return FULL_HOUSE
    else:
        raise RuntimeError("This really shouldn't be reachable.")


# card utils

def group_by_rank_count(sorted_cards):
    grouped = group_into_list(sorted_cards, attrgetter('rank'))
    return list(sorted(grouped, key=len))


def are_sequential(sorted_cards):
    return is_strict_sequence(get_ranks(sorted_cards))


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
            value, suit = string.upper()
            self.rank = CARD_VALUES.index(value)
        except ValueError:
            raise InvalidCard("invalid card: '%s'" % string)

        if suit not in CARD_SUITS:
            raise InvalidCard("invalid card: '%s'" % string)

        self.value = value
        self.suit = suit

    def __repr__(self):
        return 'Card("%s%s")' % (self.value, self.suit)

    def __str__(self):
        return self.value + self.suit

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

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


def are_any_equal(iterable):
    iterator = iter(iterable)
    try:
        first = next(iterator)
        return any(first == other for other in iterator)
    except StopIteration:
        return True
