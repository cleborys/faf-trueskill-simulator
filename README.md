# FA Forever - Trueskill simulator

A quick hack to simulate the evolution of trueskill ratings 
in [Forged Alliance Forever](https://github.com/FAForever).

# Setup

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

# Usage

Activate the virtual environment:

    $ source venv/bin/activate

Download samples from the leaderboard API:

    $ python get_rating_data.py

This will save twenty samples to `ratings.csv`.
Run the simulation:

    $ python simulator.py

Use `save_samples(n)` to save `n` samples of player ratings
for players that have both a global and ladder rating.
These are saved to `ratings.csv` in the format
```
player_id, global_mean, global_deviation, num_global_games, ladder_mean, ladder_deviation, num_ladder_games
```
Then `simulator.py` will read these contents to build the player pool.
A player is given a skill (mu and sigma), which is used to simulate their
"true" trueskill rating, as well as an initial rating (mu and sigma).
"True" skill and initial rating are determined from the CSV data
through the `RERATE_FUNCTION` passed to `Player.from_csv`.
Typically, skill is simply the ladder rating,
while initial rating is determined from the global rating.
Current options are `no_rerate` to use the plain global rating  
or `double_dev` to use the global rating with doubled deviation,
or `add_150_dev` to add 150 to the global deviation.

A number of 1v1 matches is performed, until the players played `GAMES_PER_PLAYER`
matches on average. Match participants are chosen uniformly at random,
but the match only happens if trueskill assigns it a minimum match quality,
determined by `THRESHOLD * quality_against_self`, as in the current matchmaker system..
The winner of the match is determined by probabilistically evaluating the player's "true"
trueskill, but they are scored according to their rating.
