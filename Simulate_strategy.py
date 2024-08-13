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
        if len(self.deck) == 0:
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
            return int(initial_bet * -1)  # Player loses the bet

    if player_hand.is_blackjack():
        return int(initial_bet * 1.5)  # Player wins 1.5 times the bet

    hands = [player_hand]  # Initialize with the player's original hand
    total_profit_loss = 0  # Track total profit or loss

    # Process each hand (to handle splitting)
    for hand in hands:
        while True:
            action = strategy_function(hand, dealer_hand.cards[0])

            if action == 'hit':
                hand.add_card(deck.deal())
                if hand.value > 21:
                    return int(initial_bet * -1)

            elif action == 'stand':
                break

            elif action == 'double':
                hand.double_bet()
                hand.add_card(deck.deal())
                if hand.value > 21:
                    return int(hand.bet_amount * -1)
                break

            elif action == 'split':
                if hand.can_split():
                    # Create two new hands from the split
                    new_hand1 = Hand(hand.bet_amount)
                    new_hand2 = Hand(hand.bet_amount)

                    # Add one card from the original hand to each new hand
                    new_hand1.add_card(hand.cards[0])
                    new_hand2.add_card(hand.cards[1])

                    # Deal one more card to each hand
                    new_hand1.add_card(deck.deal())
                    new_hand2.add_card(deck.deal())

                    # Add these new hands to the list of hands to process
                    hands.append(new_hand1)
                    hands.append(new_hand2)

                    break
            else:
                break

    # Dealer's turn
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())

    # Determine the outcome for each hand
    for hand in hands:
        if dealer_hand.value > 21:
            total_profit_loss += hand.bet_amount
        elif dealer_hand.value > hand.value:
            total_profit_loss -= hand.bet_amount
        elif dealer_hand.value < hand.value:
            total_profit_loss += hand.bet_amount

    return total_profit_loss


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
    is_soft = any(card[0] == 'Ace' for card in hand.cards) and hand.value == sum(values[card[0]] for card in hand.cards)
    if is_soft and hand.value == 19:
        if dealer_card_value == 6:
            return 'double'
        else:
            return 'stand'
    if is_soft and hand.value == 18:
        if 2 <= dealer_card_value <= 6:
            return 'double'
        elif 9 <= dealer_card_value <= 11:
            return 'hit'
        else:
            return 'stand'
    if is_soft and hand.value == 17:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    if is_soft and 16 <= hand.value <= 15:
        if 4 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    if is_soft and 14 <= hand.value <= 13:
        if 5 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    # remaining scenarios
    if hand.value < 9:
        return 'hit'
    if hand.value == 9:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    if hand.value == 10:
        if dealer_card_value < 10:
            return 'double'
        else:
            return 'hit'
    if hand.value == 11:
        return 'double'
    if hand.value == 12:
        if 4 <= dealer_card_value <= 6:
            return 'stand'
        else:
            return 'hit'
    if 13 <= hand.value <= 16:
        if dealer_card_value < 7:
            return 'stand'
        else:
            return 'hit'
    if hand.value >= 17:
        return 'stand'


def basic_strategy_no_aces(hand, dealer_card):
    dealer_card_value = values[dealer_card[0]]
    # handling split situations first
    if hand.can_split() and hand.value == 16:
        return 'split'
    if hand.can_split() and hand.cards[0][0] == 'Ace':
        return 'split'
    if hand.can_split() and hand.value == 18:
        if 2 <= dealer_card_value <= 6 or 8 <= dealer_card_value <= 9:
            return 'split'
    if hand.can_split() and hand.value == 14:
        if dealer_card_value <= 7:
            return 'split'
    if hand.can_split() and hand.value == 12:
        if dealer_card_value <= 6:
            return 'split'
    if hand.can_split() and hand.value == 8:
        if dealer_card_value == 5 or dealer_card_value == 6:
            return 'split'
    if hand.can_split() and hand.value == 6:
        if dealer_card_value <= 7:
            return 'split'
    if hand.can_split() and hand.value == 4:
        if dealer_card_value <= 7:
            return 'split'
    if hand.value < 9:
        return 'hit'
    if hand.value == 9:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    if hand.value == 10:
        if dealer_card_value < 10:
            return 'double'
        else:
            return 'hit'
    if hand.value == 11:
        return 'double'
    if hand.value == 12:
        if 4 <= dealer_card_value <= 6:
            return 'stand'
        else:
            return 'hit'
    if 13 <= hand.value <= 16:
        if dealer_card_value < 7:
            return 'stand'
        else:
            return 'hit'
    if hand.value >= 17:
        return 'stand'


