# Euchre

Play games of Euchre and analyze the results

## Goal: 
Create a fully functional euchre game to better understand trick taking probabilities of different starting hands

### Model to Predict Points Scored From Given Hand
Answering the question:
Given the cards in a players hand (and position at the table), what is the likelihood of winning each number of tricks that hand?

### Streamlit app 
* User can select cards in hand and table position 
* Returns bar chart of likelihood of taking 5/4/3/2/1/0 tricks

### Future Ideas:
* Model to predict number of tricks team won that hand
* Reinforcement learning agent to call trump, play card
* PySimpleGUI to learn to play game

### Tests

To run tests locally, execute:

python -m pytest C:\Users\jerem\Desktop\nonsense\euchre\tests\test_euchre.py

