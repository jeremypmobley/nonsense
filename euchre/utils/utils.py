
import copy
from utils.strategy_utils import play_random_card
from utils import CARD_VALUES, TRUMP_HIERARCHY_DICT, TEAM_ASSIGNMENTS
import random


def print_if_verbose(thing_to_print, verbose=False, **kwargs):
    """ Function to print if verbose is True """
    if verbose:
        print(thing_to_print, **kwargs)


def return_off_suit(suit: str) -> str:
    """
    Function to return off-suit given suit
    :param: suit
    :returns suit
    """
    suit_mapping = {'H': 'D', 'D': 'H', 'C': 'S', 'S': 'C'}
    return suit_mapping.get(suit, suit)


def is_card_trump(card: str,
                  trump: str):
    """
    Function to return if given card is trump
    :param: card
    :param: trump
    :returns True/False
    """
    if card[-1] == trump:
        return True
    elif return_off_suit(card[-1]) == trump and card[0] == 'J':
        return True
    else:
        return False


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


def get_highest_nontrump_card(hand: list,
                              trump: str,
                              suit: str = None):
    """
    Return highest non-trump card in hand across all suits or in given suit

    :return card
    """
    card_to_play_points = -1
    idx_to_return = None
    for idx, card in enumerate(hand):
        if is_card_trump(card=card, trump=trump):
            continue
        card_points = CARD_VALUES[card[0]]
        if suit is not None:
            if card[-1] == suit and card_points > card_to_play_points:
                card_to_play_points = card_points
                idx_to_return = idx
        else:
            if card_points > card_to_play_points:
                card_to_play_points = card_points
                idx_to_return = idx
    if idx_to_return is not None:
        return hand[idx_to_return]


def get_lowest_trump_card(hand: list, trump: str):
    """
    Function to return lowest trump card in hand
    Returns None if no trump cards found
    """
    trump_cards = copy.deepcopy(TRUMP_HIERARCHY_DICT[trump])
    reverse_trump_cards = reversed(trump_cards)
    for card in reverse_trump_cards:
        if card in hand:
            return card


def get_lowest_nontrump_card_in_suit(hand: list,
                                     suit: str,
                                     trump: str):
    """
    Function to return lowest non-trump card in suit from given hand
    Returns None if no cards found in suit
    """
    card_to_play_points = 9
    idx_to_return = None
    for idx, card in enumerate(hand):
        # if card[-1] == trump or (return_off_suit(card[-1]) == trump and card[0] == 'J'):
        if is_card_trump(card=card, trump=trump):
            continue
        if card[-1] == suit:  # if card is in given suit
            card_points = CARD_VALUES[card[0]]
            if card_points < card_to_play_points:
                card_to_play_points = card_points
                idx_to_return = idx
    if idx_to_return is not None:
        return hand[idx_to_return]


def get_lowest_nontrump_card_in_hand(hand: list,
                                     trump: str,
                                     cards_played_this_hand: list,
                                     no_trump_in_hand=False):
    """
    Function to return the lowest nontrump card overall in hand
    Return None if only trump cards remain in hand - must pass in no_trump_in_hand
    Returns card
    """
    if no_trump_in_hand:  # play card that can take fewest other cards
        idx_to_return = 0
        fewest_lower_cards = 6
        for idx, card in enumerate(hand):
            lower_cards = CARD_VALUES[card[0]]
            if lower_cards == 0:  # return nontrump 9 immediately
                return card
            for played_card in cards_played_this_hand:
                if played_card[-1] == trump or (return_off_suit(played_card[-1]) == trump and played_card[0] == 'J'):
                    continue
                if card[-1] == played_card[-1] and CARD_VALUES[card[0]] > CARD_VALUES[played_card[0]]:
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
            if is_card_trump(card=card, trump=trump):
                num_trumps += 1

        if num_trumps == len(hand):  # only trump left
            return None

        if num_trumps > 0 and len(hand) > 2:  # if trump in hand, short suit
            # get suit counts
            suit_counts = {}
            for card in hand:
                if is_card_trump(card=card, trump=trump):  # don't count trump
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
                        card_points = CARD_VALUES[card[0]]
                        if card_points < card_to_play_points:
                            card_to_play_points = card_points
                            idx_to_return = idx
                suit_to_play = hand[idx_to_return][-1]
            else:
                suit_to_play = short_suits[0]
            return get_lowest_nontrump_card_in_suit(hand=hand, suit=suit_to_play, trump=trump)

        else:  # play card that can take fewest other cards
            idx_to_return = 0
            fewest_lower_cards = 6
            for idx, card in enumerate(hand):
                if is_card_trump(card=card, trump=trump):  # don't play trump
                    continue
                lower_cards = CARD_VALUES[card[0]]
                if lower_cards == 0:  # return nontrump 9 immediately
                    return card
                for played_card in cards_played_this_hand:
                    if played_card[-1] == trump or (
                            return_off_suit(played_card[-1]) == trump and played_card[0] == 'J'):
                        continue
                    if card[-1] == played_card[-1] and CARD_VALUES[card[0]] > CARD_VALUES[played_card[0]]:
                        lower_cards -= 1
                if lower_cards == 0:  # return nontrump card with no lower cards immediately
                    return card
                if lower_cards < fewest_lower_cards:
                    fewest_lower_cards = lower_cards
                    idx_to_return = idx
            return hand[idx_to_return]


