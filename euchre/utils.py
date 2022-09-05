# Helper utility functions

import numpy as np


class EuchreGame:
    """
    Main class for euchre game
    """
    card_suits = ['S', 'C', 'H', 'D']
    card_values = ['A', 'K', 'Q', 'J', 'T', '9']

    def __init__(self,
                 score=None,
                 dealer=None,
                 next_to_deal=None,
                 hands_played=0):
        if next_to_deal is None:
            next_to_deal = ['p2', 'p3', 'p4', 'p1']
        if score is None:
            score = {'t1': 0, 't2': 0}
        if dealer is None:
            dealer = 'p1'
        self.score = score
        self.dealer = dealer
        self.next_to_deal = next_to_deal
        self.hands_played = hands_played

    def print_score(self):
        print(f"Current score: {self.score['t1']}-{self.score['t2']}")

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

    def deal_hand(self,
                  verbose=False):
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
        print(f'Card flipped up: {card_flipped_up}' if verbose else None)
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

    def determine_trump(self,
                        card_flipped_up,
                        player_hands,
                        verbose=False):
        """
        Determine suit of trump for given hand

        Returns calling player, trump suit
        """
        for player in self.next_to_deal:
            if self.eval_flipped_card(suit=card_flipped_up[-1],
                                      hand=player_hands[player]):
                trump = card_flipped_up[-1]
                print(f'Player {player} has chosen {trump} as trump' if verbose else None)
                return player, trump
        for player in self.next_to_deal:
            trump = self.choose_open_trump(hand=player_hands[player],
                                           card_flipped_up=card_flipped_up)
            if trump is not None:
                print(f'Player {player} has chosen {trump} as trump' if verbose else None)
                return player, trump
        else:  # No "F the dealer"
            return None, None

    def play_card(self,
                  hand,
                  trump,
                  cards_in_play,
                  cards_played_this_hand,
                  suit_led=None):
        """
        Function to return card to play in hand
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
        if len(cards_in_play) < 1:
            for idx, card in enumerate(hand):
                # 1 - play right bauer
                if card[-1] == trump and card[0] == 'J':
                    return hand[idx]
                # TODO: 1A - if right bauer played, play left bauer
                right_bauer = 'J' + '_' + trump
                if right_bauer in cards_played_this_hand:
                    pass
                # 2 - play off ace
                elif card[-1] != trump:
                    if card[0] == 'A':
                        return hand[idx]
                # 3 - TODO: else play highest non-trump card
            return hand[0]

        # follow suit
        if suit_led is not None:
            # play lowest card in the suit played
            card_to_play_points = -1
            idx_to_return = -1
            for idx, card in enumerate(hand):
                if card[-1] == suit_led:
                    card_points = card_values[card[0]]
                    if card_points < card_to_play_points:
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

    def play_trick(self,
                   player_hands,
                   trump,
                   next_to_play_list,
                   cards_played_this_hand,
                   verbose=False):
        """
        Function to play one full trick

        """
        cards_in_play = {}
        suit_led = None
        for idx, player in enumerate(next_to_play_list):
            card_to_play = self.play_card(hand=player_hands[player],
                                          trump=trump,
                                          cards_in_play=cards_in_play,
                                          cards_played_this_hand=cards_played_this_hand,
                                          suit_led=suit_led)
            # add card_to_play
            cards_in_play[player] = card_to_play
            cards_played_this_hand.append(card_to_play)
            # update player hands after player has played card
            player_hands[player].remove(card_to_play)
            print(f'Player {player} plays {card_to_play}' if verbose else None, end=', ')
            if idx == 0:
                suit_led = card_to_play[-1]
                player_led = player
        # print(f'Cards in play: {cards_in_play}' if verbose else None)
        # print(f'Cards played this hand {cards_played_this_hand}' if verbose else None, end=', ')
        return cards_in_play, player_led

    def determine_trick_winner(self,
                               cards_in_play,
                               trump,
                               player_led,
                               verbose=False) -> str:
        """
        Determine winner of trick

        Returns player that won trick
        """
        # create dict for each trump
        trump_hierarchy_dict = {
            'D': ['J_D', 'J_H', 'A_D', 'K_D', 'Q_D', 'T_D', '9_D'],
            'H': ['J_H', 'J_D', 'A_H', 'K_H', 'Q_H', 'T_H', '9_H'],
            'C': ['J_C', 'J_S', 'A_C', 'K_C', 'Q_C', 'T_C', '9_C'],
            'S': ['J_S', 'J_C', 'A_S', 'K_S', 'Q_S', 'T_S', '9_S']
        }
        # loop over trump cards, highest to lowest
        for trump_card in trump_hierarchy_dict[trump]:
            # if in cards_in_play:
            if trump_card in cards_in_play.values():
                # return player that played that card
                winning_player = [k for k, v in cards_in_play.items() if v == trump_card][0]
                print(f'{winning_player} wins trick' if verbose else None)
                return winning_player
        led_suit = cards_in_play[player_led][-1]
        for card_val in self.card_values:
            for card_played in cards_in_play.values():
                if card_played[0] == card_val and card_played[-1] == led_suit:
                    # return player that played that card
                    winning_player = [k for k, v in cards_in_play.items() if v == card_played][0]
                    print(f'{winning_player} wins trick' if verbose else None)
                    return winning_player

    # TODO: update this for loners
    def update_score(self,
                     trick_winners,
                     calling_player,
                     verbose=False):
        """
        Update score for one hand given trick_winners and calling_player
        """
        t1_tricks = trick_winners['p1'] + trick_winners['p3']
        t2_tricks = trick_winners['p2'] + trick_winners['p4']
        if calling_player in ['p1', 'p3']:
            if t1_tricks in [3, 4]:
                self.score['t1'] += 1
                print(f't1 scores 1' if verbose else None)
            elif t1_tricks == 5:
                self.score['t1'] += 2
                print(f't1 scores 2' if verbose else None)
            else:
                self.score['t2'] += 2
                print(f't2 scores 2' if verbose else None)
        if calling_player in ['p2', 'p4']:
            if t2_tricks in [3, 4]:
                self.score['t2'] += 1
                print(f't2 scores 1' if verbose else None)
            elif t2_tricks == 5:
                self.score['t2'] += 2
                print(f't2 scores 2' if verbose else None)
            else:
                self.score['t1'] += 2
                print(f't1 scores 2' if verbose else None)

    @staticmethod
    def get_next_trick_order(trick_winner) -> list:
        """
        Function to return new next_to_play list after trick is taken
        """
        if trick_winner == 'p1':
            return ['p1', 'p2', 'p3', 'p4']
        if trick_winner == 'p2':
            return ['p2', 'p3', 'p4', 'p1']
        if trick_winner == 'p3':
            return ['p3', 'p4', 'p1', 'p2']
        if trick_winner == 'p4':
            return ['p4', 'p1', 'p2', 'p3']

    def swap_dealer_card(self,
                         card_flipped_up: str,
                         dealer_hand: list,
                         verbose=False) -> list:
        """
        Function to swap out ordered up trump card with one from dealer's hand
        Returns: dealer new hand
        """
        # TODO: apply some strategy here - drop lowest non-trump card
        # remove first card from dealer hand
        removed_card = dealer_hand[0]
        dealer_hand = dealer_hand[1:]
        dealer_hand.append(card_flipped_up)
        print(f'Dealer discards {removed_card} and picks up {card_flipped_up}' if verbose else None)
        return dealer_hand

    def play_hand(self,
                  verbose=False):
        """
        Function to play a single hand
        """
        # deal cards
        player_hands, card_flipped_up = self.deal_hand(verbose=verbose)
        # choose trump
        calling_player, trump = self.determine_trump(card_flipped_up=card_flipped_up,
                                                     player_hands=player_hands,
                                                     verbose=verbose)

        if trump is not None:
            # check if trump called is same suit as card_flipped_up
            if card_flipped_up[-1] == trump:
                self.swap_dealer_card(card_flipped_up=card_flipped_up,
                                      dealer_hand=player_hands[self.dealer],
                                      verbose=verbose)
            trick_winners = {p: 0 for p in self.next_to_deal}
            next_to_play_list = self.next_to_deal
            cards_played_this_hand = []
            for trick in range(5):
                cards_in_play, player_led = self.play_trick(player_hands=player_hands,
                                                            trump=trump,
                                                            next_to_play_list=next_to_play_list,
                                                            cards_played_this_hand=cards_played_this_hand,
                                                            verbose=verbose)
                trick_winner = self.determine_trick_winner(cards_in_play=cards_in_play,
                                                           trump=trump,
                                                           player_led=player_led,
                                                           verbose=verbose)
                trick_winners[trick_winner] += 1
                next_to_play_list = self.get_next_trick_order(trick_winner)
            print(f'Trick winners: {trick_winners}' if verbose else None)

            # update score
            self.update_score(trick_winners=trick_winners,
                              calling_player=calling_player,
                              verbose=verbose)
            if verbose:
                self.print_score()

            self.dealer = self.next_to_deal.pop(0)
            self.next_to_deal.append(self.dealer)
        else:
            print('Trump not found' if verbose else None)
            self.dealer = self.next_to_deal.pop(0)
            self.next_to_deal.append(self.dealer)

    def play_full_game(self,
                       verbose=False):
        """
        Play full game
        """
        while self.score['t1'] < 10 and self.score['t2'] < 10:
            print(f'Hand #{self.hands_played}' if verbose else None, end='- ')
            print(f'Dealer: {self.dealer}', end='; ')
            self.play_hand(verbose=verbose)
            self.hands_played += 1

        print(f'Total hands played {self.hands_played}' if verbose else None)
