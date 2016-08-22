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
    FIVE_HIGH_STRAIGHT,
    FLUSH,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    STRAIGHT_FLUSH,
    FIVE_HIGH_STRAIGHT_FLUSH,
    ROYAL_FLUSH,
    InvalidCard,
    InvalidHand,
    is_strict_sequence,
    are_all_equal,
)


# hand

class HandFromStringTestCase(TestCase):
    def test_valid(self):
        hand = Hand.from_string('4D 3D 3D 7H AD')
        self.assertEqual(hand, (
            Card('4D'),
            Card('3D'),
            Card('3D'),
            Card('7H'),
            Card('AD'),
        ))

    def test_too_many_cards(self):
        with self.assertRaises(InvalidHand):
            Hand.from_string('4D 3D 3D 7H AD 7D')

    def test_too_few_cards(self):
        with self.assertRaises(InvalidHand):
            Hand.from_string('4D 3D 3D 7H')

    def test_duplicate_cards(self):
        with self.assertRaises(InvalidHand):
            Hand.from_string('AD AH AS AC AD')


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
        self.assertEqual(hand.category, FIVE_HIGH_STRAIGHT)

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

    def test_royal_flush(self):
        hand = Hand.from_string('TS JS QS KS AS')
        self.assertEqual(hand.category, ROYAL_FLUSH)

    def test_five_high_straight_flush(self):
        hand = Hand.from_string('5S 4S 3S 2S AS')
        self.assertEqual(hand.category, FIVE_HIGH_STRAIGHT_FLUSH)


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

class IsStrictSequenceTestCase(TestCase):
    def test_strict_sequence(self):
        self.assertTrue(is_strict_sequence([1, 2, 3, 4, 5]))

    def test_lazy_strict_sequence(self):
        self.assertTrue(is_strict_sequence(xrange(10)))

    def test_repeating_numbers(self):
        self.assertFalse(is_strict_sequence([1, 2, 2, 3, 4]))

    def test_skipping_numbers(self):
        self.assertFalse(is_strict_sequence([1, 3, 4]))

    def test_one_number(self):
        self.assertTrue(is_strict_sequence([1]))

    def test_empty(self):
        self.assertTrue(is_strict_sequence([]))


class AllEqualTestCase(TestCase):
    def test_equal(self):
        self.assertTrue(are_all_equal([1, 1, 1, 1, 1]))

    def test_unequal(self):
        self.assertFalse(are_all_equal([1, 2, 3]))

    def test_lazy_equal(self):
        self.assertTrue(are_all_equal(repeat(10, 5)))

    def test_lazy_unequal(self):
        self.assertFalse(are_all_equal(xrange(10)))
