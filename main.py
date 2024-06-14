import random
import os
clear = lambda: os.system('clear')

def shuffleDeck(deck: list) -> list:
    random.shuffle(deck)
    return deck

def collectRemoveCard(deck: list, place: list, rand_card: int= -1) -> None:
    if(rand_card != -1):
        place.append(deck[rand_card])
        del deck[rand_card]
    else:
        place.append(deck[0])
        del deck[0]

def pickRandomCard(deck: list, hand: list, table: list) -> None:
    x = random.randint(0,39)
    accept_card: str = input(f'accept the following card, {deck[x]} ?(y/n)')
    if(accept_card == 'y'):
        collectRemoveCard(deck, hand, x)
    else:
        collectRemoveCard(deck, table, x)

def dealCards(deck: list, hand_1: list, hand_2: list, table: list) -> None:
    player_1 = 2
    table_cards = 4
    if not hand_1:
        player_1 = 3
        table_cards = 3
    for _ in range(0,player_1):
        collectRemoveCard(deck, hand_1)
    for _ in range(0,table_cards):
        collectRemoveCard(deck, table)
    for _ in range(0,3):
        collectRemoveCard(deck, hand_2)

def collectEqualValueCard(table: list, card: str) -> dict:
    available = -1
    best_pick = -1
    for i in range(0, len(table)):
        if card[0] == table[i][0]:
            available = i
        if card[0] != 'd' and card[0] == table[i][0] and table[i][1] == 'd':
            best_pick = i
    return {'available' : available, 'best_pick' : best_pick}

def collectSumOfThrownCard(table: list, card: str) -> None:
    char_to_number = {
        'D': 8, 'V': 9, 'R': 10
    }

    def parse_string(s):
        first_char = s[0]
        if first_char.isdigit():
            return int(first_char)
        else:
            return char_to_number.get(first_char)

    nums = [parse_string(s) for s in table]
    card = parse_string(card)

    def find_combinations(nums, target, start, path, result):
        if target == 0:
            result.append(path)
            return
        for i in range(start, len(nums)):
            if nums[i] > target:
                break
            if i > start and nums[i] == nums[i - 1]:
                continue
            find_combinations(nums, target - nums[i], i + 1, path + [table[i]], result)

    nums.sort()
    result = []
    find_combinations(nums, card, 0, [], result)
    return result

def ThrowCollectCards(table: list, card: str, pile: list) -> None:
    result = collectEqualValueCard(table, card)
    available, best_pick = result['available'], result['best_pick']
    if(available == -1 and best_pick == -1):
        print(collectSumOfThrownCard(table, card))
        table.append(card)
        return
    if(best_pick != -1):
        pile.append(table[best_pick])
        del table[best_pick]
        pile.append(card)
        return
    pile.append(table[available])
    del table[available]
    pile.append(card)
    return

def showCards(deck: list, hand: list):
    print('deck : ', deck)
    print('hand : ', hand)

def game(deck):
    hand_1 = []
    hand_2 = []
    pile_1 = []
    pile_2 = []
    table = []
    shuffledDeck = shuffleDeck(deck)
    pickRandomCard(shuffledDeck, hand_1, table)
    dealCards(shuffledDeck, hand_1, hand_2, table)
    # Test case for priority
    table = ['1c', '2d', '1d', '3d']
    hand_1 = ['1s', '3h', '4s']
    while hand_1:
        print(" table : ")
        print(table)
        print('------')
        print("your hand : ")
        print(hand_1)
        card = input("select card from your hand :")
        card_index = int(card) -1
        card = hand_1[card_index]
        del hand_1[card_index]
        ThrowCollectCards(table, card, pile_1)
    print('table :')
    print(table)
    print('pile :')
    print(pile_1)

if __name__ == '__main__':
    deck = [
        '1c', '2c', '3c', '4c', '5c', '6c', '7c', 'Dc', 'Vc', 'Rc',
        '1d', '2d', '3d', '4d', '5d', '6d', '7d', 'Dd', 'Vd', 'Rd',
        '1h', '2h', '3h', '4h', '5h', '6h', '7h', 'Dh', 'Vh', 'Rh',
        '1s', '2s', '3s', '4s', '5s', '6s', '7s', 'Ds', 'Vs', 'Rs',
        ]
    game(deck)