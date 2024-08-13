import random

# Constants for the game
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


# Deck Class
class Deck:
    def __init__(self, num_decks):
        self.deck = []
        for i in range(num_decks):
            for suit in suits:
                for rank in ranks:
                    self.deck.append((rank, suit))
        random.shuffle(self.deck)

    def deal(self):
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


# simple blackjack strategy: hit if below 17

def random_strategy(hand, dealer_card):
    choice = random.randint(1,2)
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


def basic_strategy_no_splits_or_aces(hand,dealer_card):
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


# Function to simulate a hand of blackjack
def play_blackjack(strategy_function, initial_bet, num_of_decks):
    deck = Deck(num_of_decks)
    player_hand = Hand(initial_bet)
    dealer_hand = Hand(0)  # Dealer doesn't have a bet amount

    # Initial dealing
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    print(f"Player's hand: {player_hand.cards}, Value: {player_hand.value}")
    print(f"Dealer's visible card: {dealer_hand.cards[0]}")

    # Check for blackjack
    if dealer_hand.is_blackjack():
        if player_hand.is_blackjack():
            print("Both player and dealer have blackjack! It's a tie.")
            return 0  # No profit or loss
        else:
            print("Dealer has blackjack! Player loses.")
            return int(initial_bet * -1)  # Player loses the bet

    if player_hand.is_blackjack():
        print("Player has blackjack! Player wins 1.5 times the bet.")
        return int(initial_bet * 1.5)  # Player wins 1.5 times the bet

    hands = [player_hand]  # Initialize with the player's original hand
    total_profit_loss = 0  # Track total profit or loss

    # Process each hand (to handle splitting)
    for hand in hands:
        while True:
            action = strategy_function(hand, dealer_hand.cards[0])
            print(f"Player's action: {action}")

            if action == 'hit':
                hand.add_card(deck.deal())
                print(f"Player hits: {hand.cards}, Value: {hand.value}")
                if hand.value > 21:
                    total_profit_loss -= hand.bet_amount
                    print(f"Player busts! Lost ${hand.bet_amount}.")
                    return int(initial_bet*-1)

            elif action == 'stand':
                print(f"Player stands with value: {hand.value}")
                break

            elif action == 'double':
                hand.double_bet()
                hand.add_card(deck.deal())
                print(f"Player doubles: {hand.cards}, Value: {hand.value}")
                if hand.value > 21:
                    total_profit_loss -= hand.bet_amount
                    print(f"Player busts after doubling! Lost ${hand.bet_amount}.")
                    hand.profit_loss = -hand.bet_amount  # Mark this hand as a bust
                break

            elif action == 'split':
                if hand.can_split():
                    print("Player splits!")
                    # Create two new hands from the split
                    new_hand1 = Hand(hand.bet_amount)
                    new_hand2 = Hand(hand.bet_amount)

                    # Add one card from the original hand to each new hand
                    new_hand1.add_card(hand.cards[0])
                    new_hand2.add_card(hand.cards[1])

                    # Deal one more card to each hand
                    new_hand1.add_card(deck.deal())
                    new_hand2.add_card(deck.deal())

                    print(f"New hand 1: {new_hand1.cards}, Value: {new_hand1.value}")
                    print(f"New hand 2: {new_hand2.cards}, Value: {new_hand2.value}")

                    # Add these new hands to the list of hands to process
                    hands.append(new_hand1)
                    hands.append(new_hand2)

                    break  # Stop processing the current hand, as it has been split
            else:
                break

    # Dealer's turn
    print(f"Dealer's hand: {dealer_hand.cards}, Value: {dealer_hand.value}")
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())
        print(f"Dealer hits: {dealer_hand.cards}, Value: {dealer_hand.value}")

    # Determine the outcome for each hand
    for hand in hands:
        if dealer_hand.value > 21:
            total_profit_loss += hand.bet_amount
            print(f"Dealer busts! Player wins ${hand.bet_amount}.")
        elif dealer_hand.value > hand.value:
            total_profit_loss -= hand.bet_amount
            print(f"Dealer wins. Player loses ${hand.bet_amount}.")
        elif dealer_hand.value < hand.value:
            total_profit_loss += hand.bet_amount
            print(f"Player wins ${hand.bet_amount}.")
        else:
            print(f"It's a tie. No profit or loss.")

    return total_profit_loss


# Test the game with the basic strategy
total_profit_loss = play_blackjack(basic_strategy, 100,2)
print(f"Total profit or loss: ${total_profit_loss}")
