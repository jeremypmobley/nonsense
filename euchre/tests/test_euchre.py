
# TESTS
import pytest
from utils.utils import get_teammate
from utils.utils import return_off_suit
from utils.utils import EuchreGame


def test_get_teammate():
    assert get_teammate('p2') == 'p4'
    assert get_teammate('p4') == 'p2'
    assert get_teammate('p1') == 'p3'


def test_return_off_suit():
    assert return_off_suit('H') == 'D'


@pytest.fixture
def my_game():
    return EuchreGame()


def test_shuffle_deck_of_cards(my_game):
    result = my_game.shuffle_deck_of_cards()
    assert len(result) == 24


def test_deal_hand(my_game):
    player_hands, card_flipped_up = my_game.deal_hand()
    assert len(player_hands) == 4
    assert len(card_flipped_up) == 3
