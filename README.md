# FA Forever - Trueskill simulator

A quick hack to simulate the evolution of trueskill ratings 
in [Forged Alliance Forever](https://github.com/FAForever).

# setup

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

# Usage

    $ source venv/bin/activate
    $ python simulator.py

Adjust the pool of players in `simulator.py` at the top of the main block.
A player is given a skill (mu and sigma), which is used to simulate their
"true" trueskill rating, as well as an initial rating (mu and sigma).
The winner of a 1v1 game is determined by evaluating the player's "true"
trueskill, but they are scored according to their rating.
