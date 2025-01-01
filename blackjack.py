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
        if len(self.deck) == 0.25 * self.num_decks * len(suits) * len(ranks):
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

    def can_double(self):
        return len(self.cards) == 2

    def double_bet(self):
        self.bet_amount *= 2

    def is_blackjack(self):
        return self.value == 21 and len(self.cards) == 2

# Define your strategy functions (simplest_strategy, random_strategy, etc.) here

# Function to simulate a hand of blackjack
def play_blackjack(strategy_function, initial_bet, deck):
    player_hand = Hand(initial_bet)
    dealer_hand = Hand(0)  # Dealer doesn't have a bet amount

    # Initial dealing
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Check for blackjack
    if dealer_hand.is_blackjack():
        if player_hand.is_blackjack():
            return 0  # No profit or loss
        else:
            return -1 * initial_bet  # Player loses the bet

    if player_hand.is_blackjack():
        return initial_bet * 1.5 # Player wins 1.5 times the bet

    hands = [player_hand]  # Initialize with the player's original hand
    total_profit_loss = 0  # Track total profit or loss

    # Process each hand (to handle splitting)
    hand_index = 0
    while hand_index < len(hands):
        hand = hands[hand_index]
        while True:
            action = strategy_function(hand, dealer_hand.cards[0])

            if action == 'hit':
                hand.add_card(deck.deal())
                if hand.value > 21:
                    break  # Bust, stop the loop for this hand

            elif action == 'stand':
                break

            elif action == 'double' and hand.can_double():
                hand.double_bet()
                hand.add_card(deck.deal())
                break  # After doubling, no further actions

            elif action == 'split':
                if hand.can_split():
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
                    break  # Move on to the next hand
            else:
                break

        hand_index += 1  # Move to the next hand

    # Dealer's turn
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())

    # Determine the outcome for each hand
    for hand in hands:
        if hand.value > 21:
            total_profit_loss -= hand.bet_amount  # Player busts, loses the bet
        elif dealer_hand.value > 21 or hand.value > dealer_hand.value:
            total_profit_loss += hand.bet_amount  # Player wins
        elif hand.value < dealer_hand.value:
            total_profit_loss -= hand.bet_amount  # Dealer wins
        # No change if it's a tie

    return total_profit_loss

def calculate_mean(data):
    return sum(data)/len(data)

# play many hands
def simulate_hands(num_of_hands, strategy, bet, num_of_decks):
    results = []
    total_profit_loss = 0
    deck = Deck(num_of_decks)
    for i in range(num_of_hands):
        hand_result = play_blackjack(strategy, bet, deck)
        results.append(hand_result)
        total_profit_loss += hand_result
    #print(total_profit_loss)
    #print(f'house edge calculated at {(total_profit_loss/(bet*num_of_hands))*100}')
    return results, total_profit_loss

# plot histogram of distribution of blackjack session profits and print mean of data
def plot_hand_data(amount_of_data, num_of_hands, strategy, bet, num_of_decks):
    profits = []
    for i in range(amount_of_data):
        simulation = simulate_hands(num_of_hands, strategy, bet, num_of_decks)
        hand_profit_loss = simulation[1]
        profits.append(hand_profit_loss)
    data = profits
    plt.hist(data, bins=10, edgecolor='black')
    plt.title(f'Histogram for {strategy.__name__}')
    plt.xlabel(f'profit from {num_of_hands} hands')
    plt.ylabel('Frequency')
    plt.show()