# Helper utility functions

import numpy as np
import copy


CARD_VALUES = {
        'A': 6,
        'K': 5,
        'Q': 4,
        'J': 3,
        'T': 2,
        '9': 1,
    }


def print_if_verbose(thing_to_print, verbose=False, **kwargs):
    if verbose:
        print(thing_to_print, **kwargs)


def return_off_suit(suit: str) -> str:
    """
    Function to return off-suit

    :param: suit
    :returns suit

    """
    if suit == 'H':
        return 'D'
    if suit == 'D':
        return 'H'
    if suit == 'C':
        return 'S'
    if suit == 'S':
        return 'C'


def play_random_card(hand,
                     suit_led=None):
    """
    Function to play random card from hand
    """
    eligible_cards = []
    if suit_led is not None:
        for card in hand:
            if card[-1] == suit_led:
                eligible_cards.append(card)
        if len(eligible_cards) > 0:
            return np.random.choice(eligible_cards)
        else:
            return np.random.choice(hand)
    else:
        return np.random.choice(hand)


def get_lowest_card_in_suit(hand: list,
                            suit: str = None):
    """
    Return lowest card in given suit
    Returns None if no card in given suit
    """
    card_to_play_points = 9
    idx_to_return = -1
    if suit is not None:
        for idx, card in enumerate(hand):
            if card[-1] == suit:  # if card is in given suit
                card_points = CARD_VALUES[card[0]]
                if card_points < card_to_play_points:
                    card_to_play_points = card_points
                    idx_to_return = idx
        if idx_to_return > -1:
            return hand[idx_to_return]


# TODO: limit this down to non-trump suits
# TODO: update this to get_lowest_non_trump card ???
def get_lowest_card(hand: list):
    """
    Return lowest card in hand across all suits
    """
    card_to_play_points = 9
    idx_to_return = 0
    for idx, card in enumerate(hand):
        card_points = CARD_VALUES[card[0]]
        if card_points < card_to_play_points:
            card_to_play_points = card_points
            idx_to_return = idx
    return hand[idx_to_return]


