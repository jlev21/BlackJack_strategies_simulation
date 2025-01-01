import random
import matplotlib.pyplot as plt
from blackjack import Deck, Hand, play_blackjack, simulate_hands, plot_hand_data, values


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
            if dealer_card_value == 6 and hand.can_double():
                return 'double'
            else:
                return 'stand'
        elif hand.value == 18:  # A,7
            if 2 <= dealer_card_value <= 6 and hand.can_double():
                return 'double'
            elif 9 <= dealer_card_value <= 11:
                return 'hit'
            else:
                return 'stand'
        elif hand.value == 17:  # A,6
            if 3 <= dealer_card_value <= 6 and hand.can_double():
                return 'double'
            else:
                return 'hit'
        elif 15 <= hand.value <= 16:  # A,4 and A,5
            if 4 <= dealer_card_value <= 6 and hand.can_double():
                return 'double'
            else:
                return 'hit'
        elif 13 <= hand.value <= 14:  # A,2 and A,3
            if 5 <= dealer_card_value <= 6 and hand.can_double():
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
    elif hand.value == 11 and hand.can_double():
        return 'double'
    elif hand.value == 10:
        if dealer_card_value <= 9 and hand.can_double():
            return 'double'
        else:
            return 'hit'
    elif hand.value == 9:
        if 3 <= dealer_card_value <= 6 and hand.can_double():
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
            if 2 <= dealer_card_value <= 9 and hand.can_double():
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
    elif hand.value == 11 and hand.can_double():
        return 'double'
    elif hand.value == 10:
        if dealer_card_value <= 9:
            return 'double'
        else:
            return 'hit'
    elif hand.value == 9:
        if 3 <= dealer_card_value <= 6 and hand.can_double():
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
    elif hand.value == 11 and hand.can_double():
        return 'double'
    elif hand.value == 10:
        if dealer_card_value <= 9 and hand.can_double():
            return 'double'
        else:
            return 'hit'
    elif hand.value == 9:
        if 3 <= dealer_card_value <= 6 and hand.can_double():
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
            if 2 <= dealer_card_value <= 9 and hand.can_double():
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
            if dealer_card_value == 6 and hand.can_double():
                return 'double'
            else:
                return 'stand'
        elif hand.value == 18:  # A,7
            if 2 <= dealer_card_value <= 6 and hand.can_double():
                return 'double'
            elif 9 <= dealer_card_value <= 11:
                return 'hit'
            else:
                return 'stand'
        elif hand.value == 17:  # A,6
            if 3 <= dealer_card_value <= 6 and hand.can_double():
                return 'double'
            else:
                return 'hit'
        elif 15 <= hand.value <= 16:  # A,4 and A,5
            if 4 <= dealer_card_value <= 6 and hand.can_double():
                return 'double'
            else:
                return 'hit'
        elif 13 <= hand.value <= 14:  # A,2 and A,3
            if 5 <= dealer_card_value <= 6 and hand.can_double():
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
    elif hand.value == 11 and hand.can_double():
        return 'double'
    elif hand.value == 10:
        if dealer_card_value <= 9 and hand.can_double:
            return 'double'
        else:
            return 'hit'
    elif hand.value == 9:
        if 3 <= dealer_card_value <= 6 and hand.can_double:
            return 'double'
        else:
            return 'hit'
    else:
        return 'hit'

strategies = {
        "simplest": simplest_strategy,
        "random": random_strategy,
        "basic": basic_strategy,
        "basic_no_split": basic_strategy_no_split,
        "basic_no_aces": basic_strategy_no_aces,
        "basic_no_splits_or_aces": basic_strategy_no_splits_or_aces,
}


def run_blackjack_simulation():
    print("Welcome to Blackjack Simulator!")

    # List all available strategies
    print("\nAvailable strategies:")
    for strategy_name in strategies:
        print(f" - {strategy_name}")
    strategy_choice = input("Choose a strategy: ").strip().lower()

    if strategy_choice not in strategies:
        print("Invalid strategy choice. Exiting.")
        return

    strategy_function = strategies[strategy_choice]

    # Get number of decks
    try:
        num_of_decks = int(input("Enter the number of decks to play with: "))
        if num_of_decks <= 0:
            raise ValueError
    except ValueError:
        print("Invalid number of decks. Exiting.")
        return

    # Get bet amount
    try:
        bet_amount = int(input("Enter your bet amount: "))
    except ValueError:
        print("Invalid bet amount. Exiting.")
        return

    # Get number of hands played per day
    try:
        num_of_hands = int(input("Enter the number of hands you play in a day: "))
    except ValueError:
        print("Invalid number of hands. Exiting.")
        return

    # Get number of days to simulate
    try:
        amount_of_data = int(input("Enter the number of days you want to simulate: "))
    except ValueError:
        print("Invalid number of days. Exiting.")
        return

    # Ask if the user wants to plot results
    plot_choice = input("Would you like to plot the results? (yes/no): ").strip().lower()
    plot_results = plot_choice in ("yes", "y")

    # Simulate the games
    print("\nSimulating games...")
    profits = []
    total_hands_played = num_of_hands * amount_of_data
    for _ in range(amount_of_data):
        _, total_profit_loss = simulate_hands(num_of_hands, strategy_function, bet_amount, num_of_decks)
        profits.append(total_profit_loss)

    # Calculate results
    total_profit = sum(profits)
    average_daily_profit = total_profit / amount_of_data
    house_edge = (total_profit / (total_hands_played * bet_amount)) * -100

    # Print results
    print(f"\nSimulation complete!")
    print(f"Total Profit: {total_profit}")
    print(f"Average Daily Profit: {average_daily_profit:.2f}")
    print(f"House Edge: {house_edge:.2f}%")

    # Plot the results if requested
    if plot_results:
        print("\nPlotting results...")
        plt.hist(profits, bins=10, edgecolor='black')
        plt.title(f'Profit Distribution over {amount_of_data} Days')
        plt.xlabel('Daily Profit/Loss')
        plt.ylabel('Frequency')
        plt.show()
    else:
        print("Plotting skipped.")

if __name__ == "__main__":
    run_blackjack_simulation()


