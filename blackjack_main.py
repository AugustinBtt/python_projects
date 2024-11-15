import random
import sys
import time


def create_six_deck_shoe():
    single_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    return single_deck * 6


playing_cards = create_six_deck_shoe()
total_cards = len(playing_cards)
player_balance = 5000


def reset_cards():
    global playing_cards
    playing_cards = create_six_deck_shoe()


def win(bet):
    global player_balance
    val = bet * 2
    player_balance += val


def lose(amount):
    global player_balance
    player_balance -= amount


def hit_21(amount):
    global player_balance
    player_balance += amount + (amount * 3 / 2)


def get_score(hands):
    if not isinstance(hands[0], list):
        hands = [hands]
    scores = []
    for hand in hands:
        score = sum(hand)
        ace_adjustments_needed = hand.count(11)
        while ace_adjustments_needed > 0 and score > 21:
            score -= 10
            ace_adjustments_needed -= 1
        scores.append(score)
    return scores


def deal_cards(nb_cards, **participants):
    for player, hand in participants.items():
        dealt_cards = [random.choice(playing_cards) for _ in range(nb_cards)]
        hand.extend(dealt_cards)
        for card in dealt_cards:
            playing_cards.remove(card)


def reshuffle():
    cards_dealt_percentage = round((1 - len(playing_cards) / total_cards) * 100)
    if 50 <= cards_dealt_percentage < 75:
        if random.choice([True, False]):
            print("Cards shuffle in progress...", end='', flush=True)
            for _ in range(5):
                time.sleep(1)
                print('.', end='', flush=True)
            print()
            reset_cards()
    elif 75 <= cards_dealt_percentage <= 95:
        reset_cards()


print(r"""
   ____  _            _        _            _    
  | __ )| | __ _  ___| | __   | | __ _  ___| | __
  |  _ \| |/ _` |/ __| |/ /   | |/ _` |/ __| |/ /
  | |_) | | (_| | (__|   < |__| | (_| | (__|   < 
  |____/|_|\__,_|\___|_|\_\____/ \__,_|\___|_|\_\
""")

print(f"Welcome to the Blackjack game! Here you can split and double, the cards are shuffled (6 decks). \nYou start with {player_balance}$ Have fun!")


