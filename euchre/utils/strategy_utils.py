
import numpy as np
# from utils.utils import return_off_suit
# from utils import return_off_suit
# from . import return_off_suit
from .game_utils import return_off_suit


def play_random_card(hand: list,
                     cards_in_play: dict,
                     player_led: str,
                     trump: str):
    """
    Function to play random card from hand

    :returns card
    """
    if len(hand) == 1:  # last card in hand, play it
        return hand[0]
    if len(cards_in_play) == 0:  # no cards played yet, play any one
        return np.random.choice(hand)
    else:
        if return_off_suit(cards_in_play[player_led][-1]) == trump and cards_in_play[player_led][0] == 'J':
            suit_led = trump
        else:
            suit_led = cards_in_play[player_led][-1]
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

