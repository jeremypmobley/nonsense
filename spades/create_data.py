
import pandas as pd
from main import Game


def play_multiple_games(num_games):
    results = []

    for _ in range(num_games):
        game = Game()
        game.play()
        results.extend(game.data)  # Collect data from each game

    return results


def save_out_results(results):
    hand_results_df = pd.DataFrame(results)
    hand_results_df.columns = ['player', 'cards_binary', 'bids', 'tricks_won', 'player_score']
    hand_results_df.to_csv('data/hand_results.csv', index=False)


if __name__ == "__main__":
    num_games = 2  # Number of games to simulate
    results = play_multiple_games(num_games=num_games)
    save_out_results(results)
