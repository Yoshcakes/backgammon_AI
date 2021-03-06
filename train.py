"""
Backgammon AI
"""

from environment import Environment
from player import Player
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import os


def train():
    env = Environment()

    white = Player(0)
    black = Player(1)
    # random_black = Player(1, env, random=True)

    num_games = 10
    num_test_games = 20
    test_frequency = 200
    generation_frequency = 2000
    outputfolder="runtest"
    
    os.makedirs(outputfolder, exist_ok=True)
    performance = defaultdict(dict)
    generation = 0

    t0 = datetime.now()

    for game in range(num_games):
        # Save generation
        if game % generation_frequency == 0: # Save generation
            print("Saving generation", str(generation))
            white.save_model(outputfolder+"/gen_"+str(generation)+".h5")
            black.save_model(outputfolder+"/gen_"+str(generation)+".h5")
            generation += 1

        # Check performance
        if game % test_frequency == 0:
            print("Testing current generation")
            reference_black = Player(1, random=False)
            for gen in range(generation):
                reference_black.load_model(outputfolder+"/gen_"+str(gen)+".h5")
                performance[gen][game] = env.check_performance(white, reference_black, num_test_games)
        
        # Play game
        env.play_game(white, black, verbose=False)

        # Remember the game
        white.remember_game(env.board_history, env.winner, env.score)
        black.remember_game(env.board_history, env.winner, env.score)

        # Replay boards from the past
        white.replay(100) # ~ 1 whole games of 100 moves
        black.replay(100)

        print("Game", game, " | Nb moves", len(env.board_history), " | winner", env.winner, " | score", env.score)

    # Save last generation        
    print("Saving generation", str(generation))
    white.save_model(outputfolder+"/gen_"+str(generation)+".h5")
    black.save_model(outputfolder+"/gen_"+str(generation)+".h5")

    # Plot performance evolution
    for gen in performance:
        plt.plot(list(performance[gen].keys()), list(performance[gen].values()), label="Gen"+str(gen))
    plt.ylim((0,1))
    plt.xlabel("Game")
    plt.ylabel("Performance")
    plt.title("Evolution of performance of player vs other generations")
    plt.legend()
    plt.grid()
    plt.savefig(outputfolder+"/perfEvolution.png")

    # Final output
    print("Time:", datetime.now() - t0)


if __name__ == "__main__":
    train()