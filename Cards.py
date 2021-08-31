from enum import Enum
from itertools import permutations


class Cards:
    class CardsSuits(Enum):
        CLUBS = 1
        HEARTS = 2
        DIAMONDS = 3
        SPADES = 4
        JOKER = 5

    class CardsValue(Enum):
        TWO = 1
        THREE = 2
        FOUR = 3
        FIVE = 4
        SIX = 5
        SEVEN = 6
        EIGHT = 7
        NINE = 8
        TEN = 9
        JACK = 10
        QUEEN = 11
        KING = 12
        ACE = 13
        JOKER = 14


class Card:
    suit = ''
    value = ''
    value_points = 0

    def __init__(self, value, suit):
        self.value = value.name  # достоинство
        self.suit = suit.name  # масть
        self.value_points = value.value


class Combination(Enum):
    HIGHCARD = 1
    ONEPAIR = 2
    TWOPAIR = 3
    THREEOFAKIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULLHOUSE = 7
    FOUROFAKIND = 8
    STRAIGHTFLUSH = 9
    ROYALFLASH = 10
    FIVEACES = 11


class Combinations:
    is_joker_five = False
    is_joker_two = False
    index_joker_five = -1
    index_joker_two = -1
    list_cards_five = [Card]
    list_cards_two = [Card]
    permutation = []
    card_comb_1 = 0  # ценность карты которая участвует в комбинации(Каре,Тройка,Одна пара)
    card_comb_2 = 0  # ценность карты которая участвует в комбинации(Две пары)
    card_comb_3 = 0  # ценность карты которая участвует в комбинации одна пара (нижняя рука)

    def __init__(self, list_cards_seven: [Card]):
        self.permutation = list(permutations(list_cards_seven))
        for i in range(0, len(self.list_cards_five)):
            if self.list_cards_five[i].value == Cards.CardsValue.JOKER.name:
                self.index_joker_five = i
                self.is_joker_five = True
                break
        for i in range(0, len(self.list_cards_two)):
            if self.list_cards_two[i].value == Cards.CardsValue.JOKER.name:
                self.index_joker_two = i
                self.is_joker_two = True
                break

    def check_high_hand_comb(self):
        hand_comb = []
        if self.check_five_aces():
            hand_comb.append(Combination.FIVEACES)
        if self.check_royal_flash():
            hand_comb.append(Combination.ROYALFLASH)
        elif self.check_straight_flash():
            hand_comb.append(Combination.STRAIGHTFLUSH)
        elif self.check_flash():
            hand_comb.append(Combination.FLUSH)
        if self.check_four_of_a_king():
            hand_comb.append(Combination.FOUROFAKIND)
        if self.check_full_house():
            hand_comb.append(Combination.FULLHOUSE)
        if self.check_straigth():
            hand_comb.append(Combination.STRAIGHT)
        if self.check_three_of_a_kind():
            hand_comb.append(Combination.THREEOFAKIND)
        if self.check_two_pair(self.list_cards_five):
            hand_comb.append(Combination.TWOPAIR)
        if self.check_one_pair(self.list_cards_five):
            hand_comb.append(Combination.ONEPAIR)
        hand_comb.append(Combination.HIGHCARD)
        return hand_comb

    def check_low_hand_comb(self):
        hand_comb = []
        if self.check_one_pair(self.list_cards_two):
            hand_comb.append(Combination.ONEPAIR)
        hand_comb.append(Combination.HIGHCARD)
        return hand_comb

    def check_five_aces(self):
        ch_a = 0
        for el in self.list_cards_five:
            if el.value == Cards.CardsValue.ACE.name:
                ch_a += 1
        if ch_a == 4 and self.is_joker_five:
            return True
        return False

    def check_flash(self):
        check_list = list(self.list_cards_five)
        if self.is_joker_five:
            check_list.pop(self.index_joker_five)
        for i in range(0, len(check_list) - 1):
            for j in range(i + 1, len(check_list)):
                if check_list[i].suit != check_list[j].suit:
                    return False
        return True

    def check_royal_flash(self):
        if not self.check_flash():
            return False
        royal_comb = dict(
            [('ACE', 0), ('KING', 0), ('QUEEN', 0),
             ('JACK', 0), ('TEN', 0)])
        return self.helper_check_flash(royal_comb)

    def check_straight_flash(self):
        if not self.check_flash():
            return False
        street_comb = dict(
            [('SEVEN', 0), ('EIGHT', 0), ('NINE', 0),
             ('JACK', 0), ('TEN', 0)])
        return self.helper_check_flash(street_comb)

    def helper_check_flash(self, comb):
        for x in comb:
            for y in self.list_cards_five:
                if x == y.value:
                    if comb[x] == 1:
                        return False
                    comb[x] += 1
        count_good_cards = sum(comb.values())

        if count_good_cards == 5 or (count_good_cards == 4 and self.is_joker_five):
            return True
        return False

    def change_joker_to_ace(self, copy_list):
        copy_list.pop(self.index_joker_five)
        copy_list.append(Card(Cards.CardsValue.ACE, Cards.CardsSuits.HEARTS))

    def check_anything_of_a_kind(self, kind):
        copy_list = list(self.list_cards_five)
        if self.is_joker_five:
            self.change_joker_to_ace(copy_list)
        for i in range(0, 5 - kind + 1):
            count_good_cards = 1
            for j in range(i + 1, len(copy_list)):
                if copy_list[i].value == copy_list[j].value:
                    count_good_cards += 1
            if count_good_cards == kind:
                self.card_comb_1 = copy_list[i].value_points
                return True
        return False

    def check_four_of_a_king(self):
        return self.check_anything_of_a_kind(4)

    def check_three_of_a_kind(self):
        return self.check_anything_of_a_kind(3)

    def check_full_house(self):
        copy_list = list(self.list_cards_five)
        start = 2
        if self.is_joker_five:
            self.change_joker_to_ace(copy_list)
        first = copy_list[0].value
        second = copy_list[1].value
        check_dict = dict([(first, 1), (second, 1)])
        if first == second:
            check_dict[second] = 2
            first = copy_list[2].value
            check_dict[first] = 1
            start = 3
        for x in check_dict:
            for j in range(start, len(copy_list)):
                if x == copy_list[j].value:
                    check_dict[x] += 1
        if (check_dict[first] == 2 and check_dict[second] == 3) or (
                check_dict[first] == 3 and check_dict[second] == 2):
            return True
        return False

    def check_straigth(self):
        if not self.check_flash():
            return False
        check_dict_1 = dict(
            [('TWO', 0), ('THREE', 0), ('FOUR', 0), ('FIVE', 0), ('SIX', 0)])
        check_dict_2 = dict(
            [('THREE', 0), ('FOUR', 0), ('FIVE', 0), ('SIX', 0), ('SEVEN', 0)])
        check_dict_3 = dict(
            [('FOUR', 0), ('FIVE', 0), ('SIX', 0), ('SEVEN', 0), ('EIGHT', 0)])
        check_dict_4 = dict(
            [('FIVE', 0), ('SIX', 0), ('SEVEN', 0), ('EIGHT', 0), ('NINE', 0)])
        check_dict_5 = dict(
            [('SIX', 0), ('SEVEN', 0), ('EIGHT', 0), ('NINE', 0), ('TEN', 0)])
        list_dict = [check_dict_1, check_dict_2, check_dict_3, check_dict_4, check_dict_5]
        for x in list_dict:
            if self.helper_check_flash(x):
                return True
        return False

    def check_pair(self, list_comb):
        copy_list = list(list_comb)
        if len(list_comb) == 5:
            if self.is_joker_five:
                self.change_joker_to_ace(copy_list)
        elif self.is_joker_two:
            self.change_joker_to_ace(copy_list)
        check_dict = dict([])
        points = []
        for i in copy_list:
            if i.value in check_dict.keys():
                val = check_dict[i.value]
                check_dict[i.value] = val + 1
                points.append(i)
            else:
                check_dict[i.value] = 1
        if len(points) == 2:
            self.card_comb_1 = points[0].value_points
            self.card_comb_2 = points[1].value_points
        elif len(points) == 1:
            if len(list_comb) == 5:
                self.card_comb_1 = points[0].value_points
            elif len(list_comb) == 2:
                self.card_comb_3 = points[0].value_points
        return len(points)

    def check_two_pair(self, list_comb):
        if self.check_pair(list_comb) == 2:
            return True
        return False

    def check_one_pair(self, list_comb):
        if self.check_pair(list_comb) == 1:
            return True
        return False

    def find_max_value(self, cards: [Card]):  # метод для нахождения карты с наибольшим достоинством в HIGHCARD
        max_val = 0
        for x in cards:
            if x.value_points > max_val:
                max_val = x.value_points
        return max_val

    def check_hands(self):
        for i in range(0, len(self.permutation)):
            self.list_cards_five = self.permutation[i][0:5]
            self.list_cards_two = self.permutation[i][5:7]
            if self.check_high_hand_comb()[0].value == self.check_low_hand_comb()[0].value:
                if self.card_comb_1 > self.card_comb_3:
                    break
            if self.check_high_hand_comb()[0].value > self.check_low_hand_comb()[0].value:
                break


# 0 - lose;1-draw;2-win/ score for player


c1 = Card(Cards.CardsValue.QUEEN, Cards.CardsSuits.HEARTS)
c2 = Card(Cards.CardsValue.KING, Cards.CardsSuits.CLUBS)
c3 = Card(Cards.CardsValue.JACK, Cards.CardsSuits.HEARTS)
c4 = Card(Cards.CardsValue.SEVEN, Cards.CardsSuits.HEARTS)
c5 = Card(Cards.CardsValue.EIGHT, Cards.CardsSuits.SPADES)
c6 = Card(Cards.CardsValue.ACE, Cards.CardsSuits.HEARTS)
c7 = Card(Cards.CardsValue.NINE, Cards.CardsSuits.CLUBS)
five = [c1, c2, c3, c4, c5, c6, c7]
c = Combinations(five)
c.check_hands()
r = [c1, c2, c3, c4, c5]
