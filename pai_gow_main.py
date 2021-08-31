import math
import random
import numpy as np
import scipy.stats
from Cards import Cards, Card, Combinations, Combination


def make_pack():  # создаем колоду из 53 карт
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


def get_seven_cards(pack):  # раздаем карты
    list_comb_five = []
    for i in range(0, 7):
        card_index = random.randint(0, len(pack) - 1)
        list_comb_five.append(pack[card_index])
        pack.pop(card_index)  # удаляем карту которую использовали
    return list_comb_five


def compare_comb(comb1: Combinations,
                 comb2: Combinations):  # сравниваем комбинации дилера и игрока. Если выиграл игрок в одной руке
    # прибавляем 2. Иначе ничего не меняем.
    player_res = 0
    best_high_player = comb1.check_high_hand_comb()[0].value  # player
    best_high_dealer = comb2.check_high_hand_comb()[0].value  # dealer
    if best_high_player == best_high_dealer:
        if best_high_player == Combination.HIGHCARD.value:
            if comb1.find_max_value(comb1.list_cards_five) > comb2.find_max_value(comb2.list_cards_five):
                player_res += 2
        elif comb1.card_comb_1 > comb2.card_comb_1:
            player_res += 2
    elif best_high_player > best_high_dealer:
        player_res += 2
    best_low_player = comb1.check_low_hand_comb()[0].value
    best_low_dealer = comb2.check_low_hand_comb()[0].value
    if best_low_player == best_low_dealer:
        if best_low_player == Combination.HIGHCARD.value:
            if comb1.find_max_value(comb1.list_cards_two) > comb2.find_max_value(comb2.list_cards_two):
                player_res += 2
        elif comb1.card_comb_3 > comb2.card_comb_3:
            player_res += 2
    elif best_low_player > best_low_dealer:
        player_res += 2
    if player_res == 4:
        return 'win'
    if player_res == 2:
        return 'draw'
    elif player_res == 0:
        return 'lose'


if __name__ == '__main__':
    amount_games = 1000
    amount_wins = 0
    amount_losing = 0
    amount_draws = 0
    casino_money = 0
    profit = []
    player_money = 1000
    wager = 100
    commission = 0.05

    for i in range(0, amount_games):
        pack = make_pack()
        player_comb = Combinations(get_seven_cards(pack))
        dealer_comb = Combinations(get_seven_cards(pack))
        player_comb.check_hands()
        dealer_comb.check_hands()
        res = compare_comb(player_comb, dealer_comb)
        if res == 'lose':
            amount_losing += 1
            player_money -= wager
            if player_money < 0:
                casino_money += wager
        elif res == 'draw':
            amount_draws += 1
        elif res == 'win':
            amount_wins += 1
            player_money += wager - wager * commission
            casino_money -= wager - wager + wager * commission
        if player_money > 1000:
            profit.append(player_money - 1000)
    p_win = amount_wins / amount_games
    p_lose = amount_losing / amount_games
    p_draw = amount_draws / amount_games

    print('p_draw = ' + str(p_draw) + '\np_win = ' + str(p_win) + '\np lose = ' + str(p_lose))
    print('Players money after' + str(amount_games) + ' games: ' + str(player_money))
    print('Casino money after' + str(amount_games) + ' games: ' + str(casino_money))
    print("Мат.ожидание выигрыша " + str(np.mean(profit)))
    print("Медиана выигрыша " + str(np.median(profit)))
    print("СКО выигрыша " + str(math.sqrt(np.var(profit))))
    print("Mода выигрыша " + str(scipy.stats.mode(profit)).title())
