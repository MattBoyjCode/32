import streamlit as st
import random
from streamlit import caching

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

PAY_TABLE = {
    "Royal Flush": {5: 800, 4: 250},
    "Four Aces with a 2, 3 or 4 Kicker": 800,
    "Four Twos, Threes or Fours with an Ace, Two, Three or Four Kicker": 400,
    "Four Aces with a Five-King Kicker": 160,
    "Straight Flush": 50,
    "Four of a Kind 2’s, 3’s and 4’s with a Five-King Kicker": 80,
    "Four of a Kind 5’s through Kings": 50,
    "Full House": 9,
    "Flush": 7,
    "Straight": 4,
    "Three of a Kind": 2,
    "Two Pair": 1,
    "Pair of Jacks or Higher": 1,
}

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
    suits = [card[1] for card in hand]
    ranks.sort()

    # Check for Royal Flush
    if all(suit == suits[0] for suit in suits) and ranks == ["10", "Jack", "Queen", "King", "Ace"]:
        return "Royal Flush"

    # Check for Four Aces with a 2, 3, or 4 Kicker
    if ranks.count("Ace") == 4 and any(rank in ranks for rank in ["2", "3", "4"]):
        return "Four Aces with a 2, 3 or 4 Kicker"

    # Check for Four Twos, Threes, or Fours with an Ace, Two, Three, or Four Kicker
    if ranks.count("2") == 4 and any(rank in ranks for rank in ["Ace", "2", "3", "4"]):
        return "Four Twos, Threes or Fours with an Ace, Two, Three or Four Kicker"

    # Check for Four Aces with a Five-King Kicker
    if ranks.count("Ace") == 4 and all(rank in ranks for rank in ["5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]):
        return "Four Aces with a Five-King Kicker"

    # Check for Straight Flush
    if all(suit == suits[0] for suit in suits) and ranks == RANKS[RANKS.index(ranks[0]):RANKS.index(ranks[0])+5]:
        return "Straight Flush"

    # Check for Four of a Kind 2’s, 3’s, and 4’s with a Five-King Kicker
    if ranks.count("2") == 4 or ranks.count("3") == 4 or ranks.count("4") == 4:
        if all(rank in ranks for rank in ["5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]):
            return "Four of a Kind 2’s, 3’s and 4’s with a Five-King Kicker"

    # Check for Four of a Kind 5’s through Kings
    if any(ranks.count(rank) == 4 for rank in ["5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]):
        return "Four of a Kind 5’s through Kings"

    # Check for Full House
    if ranks.count(ranks[0]) == 2 and ranks.count(ranks[-1]) == 3:
        return "Full House"
    if ranks.count(ranks[0]) == 3 and ranks.count(ranks[-1]) == 2:
        return "Full House"

    # Check for Flush
    if all(suit == suits[0] for suit in suits):
        return "Flush"

    # Check for Straight
    if ranks == RANKS[RANKS.index(ranks[0]):RANKS.index(ranks[0])+5]:
        return "Straight"

    # Check for Three of a Kind
    if ranks.count(ranks[0]) == 3 or ranks.count(ranks[2]) == 3 or ranks.count(ranks[-1]) == 3:
        return "Three of a Kind"

    # Check for Two Pair
    if ranks.count(ranks[0]) == 2 and ranks.count(ranks[-1]) == 2:
        return "Two Pair"

    # Check for Pair of Jacks or Higher
    if ranks.count("Jack") == 2 or ranks.count("Queen") == 2 or ranks.count("King") == 2 or ranks.count("Ace") == 2:
        return "Pair of Jacks or Higher"

    # No scoring hand
    return "No Win"

def play_game():
    """Plays a single round of Triple Double Bonus Poker."""
    st.title("Triple Double Bonus Poker")

    # Create session state
    if "hand" not in st.session_state:
        st.session_state.hand = draw_cards(5)
        st.session_state.selected_indices = []

    bet = st.number_input("Place your bet", min_value=1, step=1)

    if st.button("Deal"):
        st.session_state.selected_indices = []
        st.session_state.hand = draw_cards(5)

    st.subheader("Your Hand:")
    for i, card in enumerate(st.session_state.hand):
        if i in st.session_state.selected_indices:
            st.write("[Selected]", card[0], "of", card[1])
        else:
            st.write(card[0], "of", card[1])

    selected_cards = st.multiselect(
        "Select the cards to hold",
        [f"{card[0]} of {card[1]}" for card in st.session_state.hand],
        []
    )

    st.session_state.selected_indices = [i for i, card in enumerate(st.session_state.hand) if
                                          f"{card[0]} of {card[1]}" in selected_cards]

    for i in range(5):
        if i not in st.session_state.selected_indices:
            st.session_state.hand[i] = draw_cards(1)[0]

    hand_values = [get_card_value(card) for card in st.session_state.hand]
    score = get_hand_score(st.session_state.hand)

    st.subheader("Final Hand:")
    for i in range(5):
        st.write(st.session_state.hand[i][0], "of", st.session_state.hand[i][1], "(Value:", hand_values[i], ")")

    if score != "No Win":
        if isinstance(PAY_TABLE[score], dict):
            payout = PAY_TABLE[score].get(len(st.session_state.selected_indices), 0)
        else:
            payout = PAY_TABLE[score]

        winnings = payout * bet
        st.success("Congratulations! You won {} chips.".format(winnings))
    else:
        winnings = -bet
        st.error("Sorry, you lost. Better luck next time.")

    # Disable Streamlit caching
    caching.clear_cache()

play_game()
