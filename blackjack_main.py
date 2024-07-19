import random
import sys
import time


def create_six_deck_shoe():
    single_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    return single_deck * 6


playing_cards = create_six_deck_shoe()
total_cards = len(playing_cards)
index = 0
player_balance = 5000


def update_index():
    global index
    index = index + 1


def reset_index():
    global index
    index = 0


def reset_cards():
    global playing_cards
    playing_cards = create_six_deck_shoe()


def win(amount, bet):
    global player_balance
    val = amount + bet
    player_balance += val


def lose(amount):
    global player_balance
    player_balance -= amount


def hit_21(amount):
    global player_balance
    player_balance += amount + (amount * 3 / 2)
    print(f"Balance ${player_balance}")


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
        get_score(hand)


def reshuffle():
    cards_dealt_percentage = round((1 - len(playing_cards) / total_cards) * 100)
    if 50 <= cards_dealt_percentage < 75:
        if random.choice([True, False]):
            print("Shuffle in progress", end='', flush=True)
            for _ in range(5):
                time.sleep(1)
                print('.', end='', flush=True)
            print()
            reset_cards()
    elif 75 <= cards_dealt_percentage <= 95:
        reset_cards()


def blackjack():
    computer_hand = [[]]
    player_hand = [[]]

    def split(hand):
        hand_1 = hand[0:1]
        hand_2 = hand[1:2]
        hands = [hand_1, hand_2]
        print(f"New list of hands {hands}")
        player_hand.clear()
        for single_hand in hands:
            deal_cards(1, player=single_hand)
        player_hand.extend(hands)
        game_loop()

    # GAME START
    while True:
        reset_index()
        user_input = input("Welcome to the BlackJack game, do you want to play a round of BlackJack? Y/N ").lower()
        if user_input in ['y', 'yes']:
            if player_balance == 0:
                print("Sorry, you are out of funds. Goodbye")
                sys.exit()
            else:
                bet_input = input(f"Balance: ${player_balance} Please enter your bet: $")
                try:
                    bet = int(bet_input)
                    if bet > player_balance:
                        print("Your bet cannot be higher than your balance")
                        blackjack()
                    else:
                        lose(bet)
                except ValueError:
                    print("This is not a valid entry")
                    blackjack()

            reshuffle()
            # First cards dealing
            deal_cards(2, player=player_hand[0], computer=computer_hand[0])
            playing_cards.remove(player_hand[0][-2])
            playing_cards.remove(computer_hand[0][-2])

            def game_loop():

                player_score = get_score(player_hand)
                computer_score = get_score(computer_hand)
                length_plyr_hands = len(player_hand)

                print(f"Your hand(s): {player_hand} | {player_score}"
                      f"\n Dealer's first card: {computer_hand[0][0]}")

                def computer_last_chk_win():
                    reset_index()
                    while index != length_plyr_hands:
                        local_score = player_score[index]
                        if local_score > 21 or (local_score == 21 and len(player_hand[index]) == 2):
                            update_index()
                        else:
                            if computer_score[0] > 21:
                                win(bet, bet)
                                print(f"You won, dealer busted, your hand(s): {player_hand} | {player_score}"
                                        f"\nDealer's final hand: {computer_hand} | {computer_score}")
                                print(f"Balance ${player_balance}")
                                update_index()

                            elif local_score < computer_score[0] <= 21:
                                print(f"Dealer won, your hand: {player_hand[index]} | {player_score[index]}"
                                        f"\n Dealer's final hand: {computer_hand} | {computer_score}")
                                print(f"Balance ${player_balance}")
                                update_index()

                            elif computer_score[0] < local_score <= 21:
                                win(bet, bet)
                                print(f"You won, your final hand(s): {player_hand[index]} | {player_score[index]}"
                                        f"\n Dealer's final hand: {computer_hand} | {computer_score}")
                                print(f"Balance ${player_balance}")
                                update_index()

                            elif computer_score[0] == local_score:
                                win(bet, 0)
                                print(f"PUSH, your final hand(0): {player_hand[index]} | {player_score}"
                                        f"\n Dealer's final hand: {computer_hand[index]} | {computer_score}")
                                print(f"Balance ${player_balance}")
                                update_index()
                    blackjack()

                while index != length_plyr_hands:
                    score = player_score[index]

                    if player_hand[0][0] == player_hand[0][1]:
                        split_input = input("Do you want to split?")
                        if split_input in ['y', 'yes']:
                            split(player_hand[index])

                    # CHECKING CONDITIONS
                    if score == 21 and len(player_hand[index]) == 2:
                        hit_21(bet)
                        update_index()
                        if index == length_plyr_hands:
                            print(f"BLACKJACK! Your hand: {player_hand} | {player_score}"
                                  f"\n Dealer's final hand: {computer_hand} | {computer_score}")
                            print(f"Balance ${player_balance}")
                            blackjack()
                        else:
                            print(f"BLACKJACK!! Next hand. Dealer's first hand: {computer_hand[0][0]}")
                            game_loop()

                    elif score > 21:
                        update_index()
                        if index == length_plyr_hands:
                            print(f"You busted! Your hand: {player_hand} | {player_score}"
                                  f"\n Dealer's final hand: {computer_hand} | {computer_score}")
                            print(f"Balance ${player_balance}")
                            blackjack()
                        else:
                            print(f"You BUSTED. Next hand. Dealer's first card: {computer_hand[0][0]}")
                            game_loop()
                    else:
                        player_choice = input(f"Do you want another card? Hand: {player_hand[index]} Y/N ").lower()
                        if player_choice == "y" or player_choice == "yes":
                            if player_choice == "y" or player_choice == "yes":
                                deal_cards(1, player=player_hand[index])
                                game_loop()
                        else:  # NO. Enter this logic once all previous hands are played by the player
                            update_index()
                            if index != length_plyr_hands:
                                print("NEXT HAND")
                                game_loop()
                            else:
                                if computer_score[0] == 16:
                                    deal_cards(1, computer=computer_hand[0])
                                    while computer_score[0] < score and computer_score[0] <= 21:
                                        deal_cards(1, computer=computer_hand[0])
                                    computer_last_chk_win()
                                elif computer_score[0] == 17:
                                    computer_last_chk_win()
                                else:
                                    while computer_score[0] < score and computer_score[0] <= 21:
                                        deal_cards(1, computer=computer_hand[0])
                                        computer_score = get_score(computer_hand[0])
                                    computer_last_chk_win()
            game_loop()

        elif user_input in ['n', 'no']:
            print(f"Final balance {player_balance}. Goodbye")
            sys.exit()
        else:
            print("INVALID TEXT. Please enter 'y', 'yes', or 'n'.")


blackjack()
