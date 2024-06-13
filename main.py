import random

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

    print(hand_1)
    print('-------')
    print(table)
    print('-------')
    print(hand_2)

def showCards(deck: list, hand: list):
    print('deck : ', deck)
    print('hand : ', hand)

def game(deck):
    hand_1 = []
    hand_2 = []
    table = []
    shuffledDeck = shuffleDeck(deck)
    pickRandomCard(shuffledDeck, hand_1, table)
    dealCards(shuffledDeck, hand_1, hand_2, table)

if __name__ == '__main__':
    deck = [
        '1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c',
        '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d',
        '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h',
        '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s',
        ]
    game(deck)