import streamlit as st
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
    st.title("Triple Double Bonus Poker")

    bet = st.number_input("Place your bet", min_value=1, step=1)
    if st.button("Deal"):
        st.write("Dealing cards...")
        hand = draw_cards(5)

        st.subheader("Your Hand:")

        selected_cards = st.multiselect(
            "Select the cards to hold",
            [f"{card[0]} of {card[1]}" for card in hand],
            []
        )

        selected_indices = [i for i, card in enumerate(hand) if f"{card[0]} of {card[1]}" in selected_cards]

        for i, card in enumerate(hand):
            if i in selected_indices:
                st.write("[Selected]", card[0], "of", card[1])
            else:
                st.write(card[0], "of", card[1])

        if len(selected_indices) > 0:
            for i in range(5):
                if i not in selected_indices:
                    hand[i] = draw_cards(1)[0]  # Draw a new card for unheld cards

        hand_values = [get_card_value(card) for card in hand]
        score = get_hand_score(hand)

        st.subheader("Final Hand:")
        for i in range(5):
            st.write(hand[i][0], "of", hand[i][1], "(Value:", hand_values[i], ")")

        if score > 0:
            winnings = score * bet
            st.success("Congratulations! You won {} chips.".format(winnings))
        else:
            winnings = -bet
            st.error("Sorry, you lost. Better luck next time.")

play_game()
