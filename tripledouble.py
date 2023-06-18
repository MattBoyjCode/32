import random

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

def draw_cards(num_cards):
    """Draws the specified number of cards from a standard 52-card deck."""
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    return random.sample(deck, num_cards)

def get_card_value(card):
    """Returns the value of a card."""
    rank = card[0]
    if rank in ("Jack", "Queen", "King"):
        return 10
    elif rank == "Ace":
        return 1
    return int(rank)

def get_hand_score(hand):
    """Calculates the score of a given hand."""
    ranks = [card[0] for card in hand]
    ranks.sort()

    # Check for four-of-a-kind
    if ranks.count(ranks[2]) == 4:
        return get_card_value(hand[2]) * 100

    # Check for full house
    if ranks.count(ranks[1]) in (2, 3):
        if ranks.count(ranks[3]) == 3:
            return get_card_value(hand[2]) * 10 + get_card_value(hand[4])
        elif ranks.count(ranks[3]) == 2:
            return get_card_value(hand[2]) * 10 + get_card_value(hand[0])

    # Check for three-of-a-kind
    if ranks.count(ranks[2]) == 3:
        return get_card_value(hand[2]) * 10

    # Check for two pair
    if ranks.count(ranks[1]) == 2 and ranks.count(ranks[3]) == 2:
        return get_card_value(hand[3]) * 10 + get_card_value(hand[1])

    # Check for pair
    for i in range(4):
        if ranks[i] == ranks[i + 1]:
            return get_card_value(hand[i])

    # Check for flush
    suits = set([card[1] for card in hand])
    if len(suits) == 1:
        return 50

    # No scoring hand
    return 0

def play_game():
    """Plays a single round of Triple Double Bonus Poker."""
    print("Welcome to Triple Double Bonus Poker!\n")

    while True:
        # Prompt the player to place a bet
        bet = input("Place your bet (or 'q' to quit): ")
        if bet.lower() == "q":
            break

        try:
            bet = int(bet)
            if bet <= 0:
                print("Please enter a positive bet.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # Draw the cards
        hand = draw_cards(5)
        print("Your initial hand:")
        for card in hand:
            print(card[0], "of", card[1])
        print()

        # Prompt the player to hold cards
        hold = input("Select the cards to hold (e.g., 134, 25). Leave blank to keep all cards: ")
        if hold:
            try:
                hold = [int(card) for card in hold if card.isdigit()]
                for card in hold:
                    if card < 1 or card > 5:
                        raise ValueError
            except ValueError:
                print("Invalid input. Please enter valid card numbers.")
                continue
            for i in range(5):
                if i + 1 not in hold:
                    hand[i] = draw_cards(1)[0]  # Draw a new card for unheld cards

        # Calculate the score
        hand_values = [get_card_value(card) for card in hand]
        score = get_hand_score(hand)

        # Display the final hand and score
        print("Your final hand:")
        for i in range(5):
            print(hand[i][0], "of", hand[i][1], "(Value:", hand_values[i], ")")
        if score > 0:
            winnings = score * bet
            print("Congratulations! You won {} chips.".format(winnings))
        else:
            winnings = -bet
            print("Sorry, you lost. Better luck next time.")
        print()

play_game()
