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
import joblib
from streamlit_utils import translate_st_input_to_df, count_suits_st_input


def bar_chart(expected_tricks_taken):
    num_tricks_taken = ['0 - zero', '1 - one', '2 - two', '3 - three', '4 - four', '5 - five']
    fig = plt.figure(figsize=(10, 5))
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

        # TODO: add check to make sure exactly 5 cards selected
        # tot_input_cnt = count_tot_inputs(a_s=a_s, k_s=k_s, q_s=q_s, j_s=j_s, t_s=t_s, nine_s=nine_s,
        #                                    a_c=a_c, k_c=k_c, q_c=q_c, j_c=j_c, t_c=t_c, nine_c=nine_c,
        #                                    a_d=a_d, k_d=k_d, q_d=q_d, j_d=j_d, t_d=t_d, nine_d=nine_d,
        #                                    a_h=a_h, k_h=k_h, q_h=q_h, j_h=j_h, t_h=t_h, nine_h=nine_h)

        st.text(f'Trump chosen: {select_trump}; Player table position: {player_position}')

        # translate inputs into dataframe
        hand_df = translate_st_input_to_df(trump=select_trump,
                                           a_s=a_s, k_s=k_s, q_s=q_s, j_s=j_s, t_s=t_s, nine_s=nine_s,
                                           a_c=a_c, k_c=k_c, q_c=q_c, j_c=j_c, t_c=t_c, nine_c=nine_c,
                                           a_d=a_d, k_d=k_d, q_d=q_d, j_d=j_d, t_d=t_d, nine_d=nine_d,
                                           a_h=a_h, k_h=k_h, q_h=q_h, j_h=j_h, t_h=t_h, nine_h=nine_h)
        hand_df['player_seat'] = player_position
        hand_df['num_suits'] = count_suits_st_input(trump=select_trump,
                                                    a_s=a_s, k_s=k_s, q_s=q_s, j_s=j_s, t_s=t_s, nine_s=nine_s,
                                                    a_c=a_c, k_c=k_c, q_c=q_c, j_c=j_c, t_c=t_c, nine_c=nine_c,
                                                    a_d=a_d, k_d=k_d, q_d=q_d, j_d=j_d, t_d=t_d, nine_d=nine_d,
                                                    a_h=a_h, k_h=k_h, q_h=q_h, j_h=j_h, t_h=t_h, nine_h=nine_h)

        # load model
        model = joblib.load('C:/Users/jerem/Desktop/nonsense/euchre/models/trick_model_rf_v0.sav')
        # create model preds
        hand_preds = model.predict_proba(hand_df)
        st.text(hand_preds)

        bar_chart(expected_tricks_taken=hand_preds.tolist()[0])

    # DEV MODE - check current session state
    # st.write(f'Session State: {st.session_state}')


if __name__ == '__main__':
    try:
        main()

    except Exception as err:
        raise err
