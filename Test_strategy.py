import random
import matplotlib.pyplot as plt

# Constants for the game
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Deck Class
class Deck:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.reshuffle()

    def reshuffle(self):
        """Reshuffles the decks and creates a new shoe."""
        self.deck = []
        for i in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    self.deck.append((rank, suit))
        random.shuffle(self.deck)

    def deal(self):
        if len(self.deck) == 0.25 * len(self.deck):
            self.reshuffle()
        return self.deck.pop()

# Hand Class
class Hand:
    def __init__(self, bet_amount):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.bet_amount = bet_amount  # Store the bet amount for the hand
        self.profit_loss = 0  # Track profit or loss for this hand

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card[0]]
        if card[0] == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0][0] == self.cards[1][0]

    def double_bet(self):
        self.bet_amount *= 2

    def is_blackjack(self):
        return self.value == 21 and len(self.cards) == 2

# Function to simulate a hand of blackjack
def play_blackjack(strategy_function, initial_bet, deck):
    split_aces = False
    player_hand = Hand(initial_bet)
    dealer_hand = Hand(0)  # Dealer doesn't have a bet amount

    print(f"Starting a new hand with a bet of {initial_bet}")

    # Initial dealing
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    print(f"Player's hand: {player_hand.cards}, total value: {player_hand.value}")
    print(f"Dealer's visible card: {dealer_hand.cards[0]}")

    # Check for blackjack
    if dealer_hand.is_blackjack():
        if player_hand.is_blackjack():
            print("Both player and dealer have blackjack. Push.")
            return 0  # No profit or loss
        else:
            print("Dealer has blackjack. Player loses.")
            return -1 * initial_bet  # Player loses the bet

    if player_hand.is_blackjack():
        print("Player has blackjack. Player wins 1.5 times the bet.")
        return initial_bet * 1.5  # Player wins 1.5 times the bet

    hands = [player_hand]  # Initialize with the player's original hand
    total_profit_loss = 0  # Track total profit or loss

    # Process each hand (to handle splitting)
    hand_index = 0
    while hand_index < len(hands):
        if split_aces:
            break
        hand = hands[hand_index]
        print(f"Processing hand: {hand.cards}, total value: {hand.value}")

        while True:
            action = strategy_function(hand, dealer_hand.cards[0])
            print(f"Action chosen: {action}")

            if action == 'hit':
                hand.add_card(deck.deal())
                print(f"Player hits. New hand: {hand.cards}, total value: {hand.value}")
                if hand.value > 21:
                    print("Player busts!")
                    break  # Bust, stop the loop for this hand

            elif action == 'stand':
                print("Player stands.")
                break

            elif action == 'double':
                hand.double_bet()
                hand.add_card(deck.deal())
                amount_bet = 2 * initial_bet
                print(f"Player doubles down. New hand: {hand.cards}, total value: {hand.value}, new bet: {amount_bet}")
                if hand.value > 21:
                    print("Player busts after doubling down!")
                    break  # Bust, stop the loop for this hand
                break  # After doubling, no further actions

            elif action == 'split':
                if hand.can_split():
                    if hand.cards[0][0] == 'A' and hand.cards[1][0] == 'A':
                        split_aces = True
                    print("Player splits the hand.")
                    # Remove the original hand and replace with two split hands
                    hands.pop(hand_index)

                    # Create two new hands from the split
                    new_hand1 = Hand(hand.bet_amount)
                    new_hand2 = Hand(hand.bet_amount)

                    # Add one card from the original hand to each new hand
                    new_hand1.add_card(hand.cards[0])
                    new_hand2.add_card(hand.cards[1])

                    # Deal one more card to each hand
                    new_hand1.add_card(deck.deal())
                    new_hand2.add_card(deck.deal())

                    # Insert the new hands into the list of hands
                    hands.insert(hand_index, new_hand1)
                    hands.insert(hand_index + 1, new_hand2)
                    hand_index -= 1

                    print(f"New hands after split: {new_hand1.cards} and {new_hand2.cards}")
                    break  # Move on to the next hand
            else:
                break

        hand_index += 1  # Move to the next hand

    # Dealer's turn
    print(f"Dealer's turn. Dealer's hand: {dealer_hand.cards}, total value: {dealer_hand.value}")
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())
        print(f"Dealer hits. New dealer hand: {dealer_hand.cards}, total value: {dealer_hand.value}")

    # Determine the outcome for each hand
    for hand in hands:
        print(f"Evaluating final player hand: {hand.cards}, total value: {hand.value}")
        if hand.value > 21:
            total_profit_loss -= hand.bet_amount  # Player busts, loses the bet
            print(f"Player busts. Total loss so far: {total_profit_loss}")
        elif dealer_hand.value > 21 or hand.value > dealer_hand.value:
            total_profit_loss += hand.bet_amount  # Player wins
            print(f"Player wins against the dealer. Total profit so far: {total_profit_loss}")
        elif hand.value < dealer_hand.value:
            total_profit_loss -= hand.bet_amount  # Dealer wins
            print(f"Dealer wins against the player. Total loss so far: {total_profit_loss}")
        else:
            print("Push. No change in profit or loss.")

    print(f"End of hand. Total profit/loss: {total_profit_loss}")
    return total_profit_loss


