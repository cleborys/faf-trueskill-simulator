import trueskill
from trueskill import Rating
import math

import matplotlib
import matplotlib.pyplot as plt

import random
import csv

random.seed("trueskill rulez")

# see github.com:FAForever/server/server/config.py
trueskill.setup(mu=1500, sigma=500, beta=240, tau=10, draw_probability=0.10)


class Player:
    static_id = 0

    def __init__(
        self, skill_mu=1500, skill_sigma=500, rating_mu=1500, rating_sigma=500
    ):
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

    def matches_with(self, other, threshold=0.7):
        my_quality = trueskill.quality([(self.rating,), (self.rating,)])
        their_quality = trueskill.quality([(other.rating,), (other.rating,)])
        match_quality = trueskill.quality([(self.rating,), (other.rating,)])

        return match_quality > threshold * max(my_quality, their_quality)

    def battle(self, opponent):
        i_win = random.uniform(0, 1) < win_probability(self, opponent)

        rating_groups = [(self.rating,), (opponent.rating,)]
        ranks = [1 - int(i_win), int(i_win)]

        new_ratings = trueskill.rate(rating_groups, ranks=ranks)
        my_rating = new_ratings[0][0]
        their_rating = new_ratings[1][0]

        self._game_journal.append((i_win, my_rating))
        opponent._game_journal.append((not i_win, their_rating))

        self.rating = my_rating
        opponent.rating = their_rating

    @classmethod
    def from_csv(cls, eval_function, filename="ratings.csv"):
        with open(filename) as f:
            reader = csv.reader(f)
            return [cls(*eval_function(row)) for row in reader]


def no_rerate(row):
    id, g_mean, g_dev, g_num, l_mean, l_dev, l_num = row
    return (float(l_mean), float(l_dev), float(g_mean), float(g_dev))


def double_dev(row):
    id, g_mean, g_dev, g_num, l_mean, l_dev, l_num = row
    return (float(l_mean), float(l_dev), float(g_mean), 2 * float(g_dev))


def add_150_dev(row):
    id, g_mean, g_dev, g_num, l_mean, l_dev, l_num = row
    return (float(l_mean), float(l_dev), float(g_mean), 150 + float(g_dev))


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
    THRESHOLD = 0.7
    RERATE_FUNCTION = add_150_dev
    players = Player.from_csv(RERATE_FUNCTION)

    game_count = 0
    while game_count < GAMES_PER_PLAYER * len(players):
        player, opponent = random.choices(players, k=2)
        if player.matches_with(opponent, THRESHOLD):
            game_count += 1
            if game_count % 100 == 0:
                print(f"Match {game_count}")
            player.battle(opponent)

    for player in players:
        player.print_history()

    plot_histories(players)
