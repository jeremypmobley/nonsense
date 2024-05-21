# Spades

import random


class Card:
    rank_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'Jack': 11, 'Queen': 12,
        'King': 13, 'Ace': 14
    }

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = Card.rank_values[rank]  # Store ranks as numeric values
        self.rank_str = rank  # Store the string value for display

    def __repr__(self):
        return f"{self.rank_str} of {self.suit}"


class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Deck.suits for rank in Deck.ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def summarize_hand(self):
        high_cards = ['Ace', 'King', 'Queen', 'Jack']
        spades = sorted((card for card in self.hand if card.suit == 'Spades'), key=lambda c: c.rank, reverse=True)
        other_highs = {'Ace': 0, 'King': 0, 'Queen': 0, 'Jack': 0}

        # Format spades for output
        spades_output = ' '.join(card.rank_str for card in spades)

        # Count high cards in non-spade suits
        for card in self.hand:
            if card.rank_str in high_cards and card.suit != 'Spades':
                other_highs[card.rank_str] += 1

        # Format the count of non-spade high cards
        others_output = ", ".join(f"{rank_str}: {count}" for rank_str, count in other_highs.items())
        bid_val = self.evaluate_hand()

        return f"Spades: {spades_output}; Others {others_output}; Bid val: {bid_val}"

    def evaluate_hand(self):
        # Define the base point values for non-spade face cards
        non_spade_points = {'Ace': 0.8, 'King': 0.6, 'Queen': 0.4, 'Jack': 0.2}
        total_points = 0

        # Calculate the number of cards in spades to determine decrement value
        spades = [card for card in self.hand if card.suit == 'Spades']
        decrement = 1.0 / 13

        # Calculate the points for spade cards based on linear decrease
        for i, card in enumerate(sorted(spades, key=lambda c: c.rank, reverse=True)):
            if card.rank == 'Ace':
                card_points = 1.0  # Highest value for Ace of Spades
            else:
                # Calculate decreasing value for other spades
                card_points = max(0, 1.0 - (i * decrement))
            total_points += card_points

        # Add points for non-spade high cards
        for card in self.hand:
            if card.suit != 'Spades' and card.rank in non_spade_points:
                total_points += non_spade_points[card.rank]

        return total_points

    def bid(self):
        return round(self.evaluate_hand())

    def play_highest_non_spades(self):
        """Return the highest card that is not a Spades card."""
        non_spades = [card for card in self.hand if card.suit != 'Spades']
        if non_spades:
            return max(non_spades, key=lambda c: c.rank)
        return None  # If no non-spades are available

    def play_lowest_non_spades(self):
        """Return the lowest card that is not a Spades card."""
        non_spades = [card for card in self.hand if card.suit != 'Spades']
        if non_spades:
            return min(non_spades, key=lambda c: c.rank)
        return None  # If no non-spades are available

    def play_follow_card(self, leading_suit, trick_cards, need_more_tricks):
        """
        Function to apply when player is not leading
        trick_cards should always contain at least one other card
        """
        highest_card_in_trick = max((card for card in trick_cards if card.suit == leading_suit),
                                    key=lambda c: c.rank, default=None)
        highest_spade_in_trick = max((card for card in trick_cards if card.suit == 'Spades'),
                                     key=lambda c: c.rank, default=None)

        # Check if the player has cards of the leading suit
        cards_of_leading_suit = [card for card in self.hand if card.suit == leading_suit]

        if cards_of_leading_suit:  # must follow suit
            if need_more_tricks:
                winning_cards = [card for card in cards_of_leading_suit if
                                 card.rank > highest_card_in_trick.rank]
                if winning_cards:  # Return the lowest winning card of the leading suit
                    return min(winning_cards, key=lambda c: c.rank)
                else:
                    # No winning card, play the lowest card of the leading suit
                    return min(cards_of_leading_suit, key=lambda c: c.rank)
            else:  # doesn't want to take tricks
                return min(cards_of_leading_suit, key=lambda c: c.rank)  # play the lowest card of the leading suit
                # TODO: update this to highest card that doesn't take the trick
        else:  # Player does not have cards of the leading suit, can play Spade or other suits
            if need_more_tricks:  # player wants to take trick
                if highest_spade_in_trick:  # a spade has been played this trick
                    if any(card.suit == 'Spades' for card in self.hand):  # player has spades
                        spades_in_hand = [card for card in self.hand if card.suit == 'Spades']
                        winning_spades = [card for card in spades_in_hand if
                                          card.rank > highest_spade_in_trick.rank]
                        if winning_spades:  # player has a spade that can win
                            return min(winning_spades, key=lambda c: c.rank)  # Play the lowest winning Spade
                        else:  # player doesn't have a spade that can win
                            if len(spades_in_hand) == len(self.hand):  # player only has spades but none of them can win
                                return min(spades_in_hand, key=lambda c: c.rank)
                            else:
                                return self.play_lowest_non_spades()
                    else:  # player has no spades
                        return self.play_lowest_non_spades()
                else:  # no spades played this trick
                    if any(card.suit == 'Spades' for card in self.hand):  # player has spades
                        return min((card for card in self.hand if card.suit == 'Spades'), key=lambda c: c.rank)
                    else:  # player has no spades
                        return self.play_lowest_non_spades()
            else:  # player doesn't want to take trick
                # TODO: update this to highest card that doesn't take the trick
                if any(card.suit != 'Spades' for card in self.hand):  # player has non-spade card
                    return self.play_lowest_non_spades()
                else:
                    return min((card for card in self.hand if card.suit == 'Spades'), key=lambda c: c.rank)

    def play_lead_card(self, leading_suit, trick_cards, need_more_tricks):
        if need_more_tricks:
            # play highest non-spade, else play highest spade card
            lead_card = self.play_highest_non_spades() or max(self.hand, key=lambda c: c.rank)
            # TODO: check if player has highest spade remaining
            # TODO: play card with highest likelihood of taking trick (fewest cards higher within suit)
        else:
            # play lowest non-spade, else play lowest card
            lead_card = self.play_lowest_non_spades() or min(self.hand, key=lambda c: c.rank)
            # TODO: play card with lowest likelihood of taking trick (fewest cards lower)
        return lead_card

    def play_card(self, leading_suit, trick_cards, all_played_cards, bids, tricks_won, player_index):
        need_more_tricks = tricks_won[player_index] < bids[player_index]
        is_leading = leading_suit is None  # Player is leading if there's no leading suit set yet

        if is_leading:
            card_to_play = self.play_lead_card(leading_suit, trick_cards, need_more_tricks)

        else:  # Not leading
            card_to_play = self.play_follow_card(leading_suit, trick_cards, need_more_tricks)

        self.hand.remove(card_to_play)
        return card_to_play