# Example strategy functions
def simplest_strategy(hand, dealer_card):
    if hand.value < 17:
        return 'hit'
    else:
        return 'stand'


def random_strategy(hand, dealer_card):
    choice = random.randint(1, 2)
    if choice == 1:
        return 'hit'
    else:
        return 'stand'


def basic_strategy_no_split(hand, dealer_card):
    dealer_card_value = values[dealer_card[0]]
    # handling soft totals
    is_soft = any(card[0] == 'Ace' for card in hand.cards) and hand.value == sum(values[card[0]] for card in hand.cards)
    if is_soft:
        if hand.value == 20:  # A,9
            return 'stand'
        elif hand.value == 19:  # A,8
            if dealer_card_value == 6:
                return 'double'
            else:
                return 'stand'
        elif hand.value == 18:  # A,7
            if 2 <= dealer_card_value <= 6:
                return 'double'
            elif 9 <= dealer_card_value <= 11:
                return 'hit'
            else:
                return 'stand'
        elif hand.value == 17:  # A,6
            if 3 <= dealer_card_value <= 6:
                return 'double'
            else:
                return 'hit'
        elif 13 <= hand.value <= 16:  # A,2 through A,5
            if 5 <= dealer_card_value <= 6:
                return 'double'
            else:
                return 'hit'

    # remaining hard totals
    if hand.value >= 17:
        return 'stand'
    elif 13 <= hand.value <= 16:
        if dealer_card_value < 7:
            return 'stand'
        else:
            return 'hit'
    elif hand.value == 12:
        if 4 <= dealer_card_value <= 6:
            return 'stand'
        else:
            return 'hit'
    elif hand.value == 11:
        return 'double'
    elif hand.value == 10:
        if dealer_card_value <= 9:
            return 'double'
        else:
            return 'hit'
    elif hand.value == 9:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    else:
        return 'hit'


def basic_strategy_no_aces(hand, dealer_card):
    dealer_card_value = values[dealer_card[0]]
    # handling split situations first
    if hand.can_split():
        if hand.cards[0][0] == 'Ace':
            return 'split'
        elif hand.cards[0][0] == 'Nine':
            if 2 <= dealer_card_value <= 9 and dealer_card_value != 7:
                return 'split'
            else:
                return 'stand'
        elif hand.cards[0][0] == 'Eight':
            return 'split'
        elif hand.cards[0][0] == 'Seven':
            if 2 <= dealer_card_value <= 7:
                return 'split'
            else:
                return 'hit'
        elif hand.cards[0][0] == 'Six':
            if 2 <= dealer_card_value <= 6:
                return 'split'
            else:
                return 'hit'
        elif hand.cards[0][0] == 'Five':
            if 2 <= dealer_card_value <= 9:
                return 'double'
            else:
                return 'hit'
        elif hand.cards[0][0] == 'Four':
            if 5 <= dealer_card_value <= 6:
                return 'split'
            else:
                return 'hit'
        elif hand.cards[0][0] == 'Three' or hand.cards[0][0] == 'Two':
            if 2 <= dealer_card_value <= 7:
                return 'split'
            else:
                return 'hit'
    # rest of cases
    if hand.value >= 17:
        return 'stand'
    elif 13 <= hand.value <= 16:
        if dealer_card_value < 7:
            return 'stand'
        else:
            return 'hit'
    elif hand.value == 12:
        if 4 <= dealer_card_value <= 6:
            return 'stand'
        else:
            return 'hit'
    elif hand.value == 11:
        return 'double'
    elif hand.value == 10:
        if dealer_card_value <= 9:
            return 'double'
        else:
            return 'hit'
    elif hand.value == 9:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    else:
        return 'hit'