class HandsEvaluationsClass:
    def __init__(self):
        self.player_score = None
        self.dealer_score = None
        self.player_hand = None
        self.dealer_hand = None
        self.bet = None
        self.doubled = None
        self.number_of_player_hands = None
        self.player_hand_index = 0


    def update_index(self):
        self.player_hand_index = self.player_hand_index + 1

    def reset_index(self):
        self.player_hand_index = 0

    def check_against_dealer(self):
        doubled_bet = self.bet * 2
        local_score = self.player_score[self.player_hand_index]

        if self.dealer_score[0] > 21:
            print(f"YOU WON, dealer busted, your hand(s): {self.player_hand} | {self.player_score}"
                  f"\nDealer's final hand: {self.dealer_hand} | {self.dealer_score}")
            if self.doubled:
                win(doubled_bet)
                self.doubled = False
            else:
                win(self.bet)
            print(f"Balance ${player_balance}")
            self.update_index()

        elif local_score < self.dealer_score[0] <= 21:
            print(f"YOU LOST! Your hand: {self.player_hand[self.player_hand_index]} | {local_score}"
                  f"\nDealer's final hand: {self.dealer_hand} | {self.dealer_score}")
            if self.doubled:
                lose(self.bet)  # once more since doubled
                self.doubled = False
            print(f"Balance ${player_balance}")
            self.update_index()

        elif self.dealer_score[0] < local_score <= 21:
            print(
                f"YOU WON, your final hand(s): {self.player_hand[self.player_hand_index]} | {self.player_score[self.player_hand_index]}"
                f"\nDealer's final hand: {self.dealer_hand} | {self.dealer_score}")
            if self.doubled:
                win(doubled_bet)
                self.doubled = False
            else:
                win(self.bet)
            print(f"Balance ${player_balance}")
            self.update_index()

        elif self.dealer_score[0] == local_score:
            win(self.bet // 2)
            print(f"PUSH, your final hand(0): {self.player_hand[self.player_hand_index]} | {self.player_score}"
                  f"\nDealer's final hand: {self.dealer_hand} | {self.dealer_score}")
            print(f"Balance ${player_balance}")
            self.update_index()

    def player_stands_checks(self):
        while self.dealer_score[0] < 17:
            deal_cards(1, computer=self.dealer_hand[0])
            self.dealer_score = get_score(self.dealer_hand[0])
        self.check_against_dealer()


def blackjack():
    checks = HandsEvaluationsClass()

    checks.player_hand_index = 0
    checks.doubled = False
    checks.player_hand = [[]]
    checks.dealer_hand = [[]]

    def split(hand):
        hand_1 = hand[0:1]
        hand_2 = hand[1:2]
        hands = [hand_1, hand_2]
        if hand in checks.player_hand:
            checks.player_hand.remove(hand)
        for single_hand in hands:
            deal_cards(1, player=single_hand)
        checks.player_hand.extend(hands)

    def hand_evaluation():
        checks.reset_index()
        while checks.player_hand_index != checks.number_of_player_hands:
            if checks.player_score[checks.player_hand_index] == 21 and len(checks.player_hand[checks.player_hand_index]) == 2:
                checks.update_index()
            elif checks.player_score[checks.player_hand_index] > 21:
                checks.update_index()
            else:
                print(f"Evaluating hand {checks.player_hand[checks.player_hand_index]} | {checks.player_score[checks.player_hand_index]} : ")
                checks.player_stands_checks()

    # GAME START
    while True:
        checks.reset_index()
        user_input = input("----------------- Play a round? PRESS ENTER or N ----------------- : ").lower()
        if user_input == "":
            if player_balance == 0:
                print("Sorry, you are out of funds. Goodbye")
                sys.exit()
            else:
                bet_input = input(f"Balance: ${player_balance} Enter your bet: $")
                try:
                    checks.bet = int(bet_input)
                    if checks.bet == 0:
                        print("Bet cannot be zero. Please enter a valid amount.")
                        blackjack()
                    elif checks.bet > player_balance:
                        print("Your bet cannot be higher than your balance")
                        blackjack()
                    else:
                        lose(checks.bet)
                except ValueError:
                    print("This is not a valid entry")
                    blackjack()

            reshuffle()
            # First cards dealing
            deal_cards(2, player=checks.player_hand[0], computer=checks.dealer_hand[0])
            playing_cards.remove(checks.player_hand[0][-2])
            playing_cards.remove(checks.dealer_hand[0][-2])


            def game_loop():
                checks.player_score = get_score(checks.player_hand)
                checks.dealer_score = get_score(checks.dealer_hand)
                checks.number_of_player_hands = len(checks.player_hand)

                print(f"Your hand(s): {checks.player_hand} | {checks.player_score}"
                      f"\nDealer's first card: {checks.dealer_hand[0][0]}")

                score = checks.player_score[checks.player_hand_index]

                # CHECKING CONDITIONS
                if checks.dealer_score[0] == 21 and len(checks.dealer_hand[0]) == 2:
                    print(f"Dealer hits BLACKJACK. We start a new game.")
                    if score == 21 and len(checks.player_hand[checks.player_hand_index]) == 2:
                        print(f"You have a BLACKJACK too! Push!")
                        win(checks.bet // 2)
                    else:
                        lose(checks.bet)
                    blackjack()

                if len(checks.player_hand[checks.player_hand_index]) == 2 and checks.player_hand[checks.player_hand_index][0] == checks.player_hand[checks.player_hand_index][1]:
                    split_input = input(f"SPLIT {checks.player_hand[checks.player_hand_index]} ? ").lower()
                    if split_input in ['y', 'yes']:
                        lose(checks.bet)
                        split(checks.player_hand[checks.player_hand_index])
                        game_loop()

                if score == 21 and len(checks.player_hand[checks.player_hand_index]) == 2:  # checking for blackjack
                    if checks.player_hand_index == checks.number_of_player_hands - 1:
                        hit_21(checks.bet)
                        print(f"BLACKJACK! Your hand: {checks.player_hand[checks.player_hand_index]} | {checks.player_score[checks.player_hand_index]}"
                              f"\nDealer's hand: {checks.dealer_hand} | {checks.dealer_score}")
                        print(f"Balance ${player_balance}")
                        hand_evaluation()
                        blackjack()
                    else:
                        hit_21(checks.bet)
                        print(f"BLACKJACK!! Dealer's first card: {checks.dealer_hand[0][0]} | NEXT HAND")
                        checks.update_index()
                        game_loop()
                elif score > 21:
                    if checks.player_hand_index == checks.number_of_player_hands - 1:
                        print(f"You BUSTED! Your hand(s): {checks.player_hand[checks.player_hand_index]} | {checks.player_score[checks.player_hand_index]}"
                              f"\nDealer's hand: {checks.dealer_hand} | {checks.dealer_score}")
                        print(f"Balance ${player_balance}")
                        hand_evaluation()
                        blackjack()
                    else:
                        print(f"You BUSTED. Dealer's first card: {checks.dealer_hand[0][0]} | NEXT HAND")
                        checks.update_index()
                        game_loop()
                else:
                    if len(checks.player_hand[checks.player_hand_index]) == 2:
                        if not checks.doubled:
                            double_choice = input(f"DOUBLE? {checks.player_hand[checks.player_hand_index]} Y/N ").lower()
                            if double_choice == "y" or double_choice == "yes":
                                lose(checks.bet)
                                checks.doubled = True
                                deal_cards(1, player=checks.player_hand[checks.player_hand_index])
                                print(f"DOUBLED!")
                                game_loop()
                            else:
                                pass
                        else:
                            pass

                    if not checks.doubled:
                        player_choice = input(f"Do you want another card? Hand: {checks.player_hand[checks.player_hand_index]} | {checks.player_score[checks.player_hand_index]} | Y/N ").lower()
                        if player_choice == "y" or player_choice == "yes":
                            deal_cards(1, player=checks.player_hand[checks.player_hand_index])
                            game_loop()
                        else:
                            if checks.player_hand_index != checks.number_of_player_hands - 1:
                                print("NEXT HAND")
                                checks.update_index()
                                game_loop()
                            else:  # player said no to a new card and there are no more hands to check
                                if checks.number_of_player_hands > 1:
                                    hand_evaluation()
                                else:  # playing with one hand
                                    checks.player_stands_checks()
                                blackjack()
                    else:
                        if checks.player_hand_index != checks.number_of_player_hands - 1:
                            print("NEXT HAND")
                            checks.update_index()
                            game_loop()
                        else:  # if last hand was doubled
                            if checks.number_of_player_hands > 1:
                                hand_evaluation()
                            else:  # playing with one hand
                                checks.player_stands_checks()
                            blackjack()

            game_loop()  # Game starts


        elif user_input in ['n', 'no']:
            print(f"Final balance {player_balance}. Goodbye")
            sys.exit()
        else:
            print("INVALID TEXT. Please press ENTER or 'n'.")


blackjack()
