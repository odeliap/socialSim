.. _btomimplementation:
Bayesian Theory of Mind Implementation
======================================

This section will explain the Bayesian Theory of Mind (BToM)
implementation I (Odelia Putterman) included in this repository.
If you have any questions, feel free to reach out to me by email
(putterman@oxy.edu)!

Background
++++++++++

In implementing some agent for eventual evaluation and comparison against
the companions agent(s), I chose, with the help of my research professor, to implement
BToM agents. Since the :ref:`theory of BToM <btomintro>` is quite complex,
we opted to search for existing implementations and modify them to our needs.
This culminated in finding :ref:`tomsup <tomsupintro>`, a python Theory of Mind
simulation package. This package implements a variational Bayesian k-ToM model,
which fits our wanted backing theory of mind for this evaluation exactly.
The implementation of this BToM model exists for the agents available in this
package. So, we opted to use these tomsup BToM agents in developing this comparison
staghunt game.

tomsup
++++++

Firstly, I went through all the tutorials on the tomsup page. (If you are taking over
this project, I would highly recommend going through these tutorials in jupyter notebooks -
they will introduce you to the world of agents in tomsup!) In trying to understand
how we could implement these agents in a way compatible for evaluation with the
implementation of companions agents in this repository, I read the paper tomsup's
implementation of BToM comes from and tested running the agents in different simulations
in jupyter notebooks. Below, I outline how tomsup agents learn and compete in different
game theory games.

In tomsup, the game is defined by a **payoff matrix** which describes the reward each agent
(of the two agents) will get for each decision they make. These decisions are binary - they
can only be 0 or 1. In the staghunt game, 0 represents going for the hares while 1 represents
going after the stag. The BToM agents learn by looking at the past decisions of their opponent
to decide whether to go after the hare or the stag.

Problem Context
+++++++++++++++

The initial problem with the tomsup implementation for our use in comparing BToM agents against
the previously implemented companions agents is that it simply made a choice, 0 or 1, once, without
any affect on the path the agent will take or which hare, in particular, it will pursue if its
decision signifies it will chase these hares. So, we needed some way of making these compatible.

Solution and Implementation
+++++++++++++++++++++++++++

To do so, we decided to have the Theory of Mind agent at each step of the stag hunt game take the
user's movement as directly signaling its goal prey; whichever prey the user is moving towards most
is the perceived 'goal prey'. At each step, we calculate the distances between the user and the prey
characters and compare this against the distances between the user and prey characters at the previous
timestep. Whichever prey it is minimizing its distance to most is considered the goal prey.
If this goal prey is a hare, we pass this input to the Theory of Mind agent as a choice of '0';
if this goal prey is a stag, we pass this input to the Theory of Mind agent as a choice of '1'.
We then have the Theory of Mind agent make its choice, 0 or 1. If the agent's choice is 1, we say the
agent is pursuing the stag, and we, accordingly, use an A* algorithm to find the fastest path to the stag.
The next step (from the agent's current position) to the stag returned from this algorithm is the agent's
'chosen move'. In this way, the user and agent compete, with decisions made at each timestep for both
parties to stay consistent with the other implementations of agents in this repository.

This workflow follows:

1. Calculate the distances between the human player and each of the prey characters
2. Retrieve the distances between the human player and each of the prey characters at the previous timestep
3. Find the distance between the human player and prey character which was most minimized from the previous timestep
4. Call the prey character the 'goal prey'
5. Give this 'goal prey' to the tom agent as a 0 or 1 option (0 = hare, 1 = stag)
6. Have the tom agent makes its decision (0 or 1)
7. If the tom decision was 0, find the closest hare to it and call this the 'goal prey' for the tom; otherwise the 'goal prey' for the tom is the stag
8. Use an A* algorithm to find the shortest path between the tom and its goal prey
9. Take the first step in the A* algorithm as the agent's new location/chosen movement
10. Repeat continuously until game is over