def get_lowest_winning_trump_card(hand: list,
                                  cards_in_play: dict,
                                  trump: str):
    """
    Function to find the lowest winning trump card

    :param hand: list
    :param cards_in_play:
    :param trump:

    :return: card
    """
    # find highest current trump card played
    highest_current_trump = None
    for card in TRUMP_HIERARCHY_DICT[trump]:
        if card in cards_in_play.values():
            highest_current_trump = card
            break
    if highest_current_trump is None:  # no trump cards have been played
        return get_lowest_trump_card(hand=hand, trump=trump)
    else:  # figure out if cards in hand are higher than highest_trump_card
        winning_trump_cards = []
        highest_current_trump_wins = True
        for card in TRUMP_HIERARCHY_DICT[trump]:
            if card == highest_current_trump and highest_current_trump_wins:
                return None
            if card in hand:
                winning_trump_cards.append(card)
                highest_current_trump_wins = False
        if winning_trump_cards:
            return winning_trump_cards[-1]
        else:
            return None


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
                card_points = CARD_VALUES[card[0]]
                if card_points < card_to_play_points:
                    card_to_play_points = card_points
                    idx_to_return = idx
        suit_to_play = dealer_hand[idx_to_return][-1]
    else:
        suit_to_play = short_suits[0]

    # find the lowest nontrump card in suit to short
    removed_card = get_lowest_nontrump_card_in_suit(hand=dealer_hand, suit=suit_to_play, trump=card_flipped_up[-1])

    dealer_hand.remove(removed_card)
    dealer_hand.append(card_flipped_up)
    print_if_verbose(f'Dealer discards {removed_card} and picks up {card_flipped_up}', verbose=verbose)
    return dealer_hand


def eval_flipped_card(hand: list,
                      player: str,
                      dealer: str,
                      card_flipped_up: str) -> bool:
    """
    Function to evaluate if a player will order up trump
    If hand has at least 3 trump cards

    :param hand: List of cards in player's hand
    :param player: Player
    :param dealer: Dealer of hand
    :param card_flipped_up: Card flipped card to evaluate
    :returns True/False

    TODO: check player position, adjust strategy accordingly
    TODO: assess dealer hand with card_flipped up in it
    """
    suit = card_flipped_up[-1]

    trumps = 0
    for card in hand:
        if card[-1] == suit:
            trumps += 1

    # pick up Jack if dealer and 2 trumps
    if player == dealer and card_flipped_up[0] == 'J' and trumps >= 2:
        return True

    # if 3 or more trumps
    return trumps >= 3


def choose_open_trump(hand: list,
                      card_flipped_up: str) -> str:
    """
    Function to choose trump after card is turned down
    If hand has at least 3 trump cards

    :param hand: List of cards in player's hand
    :param card_flipped_up: Card flipped up
    :returns trump
    """
    # TODO: pass in player/position/strategy to play

    suits_eligible = ['S', 'C', 'H', 'D']
    suits_eligible.remove(card_flipped_up[-1])
    for suit in suits_eligible:
        trumps = 0
        for card in hand:
            if card[-1] == suit:
                trumps += 1
        if trumps >= 3:
            return suit


