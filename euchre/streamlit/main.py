"""

Streamlit main file

Streamlit docs links:
https://docs.streamlit.io/library/get-started/main-concepts
https://docs.streamlit.io/library/cheatsheet
https://docs.streamlit.io/knowledge-base/using-streamlit/batch-elements-input-widgets-form
https://docs.streamlit.io/library/api-reference/session-state

"""


import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sys
import joblib

sys.path.insert(0, 'C:/Users/jerem/Desktop/nonsense/euchre')
# from utils import *


def bar_chart(expected_tricks_taken):
    num_tricks_taken = ['0 - zero', '1 - one', '2 - two', '3 - three', '4 - four', '5 - five']
    fig = plt.figure(figsize = (10, 5))
    plt.bar(num_tricks_taken, expected_tricks_taken)
    plt.xlabel("Tricks taken")
    plt.ylabel("Percent of hands")
    plt.title("Expected tricks taken")
    st.pyplot(fig)


def main():
    """
    Main function to run streamlit app

    :return: None
    """

    # Header
    st.markdown(f"""# Euchre Hand Evaluator""")

    with st.form(key='hand_cards_form'):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("SPADES")
            a_s = st.checkbox(label='A_S', value=False)
            k_s = st.checkbox(label='K_S', value=False)
            q_s = st.checkbox(label='Q_S', value=False)
            j_s = st.checkbox(label='J_S', value=False)
            t_s = st.checkbox(label='T_S', value=False)
            nine_s = st.checkbox(label='9_S', value=False)

        with col2:
            st.header("CLUBS")
            a_c = st.checkbox(label='A_C', value=False)
            k_c = st.checkbox(label='K_C', value=False)
            q_c = st.checkbox(label='Q_C', value=False)
            j_c = st.checkbox(label='J_C', value=False)
            t_c = st.checkbox(label='T_C', value=False)
            nine_c = st.checkbox(label='9_C', value=False)

        with col3:
            st.header("HEARTS")
            a_h = st.checkbox(label='A_H', value=False)
            k_h = st.checkbox(label='K_H', value=False)
            q_h = st.checkbox(label='Q_H', value=False)
            j_h = st.checkbox(label='J_H', value=False)
            t_h = st.checkbox(label='T_H', value=False)
            nine_h = st.checkbox(label='9_H', value=False)

        with col4:
            st.header("DIAMONDS")
            a_d = st.checkbox(label='A_D', value=False)
            k_d = st.checkbox(label='K_D', value=False)
            q_d = st.checkbox(label='Q_D', value=False)
            j_d = st.checkbox(label='J_D', value=False)
            t_d = st.checkbox(label='T_D', value=False)
            nine_d = st.checkbox(label='9_D', value=False)

        select_trump = st.selectbox(label='Suit of trump',
                                    options=['SPADES', 'CLUBS', 'HEARTS', 'DIAMONDS'],
                                    index=0)
        player_position = st.radio(label='Player Table Position (order on first trick)',
                                   options=['1', '2', '3', '4'])

        submit_button = st.form_submit_button(label='Evaluate Hand')

    if submit_button:
        st.text(f'Trump chosen: {select_trump}; Player table position: {player_position}')
        if k_s:
            st.text('K_S')

        model_features = ['has_right', 'has_left',
                          'has_Atrump', 'has_Ktrump', 'has_Qtrump', 'has_Ttrump', 'has_9trump',
                          'num_off_A', 'num_off_K', 'num_off_Q'
                          ]
        hand = {feature: [0] for feature in model_features}
        single_hand_test_df = pd.DataFrame(hand)
        single_hand_test_df['has_right'] = 0
        single_hand_test_df['has_left'] = 0
        single_hand_test_df['num_off_Q'] = 1
        single_hand_test_df['num_off_K'] = 0
        single_hand_test_df['num_off_A'] = 2
        model = joblib.load('C:/Users/jerem/Desktop/nonsense/euchre/models/trick_model_rf_v0.sav')
        single_hand_preds = model.predict_proba(single_hand_test_df)

        st.text(single_hand_preds)

        bar_chart(expected_tricks_taken=single_hand_preds.tolist()[0])

    # DEV MODE - check current session state
    # st.write(f'Session State: {st.session_state}')


if __name__ == '__main__':
    try:
        main()

    except Exception as err:
        raise err
