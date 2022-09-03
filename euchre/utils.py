# Helper utility functions

import numpy as np


class EuchreGame:
    """
    Main class for euchre game
    """
    card_suits = ['S', 'C', 'H', 'D']
    card_values = ['9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self,
                 score=None,
                 dealer=None,
                 next_to_deal=None):
        if next_to_deal is None:
            next_to_deal = ['p2', 'p3', 'p4', 'p1']
        if score is None:
            score = [0, 0]
        if dealer is None:
            dealer='p1'
        self.score = score
        self.dealer = dealer
        self.next_to_deal = next_to_deal

    def print_score(self):
        print(f'Current score: {self.score[0]}-{self.score[1]}')

    @staticmethod
    def shuffle_deck_of_cards() -> list:
        """
        Function to reset the deck_of_cards
        Returns deck of cards list
        """
        suits = ['S', 'C', 'H', 'D']
        values = ['9', 'T', 'J', 'Q', 'K', 'A']
        deck_of_cards = [value + '_' + suit for value in values for suit in suits]
        return deck_of_cards

    def deal_hand(self):
        """
        Function to deal cards for hand
        Returns player_hands dict, card_flipped_up
        """
        player_hands = {
            'p1': [],
            'p2': [],
            'p3': [],
            'p4': []
        }
        deck_of_cards = self.shuffle_deck_of_cards()
        # loop through players, pick 5 cards, remove from deck_of_cards
        for idx, player in enumerate(player_hands):
            for _ in range(5):
                dealt_card = np.random.choice(deck_of_cards, replace=False)
                player_hands[player].append(dealt_card)
                deck_of_cards.remove(dealt_card)
        card_flipped_up = deck_of_cards[0]
        return player_hands, card_flipped_up

    @staticmethod
    def eval_flipped_card(suit, hand) -> bool:
        """
        Function to evaluate if a player will order up trump
        If hand has at least 3 trump cards

        Returns True/False
        """
        trumps = 0
        for card in hand:
            if card[-1] == suit:
                trumps += 1
        if trumps >= 3:
            return True
        else:
            return False

    @staticmethod
    def choose_open_trump(hand, card_flipped_up) -> str:
        """
        Function to choose trump after card is turned down
        If hand has at least 3 trump cards

        Returns string of chosen trump, or None
        """
        card_suits = ['S', 'C', 'H', 'D']
        card_suits.remove(card_flipped_up[-1])
        for suit in card_suits:
            trumps = 0
            for card in hand:
                if card[-1] == suit:
                    trumps += 1
            if trumps >= 3:
                return suit

    def determine_trump(self, card_flipped_up, player_hands):
        """
        Determine suit of trump for given hand

        Returns calling player, trump suit
        """
        for player in self.next_to_deal:
            if self.eval_flipped_card(suit=card_flipped_up[-1],
                                      hand=player_hands[player]):
                return player, card_flipped_up[-1]
        for player in self.next_to_deal:
            trump = self.choose_open_trump(hand=player_hands[player],
                                           card_flipped_up=card_flipped_up)
            if trump is not None:
                return player, trump
        else:
            return None, None

    def play_card(self,
                  hand,
                  trump,
                  cards_in_play=[],
                  suit_led=None):
        """
        Function to return index value of card to play in hand
        TODO: check if partner has winning card_in_pot
        """
        card_values = {
            '9': 1,
            'T': 2,
            'J': 3,
            'Q': 4,
            'K': 5,
            'A': 6
        }
        # play last card
        if len(hand) == 1:
            return hand[0]
        # lead card
        # TODO: develop logic for what card to lead
        if len(cards_in_play) < 1:
            return hand[0]
        # follow suit
        if suit_led is not None:
            # play highest card in the suit played
            card_to_play_points = -1
            idx_to_return = -1
            for idx, card in enumerate(hand):
                if card[-1] == suit_led:
                    card_points = card_values[card[0]]
                    if card_points > card_to_play_points:
                        card_to_play_points = card_points
                        idx_to_return = idx
            return hand[idx_to_return]
        # play other highest non-trump card
        else:
            card_to_play_points = -1
            idx_to_return = -1
            for idx, card in enumerate(hand):
                if card[-1] != trump:
                    card_points = card_values[card[0]]
                    if card_points > card_to_play_points:
                        card_to_play_points = card_points
                        idx_to_return = idx
            if idx_to_return > -1:
                return hand[idx_to_return]
            else:  # only has trump left, play lowest trump
                trump_card_points = 9
                for idx, card in enumerate(hand):
                    card_points = card_values[card[0]]
                    if card_points < trump_card_points:
                        trump_card_points = card_points
                        idx_to_return = idx
                return hand[idx_to_return]

    def play_hand(self):
        """
        Function to play a single hand
        """
        # deal cards
        player_hands, card_flipped_up = self.deal_hand()

        # choose trump
        calling_player, trump = self.determine_trump(card_flipped_up=card_flipped_up,
                                                     player_hands=player_hands)

        if trump is not None:
            pass

        # play hand
        # next_to_play_list = self.next_to_deal
            # play trick * 5

        # update score

        else:
            self.dealer = self.next_to_deal.pop(0)
            # reset self.next_to_deal order for next turn
            self.next_to_deal = self.next_to_deal.append(self.dealer)

    def play_full_game(self):
        """
        Play full game
        """
        # while score < 10:
        # self.play_hand()
        pass