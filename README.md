Use this project to simulate your blackjack sessions. Descriptions of each file are below:
## blackjack.py
Contains all of the classes and methods needed to play blackjack and simulate a certain number of hands
## Simulate_premade_strategy.py
This is used to simulate common strategies that are already premade. When this is run, the user is asked to input the strategy they want to simulate,
the number of decks to play with, the bet size, the number of hands they would play in a day, and the number of days that they want to simulate. Then it 
simulates blackjack with the chosen parameters, and tells the user information like profit/loss and house edge, and gives them a histogram representing the
distribution of profit/loss per day. Each premade strategy is described below:
### simplest
Hit if below 17, otherwise stand
### random
Randomly choose either to hit or stand
### basic
Optimal decision structure. This is referred to as "basic strategy" in blackjack. The decisions are according to the following table (surrender is not allowed):
![mini-blackjack-strategy-chart](https://github.com/user-attachments/assets/2a9491ab-4ca0-495f-9a15-3e331d2ccfc4)
Additionally there are some premade strategies that amend basic strategy, for example basic strategy without splitting or without doing anything different for soft totals.
I added these because they are the some of the most often cases where people play sub-optimally (not splitting or mishandling aces).
## Simulate_custom_strategy.py
The purpose of this is so that people can create their own strategies and simulate what would happen if they played x number of hands. First
it will ask the user to input their changes to basic strategy, and then it will act similarly to Simulate_premade_strategy.py, using the 
user defined strategy. The default here is "basic strategy" defined above.
## Test_strategy.py
This is primarily used for debugging purposes. It simulates hands with print statements.