def basic_strategy_no_splits_or_aces(hand, dealer_card):
    dealer_card_value = values[dealer_card[0]]
    if hand.value < 9:
        return 'hit'
    if hand.value == 9:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    if hand.value == 10:
        if dealer_card_value < 10:
            return 'double'
        else:
            return 'hit'
    if hand.value == 11:
        return 'double'
    if hand.value == 12:
        if 4 <= dealer_card_value <= 6:
            return 'stand'
        else:
            return 'hit'
    if 13 <= hand.value <= 16:
        if dealer_card_value < 7:
            return 'stand'
        else:
            return 'hit'
    if hand.value >= 17:
        return 'stand'


def basic_strategy(hand, dealer_card):
    dealer_card_value = values[dealer_card[0]]
    # handling split situations first
    if hand.can_split() and hand.value == 16:
        return 'split'
    if hand.can_split() and hand.cards[0][0] == 'Ace':
        return 'split'
    if hand.can_split() and hand.value == 18:
        if 2 <= dealer_card_value <= 6 or 8 <= dealer_card_value <= 9:
            return 'split'
    if hand.can_split() and hand.value == 14:
        if dealer_card_value <= 7:
            return 'split'
    if hand.can_split() and hand.value == 12:
        if dealer_card_value <= 6:
            return 'split'
    if hand.can_split() and hand.value == 8:
        if dealer_card_value == 5 or dealer_card_value == 6:
            return 'split'
    if hand.can_split() and hand.value == 6:
        if dealer_card_value <= 7:
            return 'split'
    if hand.can_split() and hand.value == 4:
        if dealer_card_value <= 7:
            return 'split'
    # now handling soft totals
    # check if there is an ace and that ace is being counted as an 11 currently
    is_soft = any(card[0] == 'Ace' for card in hand.cards) and hand.value == sum(values[card[0]] for card in hand.cards)
    if is_soft and hand.value == 19:
        if dealer_card_value == 6:
            return 'double'
        else:
            return 'stand'
    if is_soft and hand.value == 18:
        if 2 <= dealer_card_value <= 6:
            return 'double'
        elif 9 <= dealer_card_value <= 11:
            return 'hit'
        else:
            return 'stand'
    if is_soft and hand.value == 17:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    if is_soft and 16 <= hand.value <= 15:
        if 4 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    if is_soft and 14 <= hand.value <= 13:
        if 5 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    # remaining scenarios
    if hand.value < 9:
        return 'hit'
    if hand.value == 9:
        if 3 <= dealer_card_value <= 6:
            return 'double'
        else:
            return 'hit'
    if hand.value == 10:
        if dealer_card_value < 10:
            return 'double'
        else:
            return 'hit'
    if hand.value == 11:
        return 'double'
    if hand.value == 12:
        if 4 <= dealer_card_value <= 6:
            return 'stand'
        else:
            return 'hit'
    if 13 <= hand.value <= 16:
        if dealer_card_value < 7:
            return 'stand'
        else:
            return 'hit'
    if hand.value >= 17:
        return 'stand'

def calculate_mean(data):
    return sum(data)/len(data)

# play many hands
def simulate_hands(num_of_hands, strategy, bet, num_of_decks):
    results = []
    total_profit_loss = 0
    deck = Deck(num_of_decks)  # Create the deck once for the whole simulation
    for i in range(num_of_hands):
        hand_result = play_blackjack(strategy, bet, deck)
        results.append(hand_result)
        total_profit_loss += hand_result
    return results, total_profit_loss

# plot histogram of distribution of blackjack session profits and print mean of data
def plot_hand_data(amount_of_data, num_of_hands, strategy, bet, num_of_decks):
    profits = []
    for i in range(amount_of_data):
        hand_profit_loss = simulate_hands(num_of_hands, strategy, bet, num_of_decks)[1]
        profits.append(hand_profit_loss)
    print(calculate_mean(profits))
    data = profits
    plt.hist(data, bins=10, edgecolor='black')
    plt.title(f'Histogram for {strategy.__name__}')
    plt.xlabel(f'profit from {num_of_hands} hands')
    plt.ylabel('Frequency')
    plt.show()




plot_hand_data(10000,100, basic_strategy, 25,6)
plot_hand_data(10000,100, simplest_strategy, 25,6)
plot_hand_data(10000,100, random_strategy, 25,6)
plot_hand_data(10000,100, basic_strategy_no_split, 25,6)
plot_hand_data(10000,100, basic_strategy_no_aces, 25,6)
plot_hand_data(10000,100, basic_strategy_no_splits_or_aces, 25,6)





