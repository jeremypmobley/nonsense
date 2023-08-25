
import pandas as pd


def translate_st_input_to_df(trump,
                             a_s=False, k_s=False, q_s=False, j_s=False, t_s=False, nine_s=False,
                             a_c=False, k_c=False, q_c=False, j_c=False, t_c=False, nine_c=False,
                             a_d=False, k_d=False, q_d=False, j_d=False, t_d=False, nine_d=False,
                             a_h=False, k_h=False, q_h=False, j_h=False, t_h=False, nine_h=False):
    """
    Function to take in checkbox inputs and return dataframe used in modeling

    :return dataframe
    """
    model_features = ['has_right', 'has_left',
                      'has_Atrump', 'has_Ktrump', 'has_Qtrump', 'has_Ttrump', 'has_9trump',
                      'num_off_A', 'num_off_K', 'num_off_Q'
                      ]
    hand = {feature: [0] for feature in model_features}
    df = pd.DataFrame(hand)
    if trump == 'SPADES':
        if a_s:
            df['has_Atrump'] = 1
        if k_s:
            df['has_Ktrump'] = 1
        if q_s:
            df['has_Qtrump'] = 1
        if j_s:
            df['has_right'] = 1
        if t_s:
            df['has_Ttrump'] = 1
        if nine_s:
            df['has_9trump'] = 1
        if j_c:
            df['has_left'] = 1

    if trump == 'CLUBS':
        if a_c:
            df['has_Atrump'] = 1
        if k_c:
            df['has_Ktrump'] = 1
        if q_c:
            df['has_Qtrump'] = 1
        if j_c:
            df['has_right'] = 1
        if t_c:
            df['has_Ttrump'] = 1
        if nine_c:
            df['has_9trump'] = 1
        if j_s:
            df['has_left'] = 1

    if trump == 'DIAMONDS':
        if a_d:
            df['has_Atrump'] = 1
        if k_d:
            df['has_Ktrump'] = 1
        if q_d:
            df['has_Qtrump'] = 1
        if j_d:
            df['has_right'] = 1
        if t_d:
            df['has_Ttrump'] = 1
        if nine_d:
            df['has_9trump'] = 1
        if j_h:
            df['has_left'] = 1

    if trump == 'HEARTS':
        if a_h:
            df['has_Atrump'] = 1
        if k_h:
            df['has_Ktrump'] = 1
        if q_h:
            df['has_Qtrump'] = 1
        if j_h:
            df['has_right'] = 1
        if t_h:
            df['has_Ttrump'] = 1
        if nine_h:
            df['has_9trump'] = 1
        if j_d:
            df['has_left'] = 1

    return df


def count_suits_st_input(trump: str,
                         a_s=False, k_s=False, q_s=False, j_s=False, t_s=False, nine_s=False,
                         a_c=False, k_c=False, q_c=False, j_c=False, t_c=False, nine_c=False,
                         a_d=False, k_d=False, q_d=False, j_d=False, t_d=False, nine_d=False,
                         a_h=False, k_h=False, q_h=False, j_h=False, t_h=False, nine_h=False):
    """
    :return int of number of suits
    """
    suits = set()
    if trump == 'HEARTS':
        if a_h or k_h or q_h or j_h or j_d or t_h or nine_h:
            suits.add('h')
        if a_d or k_d or q_d or t_d or nine_d:
            suits.add('d')
        if a_s or k_s or q_s or j_s or t_s or nine_s:
            suits.add('s')
        if a_c or k_c or q_c or j_c or t_c or nine_c:
            suits.add('c')
    if trump == 'SPADES':
        if a_h or k_h or q_h or j_h or t_h or nine_h:
            suits.add('h')
        if a_d or k_d or q_d or j_d or t_d or nine_d:
            suits.add('d')
        if a_s or k_s or q_s or j_s or j_c or t_s or nine_s:
            suits.add('s')
        if a_c or k_c or q_c or t_c or nine_c:
            suits.add('c')
    if trump == 'CLUBS':
        if a_h or k_h or q_h or j_h or t_h or nine_h:
            suits.add('h')
        if a_d or k_d or q_d or j_d or t_d or nine_d:
            suits.add('d')
        if a_s or k_s or q_s or t_s or nine_s:
            suits.add('s')
        if a_c or k_c or q_c or j_c or j_s or t_c or nine_c:
            suits.add('c')
    if trump == 'DIAMONDS':
        if a_h or k_h or q_h or t_h or nine_h:
            suits.add('h')
        if a_d or k_d or q_d or j_d or j_h or t_d or nine_d:
            suits.add('d')
        if a_s or k_s or q_s or j_s or t_s or nine_s:
            suits.add('s')
        if a_c or k_c or q_c or j_c or t_c or nine_c:
            suits.add('c')
    return len(suits)