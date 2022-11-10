"""
Bayesian Theory of Mind (BToM) stag hunt game using tomsup

Based off of tomsup matching pennies tutorial:
https://github.com/KennethEnevoldsen/tomsup/blob/master/tutorials/psychopy_experiment/matching_pennies.py
"""

# ---------- Libraries ----------
import os

import tomsup as ts
import streamlit as st

from btom_agent import BToMAgent
from run_sim import maps, shum_maps, shum_locs


# ------------- Getting participant information -------------

st.header("BToM Stag Hunt")

# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.mkdir("data")

# GEt out names of data in the data folder
l = os.listdir("data")

# If there is data already there
# find the max ID and set it to 1 higher,
# otherwise start at 1
if l:
    ID = max([int(i.split("_")[-1].split(".")[0]) for i in l])
    ID = ID + 1
else:
    ID = 1

n_games = 2


# ------------- Defining Variables and function -------------
introtext = f"""Dear participant

Thank you for playing against tomsup!
Here we will make you play against simulated agents in the stag hunt game.
If you at any time wish to do so, you are free to stop the experiment and 
ask for any generated data to be deleted. If you have read the above and 
wish to proceed, press 'Next' below."""

rulestext_staghunt = f"""
You will now play a game of staghunt.

You will be a hunter in this game playing with simulated hunters. You can 
choose to hunt either stags or hares. If you and the other hunter(s) both 
go after the stag, you get the greatest payoff. However, if only you go after 
the stag, you get no payoff. If you choose to go after the hares, you will 
get a payoff, but it will be smaller than the payoff for jointly getting the 
stag. Your goal is to maximize your payoff. You must choose whether or not to 
blindly cooperate with the other hunter(s) to get the stag or solely go after 
the hares. But, remember, they may not choose to co-operate with you.

You will play {n_games} games.
"""


# ------------- Write intro text -------------

if "page" not in st.session_state:
    st.session_state.page = 0

def nextpage(): st.session_state.page += 1
def restart(): st.session_state.page = 0

placeholder = st.empty()
placeholder.write(introtext)
st.button("Next",on_click=nextpage)

if st.session_state.page == 1:
    placeholder.write(rulestext_staghunt)

if st.session_state.page == 2:
    opponent_strategy = placeholder.selectbox("Choose your opponent strategy", ("0-TOM", "1-TOM", "2-TOM", "3-TOM", "4-TOM"))

    # create payoff matrix and agent
    if opponent_strategy:
        payOffMatrix = ts.PayoffMatrix("staghunt")
        agent = BToMAgent(payoffMatrix = payOffMatrix, levelOfToM = "2-TOM")

        # ---------- Preparing json to store results -------------
        gameMetadata = {
            "id": ID,
            "startTime": "",
            "endTime": "",
            "games": "",
            "opponentStrategy": opponent_strategy
        }

        games = []
        for game in range(n_games):
            games += [
                {
                    "id": ID,
                    "initialCharacterState": "",
                    "map": "",
                    "data": ""
                }
            ]

        # ------------- Running the experiment -------------
        op_choice = None # setting opponent choice to none for the first round