class Game:
    def __init__(self, verbose=False):
        self.deck = Deck()
        self.players = [Player(f"Player {i + 1}") for i in range(4)]
        self.scores = [0] * 4
        self.data = []  # Initialize an empty list to store game data
        self.verbose = verbose
        self.cards_played_this_hand = []  # Track all cards played in the hand

    def binary_hand_representation(self, hand):
        # Create a 52-length vector of zeros
        binary_vector = [0] * 52
        suit_base = {'Hearts': 0, 'Diamonds': 13, 'Clubs': 26, 'Spades': 39}
        for card in hand:
            # Subtract 2 because ranks start at 2 (2 -> index 0)
            index = suit_base[card.suit] + (card.rank - 2)
            binary_vector[index] = 1
        return binary_vector

    def log_data(self, player, hand, bid, tricks_won, game_score):
        hand_str = ','.join(map(str, hand))  # Convert binary vector to comma-separated string
        self.data.append([player.name, hand_str, bid, tricks_won, game_score])

    def reset_hand(self):
        self.cards_played_this_hand = []
        self.deck.shuffle()
        self.deal_cards()

    def deal_cards(self):
        for i in range(52):
            self.players[i % 4].hand.append(self.deck.cards[i])

    def play(self):
        while all(score < 500 for score in self.scores):  # Continue until a player reaches 500 points
            self.reset_hand()  # Reset the hand at the start of each new round

            # Log initial hands right after dealing
            initial_hands = [self.binary_hand_representation(player.hand) for player in self.players]

            bids = [player.bid() for player in self.players]
            if self.verbose:
                print(f"Bids: {bids}")
                for player in self.players:
                    print(player.summarize_hand())
            current_leader = 0
            tricks_won = [0] * 4

            # Loop over tricks
            for trick_number in range(13):
                trick_winner = self.play_trick(leader=current_leader, tricks_won=tricks_won, bids=bids)
                tricks_won[trick_winner] += 1
                current_leader = trick_winner  # Winner leads the next trick

            self.score_round(bids, tricks_won)
            for i, player in enumerate(self.players):
                self.log_data(player, initial_hands[i], bids[i], tricks_won[i], self.scores[i])
            if self.verbose:
                print(f"Scores: {self.scores}")

    def play_trick(self, leader, tricks_won, bids):
        trick_cards = []  # List to keep track of cards played in this trick
        leading_suit = None
        highest_card = None
        trick_winner = leader

        for i in range(4):
            player_index = (leader + i) % 4
            card = self.players[player_index].play_card(
                leading_suit,
                trick_cards,
                self.cards_played_this_hand,
                bids,
                tricks_won,
                player_index
            )
            trick_cards.append(card)  # Add played card to trick history
            self.cards_played_this_hand.append(card)  # Add played card to the hand history

            if i == 0:  # First player sets the leading suit
                leading_suit = card.suit

            if self.verbose:
                print(f"{self.players[player_index].name} plays {card}", end=', ')

            # Determine if the current card beats the highest card so far
            if highest_card is None or \
                    (card.suit == 'Spades' and highest_card.suit != 'Spades') or \
                    (card.suit == highest_card.suit and card.rank > highest_card.rank):
                highest_card = card
                trick_winner = player_index

        if self.verbose:
            print(f"{self.players[trick_winner].name} wins trick")
        return trick_winner

    def score_round(self, bids, tricks_won):
        # Updates self.scores based on bids, tricks_won
        # TODO: add logic to remove 100 points for overs
        for i in range(4):
            self.scores[i] += (tricks_won[i] * 10) + (tricks_won[i] - bids[i]) if tricks_won[i] >= bids[i] else tricks_won[i] * -10


if __name__ == "__main__":
    game = Game()
    game.play()
