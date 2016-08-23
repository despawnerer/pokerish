from unittest import TestCase
from itertools import repeat

from pokerish import (
    Card,
    Hand,
    HIGH_CARD,
    ONE_PAIR,
    TWO_PAIR,
    THREE_OF_A_KIND,
    STRAIGHT,
    FLUSH,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    STRAIGHT_FLUSH,
    ROYAL_FLUSH,
    InvalidCard,
    InvalidHand,
    is_counting_down,
    are_all_equal,
)


# hand

class HandFromStringTestCase(TestCase):
    def test_valid(self):
        hand = Hand.from_string('4D 3D 5D 7H AD')
        self.assertEqual(hand, Hand((
            Card('4D'),
            Card('3D'),
            Card('5D'),
            Card('7H'),
            Card('AD'),
        )))

    def test_too_many_cards(self):
        with self.assertRaises(InvalidHand):
            Hand.from_string('4D 3D 3D 7H AD 7D')

    def test_too_few_cards(self):
        with self.assertRaises(InvalidHand):
            Hand.from_string('4D 3D 3D 7H')

    def test_duplicate_cards(self):
        with self.assertRaises(InvalidHand):
            Hand.from_string('AD AH AS AC AD')

    def test_only_two_duplicates(self):
        with self.assertRaises(InvalidHand):
            Hand.from_string('4D 3D 3D 7H AD')


class HandCategoryTestCase(TestCase):
    def test_high_card(self):
        hand = Hand.from_string('TS 2S JH KS AS')
        self.assertEqual(hand.category, HIGH_CARD)

    def test_one_pair(self):
        hand = Hand.from_string('TS JS JH KS AS')
        self.assertEqual(hand.category, ONE_PAIR)

    def test_two_pair(self):
        hand = Hand.from_string('TS JS JH TH AS')
        self.assertEqual(hand.category, TWO_PAIR)

    def test_three_of_a_kind(self):
        hand = Hand.from_string('4D 4H 4S 7H 8D')
        self.assertEqual(hand.category, THREE_OF_A_KIND)

    def test_straight(self):
        hand = Hand.from_string('TS JH QS KS AS')
        self.assertEqual(hand.category, STRAIGHT)

    def test_five_high_straight(self):
        hand = Hand.from_string('5H 4S 3S 2D AS')
        self.assertEqual(hand.category, STRAIGHT)

    def test_flush(self):
        hand = Hand.from_string('5S JS QS KS AS')
        self.assertEqual(hand.category, FLUSH)

    def test_full_house(self):
        hand = Hand.from_string('4D 4H 4S KS KD')
        self.assertEqual(hand.category, FULL_HOUSE)

    def test_four_of_a_kind(self):
        hand = Hand.from_string('4D 4H 4S 4C 8D')
        self.assertEqual(hand.category, FOUR_OF_A_KIND)

    def test_straight_flush(self):
        hand = Hand.from_string('2S 3S 4S 5S 6S')
        self.assertEqual(hand.category, STRAIGHT_FLUSH)

    def test_five_high_straight_flush(self):
        hand = Hand.from_string('5S 4S 3S 2S AS')
        self.assertEqual(hand.category, STRAIGHT_FLUSH)

    def test_royal_flush(self):
        hand = Hand.from_string('TS JS QS KS AS')
        self.assertEqual(hand.category, ROYAL_FLUSH)


class ComparisonTestCase(TestCase):
    def test_category_order(self):
        hands_from_lowest_to_highest = [
            Hand.from_string('TS 2S JH KS AS'),  # high card
            Hand.from_string('TS JS JH KS AS'),  # one pair
            Hand.from_string('TS JS JH TH AS'),  # two pair
            Hand.from_string('4D 4H 4S 7H 8D'),  # three of a kind
            Hand.from_string('5H 4S 3S 2D AS'),  # straight
            Hand.from_string('5S JS QS KS AS'),  # flush
            Hand.from_string('4D 4H 4S KS KD'),  # full house
            Hand.from_string('4D 4H 4S 4C 8D'),  # four of a kind
            Hand.from_string('2S 3S 4S 5S 6S'),  # straight flush
            Hand.from_string('TS JS QS KS AS'),  # royal flush
        ]
        resorted_hands = sorted(hands_from_lowest_to_highest)
        self.assertEqual(hands_from_lowest_to_highest, resorted_hands)

    def test_straight_flushes(self):
        five_high_straight_flush = Hand.from_string('5S 4S 3S 2S AS')
        straight_flush = Hand.from_string('2S 3S 4S 5S 6S')
        royal_flush = Hand.from_string('TS JS QS KS AS')
        self.assertGreater(royal_flush, straight_flush)
        self.assertGreater(straight_flush, five_high_straight_flush)
        self.assertGreater(royal_flush, five_high_straight_flush)

    def test_four_of_a_kind(self):
        fives_with_ace = Hand.from_string('5D 5H 5S 5C AS')
        fives_with_two = Hand.from_string('5D 5H 5S 5C 2S')
        fours = Hand.from_string('4D 4H 4S 4C AS')
        self.assertGreater(fives_with_ace, fives_with_two)
        self.assertGreater(fives_with_two, fours)
        self.assertGreater(fives_with_ace, fours)

    def test_full_house(self):
        fives_and_fours = Hand.from_string('5D 5H 5S 4S 4D')
        fives_and_threes = Hand.from_string('5D 5H 5S 3S 3D')
        fours_and_aces = Hand.from_string('4D 4H 4S AC AS')
        self.assertGreater(fives_and_fours, fives_and_threes)
        self.assertGreater(fives_and_threes, fours_and_aces)
        self.assertGreater(fives_and_fours, fours_and_aces)


# card

class CardTestCase(TestCase):
    def test_valid(self):
        card = Card('4D')
        self.assertEqual(card.suit, 'D')
        self.assertEqual(card.value, '4')

    def test_long_strings(self):
        with self.assertRaises(InvalidCard):
            Card('Asd4')

    def test_short_strings(self):
        with self.assertRaises(InvalidCard):
            Card('a')

    def test_invalid_suit(self):
        with self.assertRaises(InvalidCard):
            Card('2A')

    def test_invalid_value(self):
        with self.assertRaises(InvalidCard):
            Card('PS')


# utils

class IsCountingDownTestCase(TestCase):
    def test_strict_sequence(self):
        self.assertTrue(is_counting_down([5, 4, 3, 2, 1]))

    def test_lazy_strict_sequence(self):
        self.assertTrue(is_counting_down(reversed(xrange(10))))

    def test_repeating_numbers(self):
        self.assertFalse(is_counting_down([4, 3, 2, 2, 1]))

    def test_skipping_numbers(self):
        self.assertFalse(is_counting_down([4, 3, 1]))

    def test_one_number(self):
        self.assertTrue(is_counting_down([1]))

    def test_empty(self):
        self.assertTrue(is_counting_down([]))


class AllEqualTestCase(TestCase):
    def test_equal(self):
        self.assertTrue(are_all_equal([1, 1, 1, 1, 1]))

    def test_unequal(self):
        self.assertFalse(are_all_equal([1, 2, 3]))