class EuchreGame:
    """
    Main class for euchre game
    """
    team_assignments = {
        'p1': 't1',
        'p2': 't2',
        'p3': 't1',
        'p4': 't2',
    }

    def __init__(self,
                 score=None,
                 dealer=None,
                 next_to_deal=None,
                 team_strategies=None,
                 hands_played=0):
        if next_to_deal is None:
            next_to_deal = ['p2', 'p3', 'p4', 'p1']
        if score is None:
            score = {'t1': 0, 't2': 0}
        if dealer is None:
            dealer = 'p1'
        if team_strategies is None:
            team_strategies = {'t1': None,
                               't2': None}
        self.score = score
        self.dealer = dealer
        self.next_to_deal = next_to_deal
        self.hands_played = hands_played
        self.team_strategies = team_strategies

    def print_score(self):
        """ Print current score of game """
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

        :param verbose: True/False to print out log statements
        :returns player_hands dict, card_flipped_up
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
        print_if_verbose(f'Card flipped up: {card_flipped_up}', verbose=verbose)
        print_if_verbose(f'Player hands: {player_hands}', verbose=verbose)
        return player_hands, card_flipped_up

    @staticmethod
    def eval_flipped_card(suit: str,
                          hand: list) -> bool:
        """
        Function to evaluate if a player will order up trump
        If hand has at least 3 trump cards

        :param suit: Suit of flipped card to evaluate
        :param hand: List of cards in player's hand
        :returns True/False
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
    def choose_open_trump(hand: list,
                          card_flipped_up: str) -> str:
        """
        Function to choose trump after card is turned down
        If hand has at least 3 trump cards

        :param hand: List of cards in player's hand
        :param card_flipped_up: Card flipped up
        :returns trump
        """
        suits_eligible = ['S', 'C', 'H', 'D']
        suits_eligible.remove(card_flipped_up[-1])
        for suit in suits_eligible:
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
        Loops through players in next_to_deal twice and applies eval_flipped_card then choose_open_trump

        :param card_flipped_up: Card flipped up
        :param player_hands: Dict of lists of cards in player hands
        :param verbose: True/False to print out log statements
        :returns calling player, trump suit
        """
        for player in self.next_to_deal:
            if self.eval_flipped_card(suit=card_flipped_up[-1],
                                      hand=player_hands[player]):
                trump = card_flipped_up[-1]
                print_if_verbose(f'Player {player} has chosen {trump} as trump', verbose=verbose)
                return player, trump
        for player in self.next_to_deal:
            trump = self.choose_open_trump(hand=player_hands[player],
                                           card_flipped_up=card_flipped_up)
            if trump is not None:
                print_if_verbose(f'Player {player} has chosen {trump} as trump', verbose=verbose)
                return player, trump
        else:  # No "F the dealer"
            return None, None

    def play_lead_card(self,
                       hand,
                       trump,
                       cards_played_this_hand):
        """
        Play lead card
        """
        trump_hierarchy_dict = {
            'D': ['J_D', 'J_H', 'A_D', 'K_D', 'Q_D', 'T_D', '9_D'],
            'H': ['J_H', 'J_D', 'A_H', 'K_H', 'Q_H', 'T_H', '9_H'],
            'C': ['J_C', 'J_S', 'A_C', 'K_C', 'Q_C', 'T_C', '9_C'],
            'S': ['J_S', 'J_C', 'A_S', 'K_S', 'Q_S', 'T_S', '9_S']
        }
        # identify highest un-played trump card
        highest_remaining_trump = None
        for idx, trump_card in enumerate(trump_hierarchy_dict[trump]):
            if trump_card not in cards_played_this_hand:
                highest_remaining_trump = trump_card
                break
        card_to_play_points = -1
        idx_to_return = None
        for idx, card in enumerate(hand):
            # play the highest trump card remaining
            if card == highest_remaining_trump:
                return card
            # find index of highest non-trump card
            elif card[-1] != trump:
                card_points = CARD_VALUES[card[0]]
                if card_points > card_to_play_points:
                    card_to_play_points = card_points
                    idx_to_return = idx
        if idx_to_return is not None:
            return hand[idx_to_return]
        else:
            return get_lowest_card(hand)

    def play_card(self,
                  hand,
                  trump,
                  cards_in_play,
                  player_led,
                  cards_played_this_hand,
                  suit_led=None,
                  verbose=False):
        """
        Function to return card to play in hand
        # TODO: check if current winner is teammate or not
        """
        # play last card
        if len(hand) == 1:
            print_if_verbose(f'Last card', verbose=verbose, end='- ')
            return hand[0]

        # lead card
        if len(cards_in_play) < 1:
            print_if_verbose(f'Leading off', verbose=verbose, end='- ')
            lead_card = self.play_lead_card(hand=hand,
                                            trump=trump,
                                            cards_played_this_hand=cards_played_this_hand)
            return lead_card

        # follow suit
        if suit_led is not None:
            current_winning_player = self.determine_trick_winner(cards_in_play=cards_in_play,
                                                                 trump=trump,
                                                                 player_led=player_led)
            # print_if_verbose(f'Current winning player {current_winning_player}', verbose=verbose)

            # play the lowest card in the suit played
            lowest_card_in_suit = get_lowest_card_in_suit(hand=hand, suit=suit_led)
            if lowest_card_in_suit is not None:
                print_if_verbose(f'Following suit', verbose=verbose, end='- ')
                return lowest_card_in_suit
            # can't follow suit, play the lowest trump card
            else:
                lowest_trump_card = get_lowest_card_in_suit(hand=hand, suit=trump)
                if lowest_trump_card is not None:
                    print_if_verbose(f'Lowest_trump_card', verbose=verbose, end='- ')
                    return lowest_trump_card

                else:  # no trump, play the lowest card
                    lowest_card_in_hand = get_lowest_card(hand=hand)
                    print_if_verbose(f'Lowest_card_in_hand', verbose=verbose, end='- ')
                    return lowest_card_in_hand

    def play_trick(self,
                   player_hands,
                   trump,
                   next_to_play_list,
                   cards_played_this_hand,
                   verbose=False):
        """
        Function to play one full trick

        :param player_hands:
        :param trump: Trump called this hand
        :param next_to_play_list: List of players in order to play this trick
        :param cards_played_this_hand: List of all cards played this hand
        :param verbose: True/False to print out log statements
        :returns cards_in_play, player_led
        """
        cards_in_play = {}
        suit_led = None
        player_led = None
        for idx, player in enumerate(next_to_play_list):
            if self.team_strategies[self.team_assignments[player]] == 'random':
                card_to_play = play_random_card(hand=player_hands[player],
                                                suit_led=suit_led)
            else:
                card_to_play = self.play_card(hand=player_hands[player],
                                              trump=trump,
                                              cards_in_play=cards_in_play,
                                              player_led=player_led,
                                              cards_played_this_hand=cards_played_this_hand,
                                              suit_led=suit_led,
                                              verbose=verbose)

            print_if_verbose(f'Player {player} plays {card_to_play}', verbose=verbose, end=', ')
            # add card_to_play
            cards_in_play[player] = card_to_play
            cards_played_this_hand.append(card_to_play)
            # update player hands after player has played card
            player_hands[player].remove(card_to_play)
            if idx == 0:
                suit_led = card_to_play[-1]
                player_led = player
        return cards_in_play, player_led

    def determine_trick_winner(self,
                               cards_in_play,
                               trump,
                               player_led,
                               verbose=False) -> str:
        """
        Determine winner of trick

        :param cards_in_play: List of cards played this trick
        :param trump: Trump called this hand
        :param player_led: Player that led this trick
        :param verbose: True/False to print out log statements
        :returns Player that won trick
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
                print_if_verbose(f'{winning_player} wins trick', verbose=verbose)
                return winning_player
        led_suit = cards_in_play[player_led][-1]
        # TODO: rewrite this to not rely on dict key order
        for card_val in CARD_VALUES.keys():
            for card_played in cards_in_play.values():
                if card_played[0] == card_val and card_played[-1] == led_suit:
                    # return player that played that card
                    winning_player = [k for k, v in cards_in_play.items() if v == card_played][0]
                    print_if_verbose(f'{winning_player} wins trick', verbose=verbose)
                    return winning_player

    # TODO: update this for loners
    def update_score(self,
                     trick_winners,
                     calling_player,
                     verbose=False):
        """
        Update score for one hand given trick_winners and calling_player

        :param trick_winners: Dict with counts of number of tricks won per player
        :param calling_player: Player that called trump this hand
        :param verbose: True/False to print out log statements
        :returns None
        """
        t1_tricks = trick_winners['p1'] + trick_winners['p3']
        t2_tricks = trick_winners['p2'] + trick_winners['p4']
        hand_score = {'t1': 0, 't2': 0}
        if calling_player in ['p1', 'p3']:
            if t1_tricks in [3, 4]:
                self.score['t1'] += 1
                hand_score = {'t1': 1, 't2': 0}
                print_if_verbose(f't1 scores 1', verbose=verbose)
            elif t1_tricks == 5:
                self.score['t1'] += 2
                hand_score = {'t1': 2, 't2': 0}
                print_if_verbose(f't1 scores 2', verbose=verbose)
            else:
                self.score['t2'] += 2
                hand_score = {'t1': 0, 't2': 2}
                print_if_verbose(f't2 scores 2', verbose=verbose)
        if calling_player in ['p2', 'p4']:
            if t2_tricks in [3, 4]:
                self.score['t2'] += 1
                hand_score = {'t1': 0, 't2': 1}
                print_if_verbose(f't2 scores 1', verbose=verbose)
            elif t2_tricks == 5:
                self.score['t2'] += 2
                hand_score = {'t1': 0, 't2': 2}
                print_if_verbose(f't2 scores 2', verbose=verbose)
            else:
                self.score['t1'] += 2
                hand_score = {'t1': 2, 't2': 0}
                print_if_verbose(f't1 scores 2', verbose=verbose)
        return hand_score

    @staticmethod
    def get_next_trick_order(trick_winner: str) -> list:
        """
        Function to return new next_to_play list after trick is taken

        :param trick_winner: Player that won last trick
        :returns list of players in order for next trick
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

        :param card_flipped_up: card turned over
        :param dealer_hand: List of cards currently in dealer hand
        :param verbose: True/False to print out log statements
        :returns list of cards in dealer new hand
        """
        # TODO: add logic to drop lowest card with fewest others in that suit
        # TODO: add logic to drop lowest card that reduces number of suits in hand
        card_to_play_points = 9
        idx_to_return = 0
        for idx, card in enumerate(dealer_hand):
            if card[-1] == card_flipped_up[-1]:
                continue
            else:
                card_points = CARD_VALUES[card[0]]
                if card_points < card_to_play_points:
                    card_to_play_points = card_points
                    idx_to_return = idx
        removed_card = dealer_hand[idx_to_return]
        dealer_hand.remove(removed_card)
        dealer_hand.append(card_flipped_up)
        print_if_verbose(f'Dealer discards {removed_card} and picks up {card_flipped_up}', verbose=verbose)
        return dealer_hand

    def play_hand(self,
                  verbose=False):
        """
        Function to play a single hand
        Applies deal_hand and determine_trump functions, then loops through play_trick 5 times and updates scores

        :param verbose: True/False to print out log statements
        :returns hand_results dict

        """
        hand_results = {}
        # deal cards
        player_hands, card_flipped_up = self.deal_hand(verbose=verbose)

        # TODO: fix this - is deepcopy really necessary?
        hand_results['player_hands'] = copy.deepcopy(player_hands)
        # choose trump
        calling_player, trump = self.determine_trump(card_flipped_up=card_flipped_up,
                                                     player_hands=player_hands,
                                                     verbose=verbose)

        if trump is not None:
            if card_flipped_up[-1] == trump:
                self.swap_dealer_card(card_flipped_up=card_flipped_up,
                                      dealer_hand=player_hands[self.dealer],
                                      verbose=verbose)
            # hand_results['player_hands'] = player_hands
            hand_results['calling_player'] = calling_player
            hand_results['trump'] = trump
            hand_results['dealer'] = self.dealer
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
                # print_if_verbose(f'Cards played this hand list {cards_played_this_hand}', verbose=verbose)
            print_if_verbose(f'Trick winners: {trick_winners}', verbose=verbose)

            # update score
            hand_score = self.update_score(trick_winners=trick_winners,
                                           calling_player=calling_player,
                                           verbose=verbose)
            hand_results['hand_score'] = hand_score
            if verbose:
                self.print_score()

            self.dealer = self.next_to_deal.pop(0)
            self.next_to_deal.append(self.dealer)
            hand_results['trick_winners'] = trick_winners
            return hand_results
        else:
            print_if_verbose('Trump not found', verbose=verbose)
            self.dealer = self.next_to_deal.pop(0)
            self.next_to_deal.append(self.dealer)

    def play_full_game(self,
                       return_all_hands_results=False,
                       verbose=False):
        """
        Play full game
        """
        all_hand_results = []
        while self.score['t1'] < 10 and self.score['t2'] < 10:
            print_if_verbose(f'Hand #{self.hands_played}', verbose=verbose, end='- ')
            print_if_verbose(f'Dealer: {self.dealer}', verbose=verbose, end='; ')
            hand_results = self.play_hand(verbose=verbose)
            if hand_results is not None:
                all_hand_results.append(hand_results)
                self.hands_played += 1

        print_if_verbose(f'Total hands played {self.hands_played}', verbose=verbose)
        if return_all_hands_results:
            return all_hand_results
