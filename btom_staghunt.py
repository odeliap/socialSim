"""
Bayesian Theory of Mind (BToM) stag hunt game using tomsup using streamlit for simple UI!

Based off of tomsup matching pennies tutorial:
https://github.com/KennethEnevoldsen/tomsup/blob/master/tutorials/psychopy_experiment/matching_pennies.py
"""

# ---------- Libraries ----------
import os

import numpy as np
from queue import PriorityQueue

import tomsup as ts
from pyamaze import maze, agent
import streamlit as st

from btom_agent import BToMAgent

# ------------- Getting participant information -------------

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


# ------------- Defining Variables -------------

n_games = 2

initialCharacterState_game1 = {
    "r1": [1,4],
    "r2": [5,1],
    "s1": [2,5],
    "h1": [2,1],
    "h2": [1,3]
}

initialCharacterState_game2 = {
    "r1": [1,4],
    "r2": [5,1],
    "s1": [2,5],
    "h1": [2,1],
    "h2": [1,3]
}

initialCharacterStates = [initialCharacterState_game1, initialCharacterState_game2]

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


# ------------- Defining Useful Functions -------------

def get_dist(a: list, b: list):
    """
    Get distance between two location lists.

    :param a: first list
    :type: list

    :param b: second list
    :type: list

    :return dist: distance between the two input tuples
    :rtype: double
    """
    a_np = np.asarray(tuple(a))
    b_np = np.asarray(tuple(b))
    dist = np.linalg.norm(a_np - b_np)
    return dist


def get_distances_dict(h1_loc: list, r1_loc: list, r2_loc: list, s1_loc: list):
    """
    Get dictionary representation of distances between human player and prey targets.

    :param h1_loc: list representation of human player's location
    :type: list

    :param r1_loc: list representation of first hare's location
    :type: list

    :param r2_loc: list representation of second hare's location
    :type: list

    :param s1_loc: list representation of stag's location
    :type: list

    :return dictionary: dictionary representation of distances between players
    :rtype: dict
    """
    dist_h1_r1 = get_dist(h1_loc, r1_loc)
    dist_h1_r2 = get_dist(h1_loc, r2_loc)
    dist_h1_s1 = get_dist(h1_loc, s1_loc)
    return {"r1": dist_h1_r1, "r2": dist_h1_r2, "s1": dist_h1_s1}


def get_goal_prey(prev_distances: dict, current_distances: dict):
    """
    Get goal prey by evaluating which prey target the human player is moving towards.

    :param prev_distances: previous distances between human player and prey characters
    :type: dict

    :param current_distances: current distances between human player and prey characters
    :type: dict

    :return goal_prey: perceived goal target prey of the human player
    :rtype: str
    """
    r1_diff = current_distances["r1"] - prev_distances["r1"]
    r2_diff = current_distances["r2"] - prev_distances["r2"]
    s1_diff = current_distances["s1"] - prev_distances["s1"]
    differences_dict = {"r1": r1_diff, "r2": r2_diff, "s1": s1_diff}
    goal_prey = min(differences_dict, key=differences_dict.get)
    return goal_prey


# ------------- A* Functions -------------

# Taken from: https://levelup.gitconnected.com/a-star-a-search-for-solving-a-maze-using-python-with-visualization-b0cae1c3ba92

def h(cell1,cell2):
    x1,y1=cell1
    x2,y2=cell2

    return abs(x1-x2) + abs(y1-y2)

def aStar(m):
    start=(m.rows,m.cols)
    g_score={cell:float('inf') for cell in m.grid}
    g_score[start]=0
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start]=h(start,(1,1))

    open=PriorityQueue()
    open.put((h(start,(1,1)),h(start,(1,1)),start))
    aPath={}
    while not open.empty():
        currCell=open.get()[2]
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score=g_score[currCell]+1
                temp_f_score=temp_g_score+h(childCell,(1,1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,h(childCell,(1,1)),childCell))
                    aPath[childCell]=currCell
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return fwdPath


# ------------- Write intro text -------------

