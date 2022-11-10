"""
Bayesian Theory of Mind (BToM) Agent Implementation for stag hunt game using tomsup

tomsup library can be found at:
https://github.com/KennethEnevoldsen/tomsup
"""

# ---------- Libraries ----------

import tomsup as ts


# ---------- Class ----------

class BToMAgent():

    def __init__(self, payoffMatrix: ts.PayoffMatrix = ts.PayoffMatrix("staghunt"), levelOfToM: str = "2-TOM"):
        """
        Initiate BToM Agent

        :param payoffMatrix: tomsup payoff matrix representing staghunt game
        :type: ts.PayoffMatrix

        :param levelOfToM: level of theory of mind (i.e. 1-TOM, 2-TOM, 3-TOM, etc.)
        :type: int
        """
        # set the payoff matrix
        self.payoffMatrix = payoffMatrix

        # define the agent
        self.tom = ts.create_agents(agents=levelOfToM, start_params={"save_history": True})

        # alter estimation of opponent sophistication level to match approximate human sophistication
        init_states = self.tom.get_internal_states()
        init_states["own_states"]["p_k"] = [0.3, 0.7]
        self.tom.set_internal_states(init_states)

    def respond(self, opChoice: int):
        """
        Get agent response to opponent's choice.

        :return resp_tom: response of the tom agent, either 0 or 1
        :rtype: int
        """
        resp_tom = self.tom.compete(p_matrix = self.payoffMatrix, op_choice=opChoice, agent=1)
        return resp_tom