def basic_strategy_no_splits_or_aces(hand, dealer_card):
    dealer_card_value = values[dealer_card[0]]
    if hand.value >= 17:
        return 'stand'
    elif 13 <= hand.value <= 16:
        if dealer_card_value < 7:
            return 'stand'
        else:
            return 'hit'
    elif hand.value == 12:
        if 4 <= dealer_card_value <= 6:
            return 'stand'
        else:
            return 'hit'
    elif hand.value == 11:
        return 'double'
    elif hand.value == 10:
        if dealer_card_value <= 9:
            return 'double'
        else:
            return 'hit'
    elif hand.value == 9:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    else:
        return 'hit'


def basic_strategy(hand, dealer_card):
    dealer_card_value = values[dealer_card[0]]

    # handling split situations first
    if hand.can_split():
        if hand.cards[0][0] == 'Ace':
            return 'split'
        elif hand.cards[0][0] == 'Nine':
            if 2 <= dealer_card_value <= 9 and dealer_card_value != 7:
                return 'split'
            else:
                return 'stand'
        elif hand.cards[0][0] == 'Eight':
            return 'split'
        elif hand.cards[0][0] == 'Seven':
            if 2 <= dealer_card_value <= 7:
                return 'split'
            else:
                return 'hit'
        elif hand.cards[0][0] == 'Six':
            if 2 <= dealer_card_value <= 6:
                return 'split'
            else:
                return 'hit'
        elif hand.cards[0][0] == 'Five':
            if 2 <= dealer_card_value <= 9:
                return 'double'
            else:
                return 'hit'
        elif hand.cards[0][0] == 'Four':
            if 5 <= dealer_card_value <= 6:
                return 'split'
            else:
                return 'hit'
        elif hand.cards[0][0] == 'Three' or hand.cards[0][0] == 'Two':
            if 2 <= dealer_card_value <= 7:
                return 'split'
            else:
                return 'hit'

    # handling soft totals
    is_soft = any(card[0] == 'Ace' for card in hand.cards) and hand.value == sum(values[card[0]] for card in hand.cards)
    if is_soft:
        if hand.value == 20:  # A,9
            return 'stand'
        elif hand.value == 19:  # A,8
            if dealer_card_value == 6:
                return 'double'
            else:
                return 'stand'
        elif hand.value == 18:  # A,7
            if 2 <= dealer_card_value <= 6:
                return 'double'
            elif 9 <= dealer_card_value <= 11:
                return 'hit'
            else:
                return 'stand'
        elif hand.value == 17:  # A,6
            if 3 <= dealer_card_value <= 6:
                return 'double'
            else:
                return 'hit'
        elif 15 <= hand.value <= 16:  # A,4 and A,5
            if 4 <= dealer_card_value <= 6:
                return 'double'
            else:
                return 'hit'
        elif 13 <= hand.value <= 14:  # A,2 and A,3
            if 5 <= dealer_card_value <= 6:
                return 'double'
            else:
                return 'hit'

    # remaining hard totals
    if hand.value >= 17:
        return 'stand'
    elif 13 <= hand.value <= 16:
        if dealer_card_value < 7:
            return 'stand'
        else:
            return 'hit'
    elif hand.value == 12:
        if 4 <= dealer_card_value <= 6:
            return 'stand'
        else:
            return 'hit'
    elif hand.value == 11:
        return 'double'
    elif hand.value == 10:
        if dealer_card_value <= 9:
            return 'double'
        else:
            return 'hit'
    elif hand.value == 9:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    else:
        return 'hit'


# Test the game with the basic strategy
def test_strategy(strategy):
    deck = Deck(1)
    print(play_blackjack(strategy, 100, deck))
    return





