"""
Bayesian Theory of Mind (BToM) stag hunt game

Based off of tomsup matching pennies tutorial:
https://github.com/KennethEnevoldsen/tomsup/blob/master/tutorials/psychopy_experiment/matching_pennies.py

This code utilizes pyamaze:
https://github.com/MAN1986/pyamaze

and the a* algorithm from:
https://levelup.gitconnected.com/a-star-a-search-for-solving-a-maze-using-python-with-visualization-b0cae1c3ba92
"""

# ---------- Libraries ----------
import os

import numpy as np
from queue import PriorityQueue

import tomsup as ts
from pyamaze import maze, agent

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

initialCharacterState = {
    "r1": [1,4],
    "r2": [5,1],
    "s1": [2,5],
    "h1": [2,1],
    "h2": [1,3]
}

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


# ------------- Main method -------------

def main():
    strategy_options = ["0-TOM", "1-TOM", "2-TOM", "3-TOM", "4-TOM"]

    opponent_strategy = input(
            f"Please choose your opponent strategy. Enter one of {strategy_options}: ")

    if opponent_strategy in strategy_options:
        # create payoff matrix and agent
        payOffMatrix = ts.PayoffMatrix("staghunt")
        tom_agent = BToMAgent(payoffMatrix=payOffMatrix, levelOfToM="2-TOM")

        print(f"Payoff matrix: {payOffMatrix}")

        # ---------- Preparing json to store results -------------
        gameMetadata = {
            "id": ID,
            "startTime": "",
            "endTime": "",
            "games": "",
            "opponentStrategy": opponent_strategy
        }

        game = {
            "id": ID,
            "initialCharacterState": initialCharacterState,
            "map": "",
            "data": [initialCharacterState],
        }

        # ------------- Running the experiment -------------

        inPlay = True  # initialize a variable to determine if the game is in play
        count = 0  # counter to track number of steps in game
        distances = []  # initialize distances tracker list to hold distances between prey and human agent at each step

        # the hare locations are static, so they won't need updating
        # and we can retrieve them from the initialCharacterState
        r1_loc = initialCharacterState["r1"]
        r2_loc = initialCharacterState["r2"]

        # get original stag and human player positions
        s1_loc = initialCharacterState["s1"]
        h1_loc = initialCharacterState["h1"]

        # find original distances between characters
        # and append to distances tracker list
        original_distances = get_distances_dict(h1_loc, r1_loc, r2_loc, s1_loc)
        distances.append(original_distances)

        # get original tom location
        tom_loc = initialCharacterState["h2"]

        # get and initialize current maze
        m = maze(7, 7)
        m.CreateMaze()
        maze_map = m.maze_map

        game["map"] = maze_map

        # set human player agent in pyamaze game
        h1_agent = agent(m, x=h1_loc[0], y=h1_loc[1], shape='arrow', footprints=True)
        r1 = agent(m, x=r1_loc[0], y=r1_loc[1])
        r2 = agent(m, x=r2_loc[0], y=r2_loc[1])
        s1 = agent(m, x=s1_loc[0], y=s1_loc[1], footprints=True)

        while inPlay:
            prev_player_moves = game["data"][count]

            # get options for human player to move to
            h1_maze_walls = maze_map[(h1_loc[0], h1_loc[1] + 1)]
            h1_move_options = [k for k, v in h1_maze_walls.items() if v == 0]
            h1_move_options.append("Stay")

            h1_move_direction = ""
            while h1_move_direction not in h1_move_options:
                h1_move_direction = input(
                    f"Please choose your next move. Enter one of {h1_move_options}: ")

            if h1_move_direction in h1_move_options:
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

                # get tom move/new location using A* algorithm
                if resp_tom == 1:
                    # going after hares
                    m.CreateMaze(s1_loc[0], s1_loc[1])
                    astar_moves = aStar(m)
                    print(astar_moves)
                    tom_loc = astar_moves[tuple(tom_loc)]
                else:
                    # going after hares,
                    # so find the closest hare and treat this hare as the goal
                    hare_positions = {"r1": get_dist(tom_loc, r1_loc), "r2": get_dist(tom_loc, r2_loc)}
                    goal_hare = min(hare_positions, key=hare_positions.get)
                    goal_hare_loc = initialCharacterState[goal_hare]
                    m.CreateMaze(goal_hare_loc[0], goal_hare_loc[1])
                    astar_moves = aStar(m)
                    print(astar_moves)
                    tom_loc = astar_moves[tuple(tom_loc)]

                tom_agent.position = tom_loc

                print(f"tom agent position: {tom_agent.position}")

                new_positions = {"r1": r1_loc, "r2": r2_loc, "s1": s1_loc, "h1": h1_loc, "h2": tom_loc}

                game["data"].append(new_positions)

                count = count + 1


if __name__ == '__main__':
    main()