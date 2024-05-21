# SPADES

Code that plays games of spades

Collects results of hands for training data set for hand modeling

Initial game development includes hard-coded strategy for each player


## Strategy Description


### Play Card Strategy

The strategy to play cards is logically split by whether the player is leading the trick or cards have already been played that trick.

#### Leading card strategy

1. If player currently has not yet met their bid -> play highest non-spade card
2. If player has met their bid -> play lowest non-spade card

#### Following card strategy

1. If the player can follow suit, if the player has not yet met their bid, if player has a card that can win trick -> play lowest winning card of the leading suit 
2. If the player can follow suit, if the player has not yet met their bid, if player does not have card that can win trick -> play lowest card of the leading suit 
3. If the player can follow suit, if the player has met their bid -> play lowest card of the leading suit 
4. If the player cannot follow suit, if the player has not yet met their bid, if Spades already played this trick, if player has a spade that can win -> play lowest winning spade 
5. If the player cannot follow suit, if the player has not yet met their bid, if Spades already played this trick, if player has only spades but cannot win -> play lowest spade 
6. If the player cannot follow suit, if the player has not yet met their bid, if Spades already played this trick, if player has no spades -> play lowest non-spade card 
7. If the player cannot follow suit, if the player has not yet met their bid, no spades played yet this trick, player has spades -> play lowest spade 
8. If the player cannot follow suit, if the player has not yet met their bid, no spades played yet this trick, player has no spades -> play lowest non-spade 
9. If the player cannot follow suit, if the player has met their bid, player has non-spade cards -> play lowest non-spade card 
10. If the player cannot follow suit, if the player has met their bid, player only has spades -> play lowest spade


### Bid strategy
The player will bid the number of points created by the following calculation:

Bid = Spade points + non-spade points

Where:

Spade points = 1 - 1/13 * position decrement
Ace of Spades = 1.0, King of Spades = 0.87, Queen = 0.74, etc.

Non-Spade points:
* Ace - 0.8
* King - 0.6
* Queen - 0.4
* Jack - 0.2

This should be replaced by a model prediction soon.


## Development Next steps:

* Strategy development
  * Add code to add logic to remove points for extras
  * Develop random card strategy for baseline comparison
  * Develop more advanced strategy
    * Recreate training data set, modeling iterations
* Modeling
  * Create more features
  * Pytorch modeling
    * Add other layers
    * Train with early stopping
  * sklearn modeling
    * Tune random forest 
    * Train linear model
    * Train xgboost model
  * Create more evaluation metrics
    * Misclassification matrix
      * What percent of predictions were off by >1?
* Reinforcement Learning approach