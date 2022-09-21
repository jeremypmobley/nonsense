# Euchre

Play games of Euchre and analyze the results

## Goal: 
Create a fully functional euchre game to better understand winning probabilities of different starting hands

### Identify Optimal Strategy
How much does it increase the expected points earned from a hand if a player 'plays into' partners short-suit?

### Build a Model to Predict Points Scored From Given Hand
Answering the question:
Given the cards in a players hand (and position at the table), what is the likelihood of winning each number of tricks that hand? 

### Future Ideas:
* Streamlit app where user can select cards in hand and table position and get breakdown of likelihood of taking 5/4/3/2/1/0 tricks
* Reinforcement learning agent to call trump
* PySimpleGUI to learn to play game
  * Hide/show opponents hands
  * Keep list of cards played, trump left


### Trick Phase, 1st Round

So far the points in front of each player are as follows:

| Player | Cards | Possible Points |
|--------|------:|----------------:|
| Player A | 4♠ | 4 |
| Player B | 2♣ | 2 |
| Player C | 5♠ 6♦ | 11 |
| Player D | 4♦ 5♣ 5♥ 7♥ | 21 | 


 
| Player | Hand |
|--------|:-----:|
| Player A | `7♣ 8♦ 9♠ K♥ K♦` |
| Player B | `4♥ 10♦ 10♠ J♥ A♣` |
| Player C | `3♣ 8♥ 9♥ 9♣ Q♥` |
| Player D | `3♠ 7♦ J♦ J♠ Q♣` |
