# MLB Simulation Against Left-Handed Pitching
Simulates the offensive portion of full nine-inning MLB games against left-handed pitchers using 2025 Statcast player data.

## Overview
Users input a lineup of nine MLB players, and the model simulates each plate appearance over the course of a full game. Outcomes are generated probabilistically based on each  player's hitting splits against left-handed pitchers during the 2025 season. 
For instance, if a player walked in 10% of their plate appearances against left-handed pitchers, the simulation assigns a 10% probability of a walk for that player's plate appearance.

## Features
* Simulates the offensive portion of a full nine-inning game
* Uses 2025 Statcast player data
* Prompts user for custom lineup input
* Accounts for base runners, outs, and runs scored
* Outputs the total number of runs scored by the lineup against a left-handed pitcher

## Tools Used
* Python
* pybaseball
* statcast_batter
* playerid_lookup
* random

## Setup Instructions:
* Install Python 3.10+
* Run: 'pip install pandas'
* Run: 'python3 mlb_game_simulation_against_lhp.py'
* Enter nine official MLB players when prompted.
