
# init file

CARD_VALUES = {
    'A': 6,
    'K': 5,
    'Q': 4,
    'J': 3,
    'T': 2,
    '9': 1,
}

TRUMP_HIERARCHY_DICT = {
    'D': ['J_D', 'J_H', 'A_D', 'K_D', 'Q_D', 'T_D', '9_D'],
    'H': ['J_H', 'J_D', 'A_H', 'K_H', 'Q_H', 'T_H', '9_H'],
    'C': ['J_C', 'J_S', 'A_C', 'K_C', 'Q_C', 'T_C', '9_C'],
    'S': ['J_S', 'J_C', 'A_S', 'K_S', 'Q_S', 'T_S', '9_S']
}

TEAM_ASSIGNMENTS = {
    'p1': 't1',
    'p2': 't2',
    'p3': 't1',
    'p4': 't2',
}