st.header("BToM Stag Hunt")

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
        tom_agent = BToMAgent(payoffMatrix = payOffMatrix, levelOfToM = "2-TOM")

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
                    "initialCharacterState": initialCharacterStates[game],
                    "map": "",
                    "data": [initialCharacterStates[game]],
                }
            ]

            # ------------- Running the experiment -------------
            op_choice = None # setting opponent choice to none for the first round
            inPlay = True # initialize a variable to determine if the game is in play
            count = 0 # counter to track number of steps in game
            distances = [] # initialize distances tracker list to hold distances between prey and human agent at each step

            # the hare locations are static, so they won't need updating and
            # we can retrieve them from the initialCharacterState
            r1_loc = initialCharacterStates[game]["r1"]
            r2_loc = initialCharacterStates[game]["r2"]

            # get original stag and human player positions
            s1_loc = initialCharacterStates[game]["s1"]
            h1_loc = initialCharacterStates[game]["h1"]

            # find original distances between characters
            # and append to distances tracker list
            original_distances = get_distances_dict(h1_loc, r1_loc, r2_loc, s1_loc)
            distances.append(original_distances)

            # get original tom location
            tom_loc = initialCharacterStates[game]["h2"]

            # get and initialize current maze
            m = maze(7, 7)
            m.CreateMaze()

            games[game]["map"] = m.maze_map

            # set human player agent in pyamaze game
            h1_agent = agent(m, x=h1_loc[0], y=h1_loc[1], shape='arrow', footprints=True)
            r1 = agent(m, x=r1_loc[0], y=r1_loc[1])
            r2 = agent(m, x=r2_loc[0], y=r2_loc[1])
            s1 = agent(m, x=s1_loc[0], y=s1_loc[1], footprints=True)

            while inPlay:
                prev_player_moves = games[game]["data"][count]

                # get options for human player to move to
                maze_map = m.maze_map
                h1_maze_walls = maze_map[tuple(h1_loc)]
                h1_move_options = [k for k, v in h1_maze_walls.items() if v == 0]

                # prompt user to choose next move from available choices
                h1_move_direction = placeholder.selectbox('Choose direction to move', h1_move_options)

                if h1_move_direction:
                    if h1_move_direction == 'E':
                        h1_loc = [h1_loc[0], h1_loc[1] + 1]
                    elif h1_move_direction == 'W':
                        h1_loc = [h1_loc[0], h1_loc[1] - 1]
                    elif h1_move_direction == 'N':
                        h1_loc = [h1_loc[0] + 1, h1_loc[1]]
                    elif h1_move_direction == 'S':
                        h1_loc = [h1_loc[0] - 1, h1_loc[1]]

                    h1_agent.position = h1_loc

                    # get distances from human to prey and
                    # add these distances to the distances tracker list
                    step_distances = get_distances_dict(h1_loc, r1_loc, r2_loc, s1_loc)
                    distances.append(step_distances)

                    # find the human player's goal prey
                    goal_prey = get_goal_prey(distances[count], distances[count + 1])

                    # determine the human player's choice (0 = hares, 1 = stag)
                    if goal_prey == 'r1' or goal_prey == 'r2':
                        user_choice = 0
                    else:
                        user_choice = 1

                    # get tom response to human player's choice
                    # if response = 1, going after stag
                    # otherwise if response = 0, going after hares
                    resp_tom = tom_agent.respond(user_choice)

                    # TODO: get astar for tom position to goal prey position
                    # get tom move/new location using A* algorithm
                    if resp_tom == 1:
                        # going after hares
                        astar_moves = aStar(m)
                        tom_loc = astar_moves # TODO: fixme!
                    else:
                        # going after hares,
                        # so find the closest hare and treat this hare as the goal
                        hare_positions = {"r1": get_dist(tom_loc, r1_loc), "r2": get_dist(tom_loc, r2_loc)}
                        goal_hare = min(hare_positions, key=hare_positions.get)
                        astar_moves = aStar(m)
                        tom_loc = tom_loc # TODO: fixme!
                    tom_agent.position = tom_loc

                    new_positions = {"r1": r1_loc, "r2": r2_loc, "s1": s1_loc, "h1": h1_loc, "h2": tom_loc}

                    games[game]["data"] = games[game]["data"].append(new_positions)

                    count = count + 1