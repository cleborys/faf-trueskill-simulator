import trueskill
from trueskill import Rating
import math

import matplotlib
import matplotlib.pyplot as plt

import random

random.seed("trueskill rulez")

# see github.com:FAForever/server/server/config.py
trueskill.setup(mu=1500, sigma=500, beta=240, tau=10, draw_probability=0.10)


class Player:
    static_id = 0
    def __init__(self, skill_mu=1500, skill_sigma=500, rating_mu=1500, rating_sigma=500):
        self._id = Player.static_id
        Player.static_id += 1

        self._initial_rating = Rating(rating_mu, rating_sigma)
        self.rating = self._initial_rating
        self.skill = Rating(skill_mu, skill_sigma)
        self._game_journal = [(True, self.rating)]

    def print_history(self):
        print(
            f"Player {self._id} with true skill {self.skill}\n"
            f"  started at rating {self._initial_rating}\n"
            f"  and arrived at rating {self.rating} "
            f" after {len(self._game_journal)} games."
        )


    def battle(self, opponent):
        i_win = (random.uniform(0, 1) < win_probability(self, opponent))
        
        rating_groups = [(self.rating,), (opponent.rating,)]
        ranks = [1 - int(i_win), int(i_win)]

        new_ratings = trueskill.rate(rating_groups, ranks=ranks)
        my_rating = new_ratings[0][0]
        their_rating = new_ratings[1][0]

        self._game_journal.append((i_win, my_rating))
        opponent._game_journal.append((not i_win, their_rating))

        self.rating = my_rating
        opponent.rating = their_rating
    
def plot_histories(players):
    fig, ax = plt.subplots()
    for player in players:
        ratings = [result[1].mu for result in player._game_journal]
        plt.plot(range(len(ratings)), ratings)

    plt.show()

# see https://trueskill.org/#win-probability
def win_probability(player, opponent):
    delta_mu = player.skill.mu - opponent.skill.mu
    sum_sigma = player.skill.sigma ** 2 + opponent.skill.sigma ** 2
    ts = trueskill.global_env()
    denom = math.sqrt(2 * (ts.beta * ts.beta) + sum_sigma)
    return ts.cdf(delta_mu / denom)



if __name__ == "__main__":
    GAMES_PER_PLAYER = 20
    # Player(
    #    actual_skill, actual_skill_sigma, 
    #    initial_rating=1500, initial_sigma=500
    # )
    players = [
        Player(1000, 200),
        Player(1000, 200),
        Player(1000, 200),
        Player(2000, 200),
        Player(2000, 200),
        Player(2000, 200),
    ]

    for _ in range(GAMES_PER_PLAYER * len(players)):
        player, opponent = random.choices(players, k=2)
        player.battle(opponent)
    
    for player in players:
        player.print_history()

    plot_histories(players)