def play_lead_card(hand,
                   trump,
                   cards_played_this_hand,
                   verbose=False):
    """
    Play lead card

    :param hand: List of cards in player's hand
    :param trump: Trump called this hand
    :param cards_played_this_hand: List of cards played in this hand so far
    :param verbose: True/False to print out log statements

    :return card to play
    """
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


def determine_trick_winner(cards_in_play,
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
    for trump_card in TRUMP_HIERARCHY_DICT[trump]:
        # if in cards_in_play:
        if trump_card in cards_in_play.values():
            # return player that played that card
            winning_player = [k for k, v in cards_in_play.items() if v == trump_card][0]
            print_if_verbose(f'{winning_player} wins trick', verbose=verbose)
            return winning_player
    led_suit = cards_in_play[player_led][-1]
    for card_val in CARD_VALUES.keys():
        for card_played in cards_in_play.values():
            if card_played[0] == card_val and card_played[-1] == led_suit:
                # return player that played that card
                winning_player = [k for k, v in cards_in_play.items() if v == card_played][0]
                print_if_verbose(f'{winning_player} wins trick', verbose=verbose)
                return winning_player


class EuchreGame:
    """
    Main class for euchre game
    """
    def __init__(self,
                 score=None,
                 dealer=None,
                 next_to_deal=None,
                 tm_play_card_strategy=None,
                 hands_played=0):
        if next_to_deal is None:
            next_to_deal = ['p2', 'p3', 'p4', 'p1']
        if score is None:
            score = {'t1': 0, 't2': 0}
        if dealer is None:
            dealer = 'p1'
        if tm_play_card_strategy is None:
            tm_play_card_strategy = {'t1': None, 't2': None}

        self.score = score
        self.dealer = dealer
        self.next_to_deal = next_to_deal
        self.hands_played = hands_played
        self.tm_play_card_strategy = tm_play_card_strategy

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
            if eval_flipped_card(hand=player_hands[player],
                                 player=player,
                                 dealer=self.dealer,
                                 card_flipped_up=card_flipped_up):
                trump = card_flipped_up[-1]
                print_if_verbose(f'Player {player} in seat {idx+1} has chosen {trump} as trump', verbose=verbose)
                return player, trump
        for idx, player in enumerate(self.next_to_deal):
            trump = choose_open_trump(hand=player_hands[player],
                                      card_flipped_up=card_flipped_up)
            if trump is not None:
                print_if_verbose(f'Player {player} in seat {idx+1} has chosen {trump} as trump', verbose=verbose)
                return player, trump
        else:  # No "F the dealer"
            return None, None

    def play_card(self,
                  player,
                  hand,
                  trump,
                  cards_in_play,
                  player_led,
                  cards_played_this_hand,
                  verbose=False):
        """
        Function to return card to play in hand

        :param player: Player to play card
        :param hand: List of cards in player's hand from which to play
        :param trump: Suit of trump this hand
        :param cards_in_play: Cards currently played this trick
        :param player_led: Player that led
        :param cards_played_this_hand: List of cards played in this hand so far
        :param verbose: True/False to print out log statements

        """
        # play last card
        if len(hand) == 1:
            print_if_verbose(f'Last card', verbose=verbose, end='- ')
            return hand[0]

        # lead card
        if len(cards_in_play) < 1:
            lead_card = play_lead_card(hand=hand,
                                       trump=trump,
                                       cards_played_this_hand=cards_played_this_hand,
                                       verbose=verbose)
            return lead_card

        # cards have been played this trick
        else:
            if return_off_suit(cards_in_play[player_led][-1]) == trump and cards_in_play[player_led][0] == 'J':
                suit_led = trump
            else:
                suit_led = cards_in_play[player_led][-1]
            # check current winner is teammate or not
            print_if_verbose(f'Cards in play: {cards_in_play}', verbose=verbose)
            current_winning_player = determine_trick_winner(cards_in_play=cards_in_play,
                                                            trump=trump,
                                                            player_led=player_led)
            # print_if_verbose(f'Current winning player {current_winning_player}', verbose=verbose)

            # teammate winning
            if TEAM_ASSIGNMENTS[player] == TEAM_ASSIGNMENTS[current_winning_player]:

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
                    # TODO: check likelihood that teammate will win trick with current card, maybe overtake partner
                    lowest_card_in_suit = get_lowest_nontrump_card_in_suit(hand=hand, suit=suit_led, trump=trump)
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
                    # check if player has a trump card that can win
                    lowest_winning_trump_card = get_lowest_winning_trump_card(hand=hand,
                                                                              cards_in_play=cards_in_play,
                                                                              trump=trump)
                    if lowest_winning_trump_card is not None:
                        print_if_verbose(f'Following suit with lowest winning trump card', verbose=verbose, end='- ')
                        return lowest_winning_trump_card
                    # else: play lowest trump card
                    lowest_trump_card = get_lowest_trump_card(hand=hand, trump=trump)
                    if lowest_trump_card is not None:
                        print_if_verbose(f'Following suit with lowest trump card', verbose=verbose, end='- ')
                        return lowest_trump_card
                    else:  # no trump, play card in hand with lowest chance of taking trick later
                        lowest_card_in_hand = get_lowest_nontrump_card_in_hand(hand=hand,
                                                                               trump=trump,
                                                                               cards_played_this_hand=cards_played_this_hand,
                                                                               no_trump_in_hand=False)
                        print_if_verbose(f'No trump, playing lowest card in hand', verbose=verbose, end='- ')
                        return lowest_card_in_hand
                else:  # suit led not trump
                    # TODO: check if trump has been played
                    # TODO: check if player has a card that can win, if not play lowest card
                    # play the highest card in the suit led
                    highest_nontrump_card = get_highest_nontrump_card(hand=hand, trump=trump, suit=suit_led)
                    if highest_nontrump_card is not None:
                        print_if_verbose(f'Following suit with highest card', verbose=verbose, end='- ')
                        return highest_nontrump_card
                    # play the lowest card in the suit led
                    lowest_card_in_suit = get_lowest_nontrump_card_in_suit(hand=hand, suit=suit_led, trump=trump)
                    if lowest_card_in_suit is not None:
                        print_if_verbose(f'Following suit with lowest card', verbose=verbose, end='- ')
                        return lowest_card_in_suit
                    # check if player has a trump card that can win
                    lowest_winning_trump_card = get_lowest_winning_trump_card(hand=hand,
                                                                              cards_in_play=cards_in_play,
                                                                              trump=trump)
                    if lowest_winning_trump_card is not None:
                        print_if_verbose(f'Lowest winning trump card', verbose=verbose, end='- ')
                        return lowest_winning_trump_card

                    else:  # no winning trump, play off with the lowest card
                        lowest_card_in_hand = get_lowest_nontrump_card_in_hand(hand=hand,
                                                                               trump=trump,
                                                                               cards_played_this_hand=cards_played_this_hand,
                                                                               no_trump_in_hand=True)
                        if lowest_card_in_hand is not None:
                            print_if_verbose(f'No {suit_led}, no trump, playing lowest card in hand',
                                             verbose=verbose, end='- ')
                            return lowest_card_in_hand
                        else:  # play lowest trump card
                            lowest_trump_card = get_lowest_trump_card(hand=hand, trump=trump)
                            print_if_verbose(f'Playing lowest losing trump card', verbose=verbose, end='- ')
                            return lowest_trump_card

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
        player_led = None
        for idx, player in enumerate(next_to_play_list):
            if self.tm_play_card_strategy[TEAM_ASSIGNMENTS[player]] == 'random':
                card_to_play = play_random_card(hand=player_hands[player],
                                                cards_in_play=cards_in_play,
                                                player_led=player_led,
                                                trump=trump)
            else:
                card_to_play = self.play_card(player=player,
                                              hand=player_hands[player],
                                              trump=trump,
                                              cards_in_play=cards_in_play,
                                              player_led=player_led,
                                              cards_played_this_hand=cards_played_this_hand,
                                              verbose=verbose)

            print_if_verbose(f'Player {player} plays {card_to_play}', verbose=verbose, end=', ')
            # add card_to_play
            cards_in_play[player] = card_to_play
            cards_played_this_hand.append(card_to_play)
            # update player hands after player has played card
            player_hands[player].remove(card_to_play)
            # set player_led after first card played
            if len(cards_in_play) == 1:
                player_led = player
        return cards_in_play, player_led

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

    def play_full_game(self,
                       return_all_hands_results=False,
                       verbose=False):
        """
        Play full game
        """

        all_hand_results = []
        while self.score['t1'] < 10 and self.score['t2'] < 10:
            print_if_verbose(f'Hand #{self.hands_played}- Dealer: {self.dealer}', verbose=verbose, end='; ')
            # hand_results = self.play_hand(verbose=verbose)
            hand_results = Hand(game=self, verbose=verbose).play_hand()
            if hand_results is not None:
                all_hand_results.append(hand_results)
                self.hands_played += 1
        print_if_verbose(f'Total hands played {self.hands_played}', verbose=verbose)
        if return_all_hands_results:
            return all_hand_results


class Hand:
    def __init__(self, game, verbose):
        self.hand_results = {}
        self.game = game
        self.verbose = verbose

    def play_hand(self):
        my_deck = Deck()
        my_deck.shuffle()
        player_hands, card_flipped_up = my_deck.deal_hand()

        self.hand_results['player_hands'] = copy.deepcopy(player_hands)
        # choose trump
        calling_player, trump = self.game.determine_trump(card_flipped_up=card_flipped_up, player_hands=player_hands,
                                                          verbose=self.verbose)

        if trump is not None:
            if card_flipped_up[-1] == trump:
                swap_dealer_card(card_flipped_up=card_flipped_up, dealer_hand=player_hands[self.game.dealer],
                                 verbose=self.verbose)
            self.hand_results['calling_player'] = calling_player
            self.hand_results['card_flipped_up'] = card_flipped_up
            self.hand_results['trump'] = trump
            self.hand_results['dealer'] = self.game.dealer
            self.hand_results['next_to_deal'] = self.game.next_to_deal
            trick_winners = {p: 0 for p in self.game.next_to_deal}
            next_to_play_list = self.game.next_to_deal
            cards_played_this_hand = []
            for trick in range(5):
                print_if_verbose(f'Trick {trick}', verbose=self.verbose, end=': ')
                cards_in_play, player_led = self.game.play_trick(player_hands=player_hands,
                                                                 trump=trump,
                                                                 next_to_play_list=next_to_play_list,
                                                                 cards_played_this_hand=cards_played_this_hand,
                                                                 verbose=self.verbose)
                trick_winner = determine_trick_winner(cards_in_play=cards_in_play,
                                                      trump=trump,
                                                      player_led=player_led,
                                                      verbose=self.verbose)
                trick_winners[trick_winner] += 1
                next_to_play_list = get_next_trick_order(trick_winner)
            print_if_verbose(f'Trick winners: {trick_winners}', verbose=self.verbose, end=' - ')

            # update score
            hand_score = self.game.update_score(trick_winners=trick_winners,
                                                calling_player=calling_player,
                                                verbose=self.verbose)
            self.hand_results['hand_score'] = hand_score

            self.game.dealer = self.game.next_to_deal.pop(0)
            self.game.next_to_deal.append(self.game.dealer)
            self.hand_results['trick_winners'] = trick_winners
            return self.hand_results
        else:
            print_if_verbose('Trump not found', verbose=self.verbose)
            self.game.dealer = self.game.next_to_deal.pop(0)
            self.game.next_to_deal.append(self.game.dealer)
            return None


class Deck:
    def __init__(self):
        suits = ['S', 'C', 'H', 'D']
        values = ['9', 'T', 'J', 'Q', 'K', 'A']
        self.cards = [value + '_' + suit for value in values for suit in suits]

    def shuffle(self):
        return random.shuffle(self.cards)

    def deal_hand(self):
        """
        Function to deal cards for hand
        :returns player_hands dict, card_flipped_up
        """
        deck_of_cards = self.cards
        player_hands = {'p1': [deck_of_cards[i] for i in range(0, 5)],
                        'p2': [deck_of_cards[i] for i in range(5, 10)],
                        'p3': [deck_of_cards[i] for i in range(10, 15)],
                        'p4': [deck_of_cards[i] for i in range(15, 20)]}
        return player_hands, deck_of_cards[20]
