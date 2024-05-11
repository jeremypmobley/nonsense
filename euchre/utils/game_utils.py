
# General game utility functions


def return_off_suit(suit: str) -> str:
    """
    Function to return off-suit given suit
    :param: suit
    :returns suit
    """
    suit_mapping = {'H': 'D', 'D': 'H', 'C': 'S', 'S': 'C'}
    return suit_mapping.get(suit, suit)

