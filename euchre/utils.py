# Helper utility functions

import numpy as np
import copy


def print_if_verbose(thing_to_print, verbose=False, **kwargs):
    if verbose:
        print(thing_to_print, **kwargs)


# TODO: convert this to a dict lookup
def get_teammate(player: str) -> str:
    """
    Function to return teammate of player
    :param: player
    :returns player
    """
    if player == 'p1':
        return 'p3'
    if player == 'p2':
        return 'p4'
    if player == 'p3':
        return 'p1'
    if player == 'p4':
        return 'p2'


# TODO: convert this to a dict lookup
def return_off_suit(suit: str) -> str:
    """
    Function to return off-suit given suit
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


def get_highest_nontrump_card(hand: list, trump: str):
    """
    Return highest non-trump card in hand across all suits
    """
    card_values = {
        'A': 6,
        'K': 5,
        'Q': 4,
        'J': 3,
        'T': 2,
        '9': 1,
    }
    card_to_play_points = -1
    idx_to_return = None
    for idx, card in enumerate(hand):
        card_points = card_values[card[0]]
        if card_points > card_to_play_points and card[-1] != trump:
            card_to_play_points = card_points
            idx_to_return = idx
    if idx_to_return is not None:
        return hand[idx_to_return]
    else:  # is this necessary???
        return None


def get_lowest_trump_card(hand: list, trump: str):
    """
    Function to return lowest trump card in hand
    Returns None if no trump cards found
    """
    trump_hierarchy_dict = {
        'D': ['J_D', 'J_H', 'A_D', 'K_D', 'Q_D', 'T_D', '9_D'],
        'H': ['J_H', 'J_D', 'A_H', 'K_H', 'Q_H', 'T_H', '9_H'],
        'C': ['J_C', 'J_S', 'A_C', 'K_C', 'Q_C', 'T_C', '9_C'],
        'S': ['J_S', 'J_C', 'A_S', 'K_S', 'Q_S', 'T_S', '9_S']
    }
    trump_cards = trump_hierarchy_dict[trump]
    trump_cards.reverse()
    for card in trump_cards:
        if card in hand:
            return card


def get_lowest_nontrump_card_in_suit(hand: list,
                                     suit: str):
    """
    Function to return lowest non-trump card in suit from given hand
    Returns None if no cards found in suit
    """
    card_values = {
        'A': 6,
        'K': 5,
        'Q': 4,
        'J': 3,
        'T': 2,
        '9': 1,
    }
    card_to_play_points = 9
    idx_to_return = None
    for idx, card in enumerate(hand):
        if card[-1] == suit:  # if card is in given suit
            card_points = card_values[card[0]]
            if card_points < card_to_play_points:
                card_to_play_points = card_points
                idx_to_return = idx
    if idx_to_return is not None:
        return hand[idx_to_return]


# TODO: get rid of this and use get_lowest_nontrump_card_in_suit OR get_lowest_trump_card
def get_lowest_card(hand: list):
    """
    Return lowest card in hand across all suits
    """
    card_values = {
        'A': 6,
        'K': 5,
        'Q': 4,
        'J': 3,
        'T': 2,
        '9': 1,
    }
    card_to_play_points = 9
    idx_to_return = 0
    for idx, card in enumerate(hand):
        card_points = card_values[card[0]]
        if card_points < card_to_play_points:
            card_to_play_points = card_points
            idx_to_return = idx
    return hand[idx_to_return]


def get_lowest_nontrump_card_in_hand(hand: list,
                                     trump: str,
                                     cards_played_this_hand: list,
                                     no_trump_in_hand=False,
                                     verbose=False):
    """
    Function to return the lowest nontrump card overall in hand
    Return None if only trump cards remain in hand - must pass in no_trump_in_hand
    Returns card
    """
    card_values = {
        'A': 5,
        'K': 4,
        'Q': 3,
        'J': 2,
        'T': 1,
        '9': 0,
    }

    if no_trump_in_hand:  # play card that can take fewest other cards
        idx_to_return = 0
        fewest_lower_cards = 6
        for idx, card in enumerate(hand):
            lower_cards = card_values[card[0]]
            if lower_cards == 0:  # return nontrump 9 immediately
                return card
            for played_card in cards_played_this_hand:
                if played_card[-1] == trump or (return_off_suit(played_card[-1]) == trump and played_card[0] == 'J'):
                    continue
                if card[-1] == played_card[-1] and card_values[card[0]] > card_values[played_card[0]]:
                    lower_cards -= 1
            if lower_cards == 0:  # return nontrump card with no lower cards immediately
                return card
            if lower_cards < fewest_lower_cards:
                fewest_lower_cards = lower_cards
                idx_to_return = idx
        return hand[idx_to_return]

    else:
        # count trumps in hand
        num_trumps = 0
        for card in hand:
            if card[-1] == trump or (return_off_suit(card[-1]) == trump and card[0] == 'J'):
                num_trumps += 1

        if num_trumps == len(hand):  # only trump left
            return None

        if num_trumps > 0 and len(hand) > 2:  # if trump in hand, short suit
            # get suit counts
            suit_counts = {}
            for card in hand:
                if card[-1] == trump or (return_off_suit(card[-1]) == trump and card[0] == 'J'):  # don't count trump
                    continue
                if card[-1] in suit_counts.keys():
                    suit_counts[card[-1]] += 1
                else:
                    suit_counts[card[-1]] = 1
            # list of suit(s) with fewest count
            minval = min(suit_counts.values())
            short_suits = [k for k, v in suit_counts.items() if v == minval]
            # if there are multiple suits that could be shorted
            if len(short_suits) > 1:
                card_to_play_points = 9
                # find short suit with lowest card  # TODO: update this to card with fewest cards it can take
                for idx, card in enumerate(hand):
                    if card[-1] in short_suits and not (
                            return_off_suit(card[-1]) == trump and card[0] == 'J'):
                        card_points = card_values[card[0]]
                        if card_points < card_to_play_points:
                            card_to_play_points = card_points
                            idx_to_return = idx
                suit_to_play = hand[idx_to_return][-1]
            else:
                suit_to_play = short_suits[0]
            return get_lowest_nontrump_card_in_suit(hand=hand, suit=suit_to_play)

        else:  # play card that can take fewest other cards
            idx_to_return = 0
            fewest_lower_cards = 6
            for idx, card in enumerate(hand):
                if card[-1] == trump or (return_off_suit(card[-1]) == trump and card[0] == 'J'):  # don't play trump
                    continue
                lower_cards = card_values[card[0]]
                if lower_cards == 0:  # return nontrump 9 immediately
                    return card
                for played_card in cards_played_this_hand:
                    if played_card[-1] == trump or (
                            return_off_suit(played_card[-1]) == trump and played_card[0] == 'J'):
                        continue
                    if card[-1] == played_card[-1] and card_values[card[0]] > card_values[played_card[0]]:
                        lower_cards -= 1
                if lower_cards == 0:  # return nontrump card with no lower cards immediately
                    return card
                if lower_cards < fewest_lower_cards:
                    fewest_lower_cards = lower_cards
                    idx_to_return = idx
            return hand[idx_to_return]


def swap_dealer_card(card_flipped_up: str,
                     dealer_hand: list,
                     verbose=False) -> list:
    """
    Function to swap out ordered up trump card with one from dealer's hand

    :param card_flipped_up: card turned over
    :param dealer_hand: List of cards currently in dealer hand
    :param verbose: True/False to print out log statements

    :returns list of cards in dealer new hand
    """
    card_values = {
        'A': 6,
        'K': 5,
        'Q': 4,
        'J': 3,
        'T': 2,
        '9': 1,
    }
    # get suit counts
    suit_counts = {}
    for card in dealer_hand:
        if card[-1] == card_flipped_up[-1] or (
                return_off_suit(card[-1]) == card_flipped_up[-1] and card[0] == 'J'):  # don't count trump
            continue
        if card[-1] in suit_counts.keys():
            suit_counts[card[-1]] += 1
        else:
            suit_counts[card[-1]] = 1

    # if dealer only has trump
    if len(suit_counts) == 0:
        removed_card = dealer_hand[0]
        dealer_hand.remove(removed_card)
        dealer_hand.append(card_flipped_up)
        print_if_verbose(f'Dealer discards {removed_card} and picks up {card_flipped_up}', verbose=verbose)
        return dealer_hand

    # list of suit(s) with fewest count
    minval = min(suit_counts.values())
    short_suits = [k for k, v in suit_counts.items() if v == minval]

    # if there are multiple suits that could be shorted
    if len(short_suits) > 1:
        card_to_play_points = 9
        idx_to_return = 0
        # find short suit with lowest card
        for idx, card in enumerate(dealer_hand):
            if card[-1] in short_suits and not (
                    return_off_suit(card[-1]) == card_flipped_up[-1] and card[0] == 'J'):
                card_points = card_values[card[0]]
                if card_points < card_to_play_points:
                    card_to_play_points = card_points
                    idx_to_return = idx
        suit_to_play = dealer_hand[idx_to_return][-1]
    else:
        suit_to_play = short_suits[0]

    # find the lowest card in suit to short
    # TODO: replace this with get_lowest_nontrump_card_in_suit function
    card_to_play_points = 9
    idx_to_return = 0
    for idx, card in enumerate(dealer_hand):
        if card[-1] == suit_to_play and not (return_off_suit(card[-1]) == card_flipped_up[-1] and card[0] == 'J'):
            card_points = card_values[card[0]]
            if card_points < card_to_play_points:
                card_to_play_points = card_points
                idx_to_return = idx

    removed_card = dealer_hand[idx_to_return]
    dealer_hand.remove(removed_card)
    dealer_hand.append(card_flipped_up)
    print_if_verbose(f'Dealer discards {removed_card} and picks up {card_flipped_up}', verbose=verbose)
    return dealer_hand


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

    CARD_VALUES = {
        'A': 6,
        'K': 5,
        'Q': 4,
        'J': 3,
        'T': 2,
        '9': 1,
    }

    trump_hierarchy_dict = {
        'D': ['J_D', 'J_H', 'A_D', 'K_D', 'Q_D', 'T_D', '9_D'],
        'H': ['J_H', 'J_D', 'A_H', 'K_H', 'Q_H', 'T_H', '9_H'],
        'C': ['J_C', 'J_S', 'A_C', 'K_C', 'Q_C', 'T_C', '9_C'],
        'S': ['J_S', 'J_C', 'A_S', 'K_S', 'Q_S', 'T_S', '9_S']
    }

    def __init__(self,
                 score=None,
                 dealer=None,
                 next_to_deal=None,
                 tm_play_card_strategy=None,
                 tm_call_trump_strategy=None,
                 hands_played=0):
        if next_to_deal is None:
            next_to_deal = ['p2', 'p3', 'p4', 'p1']
        if score is None:
            score = {'t1': 0, 't2': 0}
        if dealer is None:
            dealer = 'p1'
        if tm_play_card_strategy is None:
            tm_play_card_strategy = {'t1': None, 't2': None}
        if tm_call_trump_strategy is None:
            tm_call_trump_strategy = {'t1': None, 't2': None}

        self.score = score
        self.dealer = dealer
        self.next_to_deal = next_to_deal
        self.hands_played = hands_played
        self.tm_play_card_strategy = tm_play_card_strategy
        self.tm_call_trump_strategy = tm_call_trump_strategy

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
        deck_of_cards = self.shuffle_deck_of_cards()
        rng = np.random.default_rng()
        numbers = rng.choice(21, size=21, replace=False)
        player_hands = {'p1': [deck_of_cards[numbers[i]] for i in range(0, 5)],
                        'p2': [deck_of_cards[numbers[i]] for i in range(5, 10)],
                        'p3': [deck_of_cards[numbers[i]] for i in range(10, 15)],
                        'p4': [deck_of_cards[numbers[i]] for i in range(15, 20)]}
        print_if_verbose(f'Player Hands: {player_hands}', verbose=verbose)
        print_if_verbose(f'Card flipped up: {deck_of_cards[numbers[20]]}', verbose=verbose)
        return player_hands, deck_of_cards[numbers[20]]

    def eval_flipped_card(self,
                          hand: list,
                          player: str,
                          card_flipped_up: str) -> bool:
        """
        Function to evaluate if a player will order up trump
        If hand has at least 3 trump cards

        :param hand: List of cards in player's hand
        :param player: PLayer
        :param card_flipped_up: Card flipped card to evaluate
        :returns True/False

        TODO: check player position, adjust strategy accordingly
        """
        suit = card_flipped_up[-1]
        # ALWAYS order up trump - this is insane
        if self.tm_call_trump_strategy[self.team_assignments[player]] == 'always':
            return True

        # # Never order up Jack if not dealer - this appears to be a bad strategy
        # if self.tm_call_trump_strategy[self.team_assignments[player]] == 'NEW':
        #     if player != self.dealer and card_flipped_up[0] == 'J':
        #         return False

        trumps = 0
        for card in hand:
            if card[-1] == suit:
                trumps += 1

        # pick up Jack if dealer and 2 trumps
        # if self.tm_call_trump_strategy[self.team_assignments[player]] == 'NEW':
        if player == self.dealer and card_flipped_up[0] == 'J' and trumps >= 2:
            return True

        # if 3 or more trumps
        if trumps >= 3:
            return True
        else:
            return False

    # TODO: pass in player/position/strategy to play
    def choose_open_trump(self,
                          hand: list,
                          player: str,
                          card_flipped_up: str) -> str:
        """
        Function to choose trump after card is turned down
        If hand has at least 3 trump cards

        :param hand: List of cards in player's hand
        :param player: PLayer
        :param card_flipped_up: Card flipped up
        :returns trump
        """
        suits_eligible = ['S', 'C', 'H', 'D']
        suits_eligible.remove(card_flipped_up[-1])
        if self.tm_call_trump_strategy[self.team_assignments[player]] == 'always':
            return suits_eligible[0]
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
        for idx, player in enumerate(self.next_to_deal):
            if self.eval_flipped_card(hand=player_hands[player],
                                      player=player,
                                      card_flipped_up=card_flipped_up):
                trump = card_flipped_up[-1]
                print_if_verbose(f'Player {player} in seat {idx+1} has chosen {trump} as trump', verbose=verbose)
                return player, trump
        for idx, player in enumerate(self.next_to_deal):
            trump = self.choose_open_trump(hand=player_hands[player],
                                           player=player,
                                           card_flipped_up=card_flipped_up)
            if trump is not None:
                print_if_verbose(f'Player {player} in seat {idx+1} has chosen {trump} as trump', verbose=verbose)
                return player, trump
        else:  # No "F the dealer"
            return None, None

    def play_lead_card(self,
                       hand,
                       trump,
                       cards_played_this_hand,
                       unplayed_trump_this_hand,
                       verbose=False):
        """
        Play lead card

        :param hand: List of cards in player's hand
        :param trump: Trump called this hand
        :param cards_played_this_hand: List of cards played in this hand so far
        :param unplayed_trump_this_hand: List of unplayed trump cards this hand
        :param verbose: True/False to print out log statements

        :return card to play
        """
        # print_if_verbose(f'Highest trump left: {unplayed_trump_this_hand[0]}', verbose=verbose, end='- ')

        if unplayed_trump_this_hand:  # if there are unplayed trump cards left
            if unplayed_trump_this_hand[0] in hand:  # always play highest trump card left
                print_if_verbose(f'Leading with highest trump card remaining', verbose=verbose, end='- ')
                # print_if_verbose(f'Trump cards remaining {unplayed_trump_this_hand}', verbose=verbose, end='- ')
                return unplayed_trump_this_hand[0]

        # TODO: check if opponents don't have any trump left, play any trump in hand

        # TODO: update this to be of suit least played so far in case of ties, or to partners short-suit
        # TODO: if highest_non_trump not A -> play into partner's short suit if exists
        # play highest non-trump
        highest_non_trump = get_highest_nontrump_card(hand=hand, trump=trump)
        if highest_non_trump is not None:
            print_if_verbose(f'Leading with highest non-trump', verbose=verbose, end='- ')
            return highest_non_trump
        else:  # only trump left in hand
            lowest_trump_card = get_lowest_trump_card(hand=hand, trump=trump)
            if lowest_trump_card is not None:
                print_if_verbose(f'Leading with lowest trump (only trump left)', verbose=verbose, end='- ')
                return lowest_trump_card

    def play_card(self,
                  player,
                  hand,
                  trump,
                  cards_in_play,
                  player_led,
                  cards_played_this_hand,
                  unplayed_trump_this_hand,
                  suit_led=None,
                  verbose=False):
        """
        Function to return card to play in hand

        :param player: Player to play card
        :param hand: List of cards in player's hand from which to play
        :param trump: Suit of trump this hand
        :param cards_in_play: Cards currently played this trick
        :param player_led: Player that led
        :param cards_played_this_hand: List of cards played in this hand so far
        :param unplayed_trump_this_hand: List of unplayed trump cards this hand
        :param suit_led: Suit led this trick
        :param verbose: True/False to print out log statements

        """
        # play last card
        if len(hand) == 1:
            print_if_verbose(f'Last card', verbose=verbose, end='- ')
            return hand[0]

        # lead card
        if len(cards_in_play) < 1:
            lead_card = self.play_lead_card(hand=hand,
                                            trump=trump,
                                            cards_played_this_hand=cards_played_this_hand,
                                            unplayed_trump_this_hand=unplayed_trump_this_hand,
                                            verbose=verbose)
            return lead_card

        # cards have been played this trick
        else:
            # check current winner is teammate or not
            current_winning_player = self.determine_trick_winner(cards_in_play=cards_in_play,
                                                                 trump=trump,
                                                                 player_led=player_led)
            print_if_verbose(f'Current winning player {current_winning_player}', verbose=verbose)

            # teammate winning
            if get_teammate(player) == current_winning_player:
                # trump led
                if suit_led == trump:
                    # play lowest trump card
                    lowest_trump_card = get_lowest_trump_card(hand=hand, trump=trump)
                    if lowest_trump_card is not None:
                        print_if_verbose(f'Teammate winning, following suit w/ lowest trump card', verbose=verbose, end='- ')
                        return lowest_trump_card
                    else:  # play card in hand with lowest chance of taking trick
                        lowest_card_in_hand = get_lowest_nontrump_card_in_hand(hand=hand,
                                                                               trump=trump,
                                                                               cards_played_this_hand=cards_played_this_hand,
                                                                               no_trump_in_hand=True)
                        print_if_verbose(f'Teammate winning, no trump, play lowest card', verbose=verbose, end='- ')
                        return lowest_card_in_hand
                else:  # trump not led
                    # play lowest card in suit led
                    lowest_card_in_suit = get_lowest_nontrump_card_in_suit(hand=hand, suit=suit_led)
                    if lowest_card_in_suit is not None:
                        print_if_verbose(f'Teammate winning, following suit w/ lowest card', verbose=verbose, end='- ')
                        return lowest_card_in_suit
                    else:  # play card in hand with lowest chance of taking trick
                        lowest_card_in_hand = get_lowest_nontrump_card_in_hand(hand=hand,
                                                                               trump=trump,
                                                                               cards_played_this_hand=cards_played_this_hand,
                                                                               no_trump_in_hand=False)
                        if lowest_card_in_hand is not None:
                            print_if_verbose(f'Teammate winning, no follow suit, play lowest card', verbose=verbose, end='- ')
                            return lowest_card_in_hand
                        else:  # only trump remaining
                            lowest_trump_card = get_lowest_trump_card(hand=hand, trump=trump)
                            print_if_verbose(f'Teammate winning, no follow suit, only trump left', verbose=verbose, end='- ')
                            return lowest_trump_card
            else:  # teammate not winning
                # trump led
                if suit_led == trump:
                    # TODO: check if player has a trump card that can win
                    # if player has card that can win:
                        # play lowest winning card
                    # else: play lowest trump card
                    lowest_trump_card = get_lowest_trump_card(hand=hand, trump=trump)
                    if lowest_trump_card is not None:
                        print_if_verbose(f'Following suit with lowest trump card', verbose=verbose, end='- ')
                        return lowest_trump_card
                    else:  # play card in hand with lowest chance of taking trick
                        lowest_card_in_hand = get_lowest_nontrump_card_in_hand(hand=hand,
                                                                               trump=trump,
                                                                               cards_played_this_hand=cards_played_this_hand,
                                                                               no_trump_in_hand=False)
                        print_if_verbose(f'No trump, playing lowest card in hand', verbose=verbose, end='- ')
                        return lowest_card_in_hand
                else:  # suit led not trump
                    # TODO: check if player has a card that can win
                    # TODO: BUG: left bauer trump cards are being played here
                    # play the lowest card in the suit played
                    lowest_card_in_suit = get_lowest_nontrump_card_in_suit(hand=hand, suit=suit_led)
                    if lowest_card_in_suit is not None:
                        print_if_verbose(f'Following suit with lowest non-trump card', verbose=verbose, end='- ')
                        return lowest_card_in_suit
                    # try to play lowest trump card
                    # TODO: check what trump cards have been played, if player can out-trump
                    lowest_trump_card = get_lowest_trump_card(hand=hand, trump=trump)
                    if lowest_trump_card is not None:
                        print_if_verbose(f'Lowest trump card', verbose=verbose, end='- ')
                        return lowest_trump_card
                    else:  # no trump, play off with the lowest card
                        lowest_card_in_hand = get_lowest_nontrump_card_in_hand(hand=hand,
                                                                               trump=trump,
                                                                               cards_played_this_hand=cards_played_this_hand,
                                                                               no_trump_in_hand=False)
                        print_if_verbose(f'No {suit_led}, no trump, playing lowest card in hand', verbose=verbose, end='- ')
                        return lowest_card_in_hand

    def play_trick(self,
                   player_hands,
                   trump,
                   next_to_play_list,
                   cards_played_this_hand,
                   unplayed_trump_this_hand,
                   verbose=False):
        """
        Function to play one full trick

        :param player_hands:
        :param trump: Trump called this hand
        :param next_to_play_list: List of players in order to play this trick
        :param cards_played_this_hand: List of all cards played this hand
        :param unplayed_trump_this_hand: List of unplayed trump cards this hand
        :param verbose: True/False to print out log statements
        :returns cards_in_play, player_led
        """
        cards_in_play = {}
        suit_led = None
        player_led = None
        for idx, player in enumerate(next_to_play_list):
            if self.tm_play_card_strategy[self.team_assignments[player]] == 'random':
                card_to_play = play_random_card(hand=player_hands[player],
                                                suit_led=suit_led)
            else:
                card_to_play = self.play_card(player=player,
                                              hand=player_hands[player],
                                              trump=trump,
                                              cards_in_play=cards_in_play,
                                              player_led=player_led,
                                              cards_played_this_hand=cards_played_this_hand,
                                              unplayed_trump_this_hand=unplayed_trump_this_hand,
                                              suit_led=suit_led,
                                              verbose=verbose)

            print_if_verbose(f'Player {player} plays {card_to_play}', verbose=verbose, end=', ')
            if card_to_play[-1] == trump:
                unplayed_trump_this_hand.remove(card_to_play)
            # add card_to_play
            cards_in_play[player] = card_to_play
            cards_played_this_hand.append(card_to_play)
            # update player hands after player has played card
            player_hands[player].remove(card_to_play)
            if len(cards_in_play) == 1:
                # switch suit led to trump for left bauer
                if return_off_suit(card_to_play[-1]) == trump and card_to_play[0] == 'J':
                    suit_led = trump
                else:
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
        # check if cards_in_play only has one card, return player that played that card
        if len(cards_in_play) == 1:
            return list(cards_in_play.keys())[0]

        # loop over trump cards, highest to lowest
        for trump_card in self.trump_hierarchy_dict[trump]:
            # if in cards_in_play:
            if trump_card in cards_in_play.values():
                # return player that played that card
                winning_player = [k for k, v in cards_in_play.items() if v == trump_card][0]
                print_if_verbose(f'{winning_player} wins trick', verbose=verbose)
                return winning_player
        led_suit = cards_in_play[player_led][-1]
        # TODO: rewrite this to not rely on dict key order
        for card_val in self.CARD_VALUES.keys():
            for card_played in cards_in_play.values():
                if card_played[0] == card_val and card_played[-1] == led_suit:
                    # return player that played that card
                    winning_player = [k for k, v in cards_in_play.items() if v == card_played][0]
                    print_if_verbose(f'{winning_player} wins trick', verbose=verbose)
                    return winning_player

    def update_score(self,
                     trick_winners,
                     calling_player,
                     is_loner=False,
                     verbose=False):
        """
        Update score for one hand given trick_winners and calling_player

        :param trick_winners: Dict with counts of number of tricks won per player
        :param calling_player: Player that called trump this hand
        :param verbose: True/False to print out log statements
        :param is_loner: True/False if player went alone
        :returns None
        """
        t1_tricks = trick_winners['p1'] + trick_winners['p3']
        t2_tricks = trick_winners['p2'] + trick_winners['p4']
        hand_score = {'t1': 0, 't2': 0}
        if calling_player in ['p1', 'p3']:
            if not is_loner:
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
            else:
                if t1_tricks in [3, 4]:
                    self.score['t1'] += 1
                    hand_score = {'t1': 1, 't2': 0}
                    print_if_verbose(f't1 scores 1', verbose=verbose)
                elif t1_tricks == 5:
                    self.score['t1'] += 4
                    hand_score = {'t1': 4, 't2': 0}
                    print_if_verbose(f't1 scores 4', verbose=verbose)
                else:
                    self.score['t2'] += 2
                    hand_score = {'t1': 0, 't2': 2}
                    print_if_verbose(f't2 scores 2', verbose=verbose)
        if calling_player in ['p2', 'p4']:
            if not is_loner:
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
            else:
                if t2_tricks in [3, 4]:
                    self.score['t2'] += 1
                    hand_score = {'t1': 0, 't2': 1}
                    print_if_verbose(f't2 scores 1', verbose=verbose)
                elif t2_tricks == 5:
                    self.score['t2'] += 4
                    hand_score = {'t1': 0, 't2': 4}
                    print_if_verbose(f't2 scores 4', verbose=verbose)
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

    def play_hand(self,
                  verbose=False):
        """
        Function to play a single hand
        Applies deal_hand and determine_trump functions, then loops through play_trick 5 times and updates scores

        :param verbose: True/False to print out log statements
        :returns hand_results dict

        """
        trump_hierarchy_dict = {
            'D': ['J_D', 'J_H', 'A_D', 'K_D', 'Q_D', 'T_D', '9_D'],
            'H': ['J_H', 'J_D', 'A_H', 'K_H', 'Q_H', 'T_H', '9_H'],
            'C': ['J_C', 'J_S', 'A_C', 'K_C', 'Q_C', 'T_C', '9_C'],
            'S': ['J_S', 'J_C', 'A_S', 'K_S', 'Q_S', 'T_S', '9_S']
        }
        hand_results = {}
        # deal cards
        player_hands, card_flipped_up = self.deal_hand(verbose=verbose)

        hand_results['player_hands'] = copy.deepcopy(player_hands)
        # choose trump
        calling_player, trump = self.determine_trump(card_flipped_up=card_flipped_up, player_hands=player_hands,
                                                     verbose=verbose)

        if trump is not None:
            if card_flipped_up[-1] == trump:
                swap_dealer_card(card_flipped_up=card_flipped_up, dealer_hand=player_hands[self.dealer],
                                 verbose=verbose)
            hand_results['calling_player'] = calling_player
            hand_results['trump'] = trump
            hand_results['dealer'] = self.dealer
            trick_winners = {p: 0 for p in self.next_to_deal}
            next_to_play_list = self.next_to_deal
            cards_played_this_hand = []
            unplayed_trump_this_hand = trump_hierarchy_dict[trump]
            for trick in range(5):
                print_if_verbose(f'Trick {trick}', verbose=verbose, end=': ')
                cards_in_play, player_led = self.play_trick(player_hands=player_hands,
                                                            trump=trump,
                                                            next_to_play_list=next_to_play_list,
                                                            cards_played_this_hand=cards_played_this_hand,
                                                            unplayed_trump_this_hand=unplayed_trump_this_hand,
                                                            verbose=verbose)
                trick_winner = self.determine_trick_winner(cards_in_play=cards_in_play,
                                                           trump=trump,
                                                           player_led=player_led,
                                                           verbose=verbose)
                trick_winners[trick_winner] += 1
                next_to_play_list = self.get_next_trick_order(trick_winner)
                print_if_verbose(f'Cards played this hand list {cards_played_this_hand}', verbose=verbose)
            print_if_verbose(f'Trick winners: {trick_winners}', verbose=verbose)

            # update score
            hand_score = self.update_score(trick_winners=trick_winners, calling_player=calling_player, verbose=verbose)
            hand_results['hand_score'] = hand_score

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
