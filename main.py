import random
import os
clear = lambda: os.system('clear')

class IntRef:
    def __init__(self, value):
        self.value = value

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
        if card[0] != '♦' and card[0] == table[i][0] and table[i][1] == '♦':
            best_pick = i
    return {'available' : available, 'best_pick' : best_pick}

char_to_number = {
        'D': 8, 'V': 9, 'R': 10
    }

def parse_string(s):
    first_char = s[0]
    if first_char.isdigit():
        return int(first_char)
    else:
        return char_to_number.get(first_char)

def collectSumOfThrownCard(table: list, card: str) -> None:

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

def ThrowCollectCards(table: list, card: str, pile: list, score: IntRef) -> bool:
    result = collectEqualValueCard(table, card)
    available, best_pick = result['available'], result['best_pick']
    if(available == -1 and best_pick == -1):
        result = collectSumOfThrownCard(table, card)
        if(result):
            print("Please select a combination of cards you want to pick up : ")
            for i in range(len(result)):
                print(f'{i+1} : {result[i]}')
            selected = input('-> ')
            selected_card = result[int(selected)-1]
            pile.append(card)
            for c in selected_card:
                pile.append(c)
                del table[table.index(c)]
            if len(table) == 0:
                score.value += 1
        else:
            table.append(card)
            return False
    if(best_pick != -1):
        pile.append(table[best_pick])
        del table[best_pick]
        if len(table) == 0:
            score.value += 1
        pile.append(card)
    else:
        pile.append(table[available])
        del table[available]
        if len(table) == 0:
            score.value += 1
        pile.append(card)
    return True

def calculateNumberOfCards(pile: list) -> int:
    if(len(pile) > 20):
        return 1
    return 0

def verifySevenOfDiamond(pile: list) -> int:
    if '7♦' in pile:
        return 1
    return 0

def bermila(pile: list) -> int:
    sevens = 0
    sixes = 0
    nums = [parse_string(s) for s in pile]
    for num in nums:
        if num == 7:
            sevens += 1
        if num == 6:
            sixes += 1
    if sevens > 2:
        return 1
    if sevens == 2 and sixes > 2:
        return 1
    return 0

def diamondCount(pile: list) -> int:
    nb_diamonds = 0
    for card in pile:
        if '♦' in card:
            nb_diamonds += 1
    if nb_diamonds == 10:
        return 21
    if nb_diamonds > 5:
        return 1
    return 0

def calcScore(pile: list) -> int:
    return calculateNumberOfCards(pile) + diamondCount(pile) + bermila(pile) + verifySevenOfDiamond(pile)

def showCards(deck: list, hand: list):
    print('deck : ', deck)
    print('hand : ', hand)

def game(deck):
    hand_1 = []
    hand_2 = []
    pile_1 = []
    pile_2 = []
    score_p1 = IntRef(0)
    score_p2 = IntRef(0)
    last_picked_p1 = False
    last_picked_p2 = False
    table = []
    shuffledDeck = shuffleDeck(deck)
    turn = 0
    while(True):
        clear()
        while len(deck):
            if turn == 0:
                pickRandomCard(shuffledDeck, hand_1, table)
                dealCards(shuffledDeck, hand_1, hand_2, table)
            if turn // 2 == 0:
                print("Player 1 turn : ")
                print(hand_1)
                print('-----')
                print(table)
                card = input("select card from your hand :")
                card_index = int(card) -1
                card = hand_1[card_index]
                del hand_1[card_index]
                last_picked_p1 = ThrowCollectCards(table, card, pile_1, score_p1)
                clear()
            if turn // 2 != 1:
                print("Player 2 turn : ")
                print(hand_2)
                print('-----')
                print(table)
                card = input("select card from your hand :")
                card_index = int(card) -1
                card = hand_2[card_index]
                del hand_2[card_index]
                last_picked_p2 = ThrowCollectCards(table, card, pile_2, score_p2)
                clear()
            turn += 1
                
        if(last_picked_p1):
            for card in table:
                pile_1.append(pile_1)
        if(last_picked_p2):
            for card in table:
                pile_2.append(pile_2)
        score_p1.value += calcScore(pile_1)
        score_p2.value += calcScore(pile_2)
        print('player 1 score : ', score_p1.value)
        print('player 2 score : ', score_p2.value)

if __name__ == '__main__':
    deck = [
        '1♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', 'D♥', 'V♥', 'R♥',
        '1♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', 'D♦', 'V♦', 'R♦',
        '1♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', 'D♣', 'V♣', 'R♣',
        '1♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', 'D♠', 'V♠', 'R♠',
        ]
    game(deck)