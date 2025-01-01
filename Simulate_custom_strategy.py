import random
import matplotlib.pyplot as plt
from blackjack import Deck, play_blackjack, simulate_hands, values
from Simulate_premade_strategy import basic_strategy


# Learn Strategy Function
def learn_strategy():
    """
    Allow users to input their strategy upfront, overriding the default basic strategy.
    """
    print("\nFirst you will define specifically which changes you want to make to basic strategy in your custom strategy")
    print("\nProvide your overrides using the following format:")
    print("Example: hard, 17, 10, hit")
    print("Format: <hand_type>, <hand_value>, <dealer_card>, <action>")
    print("Type 'done' to finish input.")
    print("\nDefaults to Basic Strategy for all undefined scenarios.\n")

    strategy_memory = {}

    while True:
        user_input = input("Enter a strategy (or 'done' to finish): ").strip().lower()
        if user_input == "done":
            break

        try:
            hand_type, hand_value, dealer_card, action = map(str.strip, user_input.split(","))
            if hand_type not in ("hard", "soft") or action not in ("hit", "stand", "double", "split"):
                raise ValueError

            hand_value = int(hand_value)
            dealer_card = int(dealer_card)
            strategy_memory[(hand_type, hand_value, dealer_card)] = action

        except ValueError:
            print("Invalid input. Please follow the format: <hand_type>, <hand_value>, <dealer_card>, <action>")

    print("\nYour overrides have been added to the Basic Strategy.")
    return strategy_memory


# Custom Strategy Wrapper
def custom_strategy_with_defaults(strategy_memory):
    """
    Custom strategy function based on user-defined memory and Basic Strategy as default.
    """
    def custom_strategy(hand, dealer_card):
        is_soft = any(card[0] == 'Ace' for card in hand.cards) and hand.value <= 21
        dealer_card_value = values[dealer_card[0]]
        situation = ("soft" if is_soft else "hard", hand.value, dealer_card_value)

        # Use user-defined strategy if available, otherwise default to basic_strategy
        if situation in strategy_memory:
            return strategy_memory[situation]
        else:
            return basic_strategy(hand, dealer_card)  # Default fallback to Basic Strategy

    return custom_strategy


# Main Simulation Function
def run_custom_strategy_simulation():
    print("Welcome to Custom Blackjack Strategy Simulator!")

    # Learn the strategy with basic strategy as default
    strategy_memory = learn_strategy()
    user_defined_strategy = custom_strategy_with_defaults(strategy_memory)

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
        _, total_profit_loss = simulate_hands(num_of_hands, user_defined_strategy, bet_amount, num_of_decks)
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
    run_custom_strategy_simulation()