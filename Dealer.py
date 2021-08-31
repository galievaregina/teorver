import random

from pai_gow.Pack import Pack

from pai_gow.Cards import Card, Cards


class Dealer:
    pack = []

    def __init__(self):
        self.pack = make_pack()


def make_pack():
    pack = []
    for value in Cards.CardsValue:
        if value == Cards.CardsValue.JOKER:
            pack.append(Card(Cards.CardsValue.JOKER, Cards.CardsSuits.JOKER))
        else:
            pack.append(Card(value, Cards.CardsSuits.HEARTS))
            pack.append(Card(value, Cards.CardsSuits.DIAMONDS))
            pack.append(Card(value, Cards.CardsSuits.CLUBS))
            pack.append(Card(value, Cards.CardsSuits.SPADES))

    return pack


staticmethod


def get_five_cards(pack):
    list_comb_five = []
    for i in range(0, 5):
        card_index = random.randint(0, len(pack) - 1)
        list_comb_five.append(pack[card_index])
        pack.pop(card_index)
    return list_comb_five


def get_two_cards(pack):
    list_comb_two = []
    for i in range(0, 2):
        card_index = random.randint(0, 53)
        list_comb_two.append(pack[card_index])
        pack.pop(card_index)
    return list_comb_two
