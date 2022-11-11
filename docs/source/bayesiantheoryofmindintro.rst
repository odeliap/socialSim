.. _btomintro:
Introduction to Bayesian Theory of Mind
=======================================

This section will teach you about Bayesian Theory of Mind (BToM).
The content here is based on the paper *Bayesian Theory of Mind: Modeling
Joint Belief-Desire Attribution* by Chris L. Baker, Rebecca R. Saxe, and
Joshua B. Tenenbaum.

Background
----------

Theory of mind is the capacity to explain and predict people's
actions from mental states such as beliefs and desires. The goal
of theory of mind is to infer others' goals or preferences from
their decisions, which is done through inverse planning or inverse
decision theory. Bayesian Theory of Mind is inspired by inverse
planning.

Generally, agents are expected to choose actions which maximize
their desires. So, goals are inferred from objective observed
actions as being the goal which is maximized from the action most
directly. Theory of Mind (ToM) builds on this by adding mental states
(such as beliefs about the world) to the agent representations.

Bayesian Theory of Mind (BToM) can be cast as an inverse planning
and inference problem: agent's planning and inference are represented
as partially observable Markov decision processes (POMDPs). This BToM
model includes:

* Representations of agent's desires (utility function); and
* Agent's own subjective beliefs about the environment (probability distribution)

Questions
+++++++++

From this BToM framework arise certain questions, such as

* How closely do human judgements approach an ideal limit?
* What mental representations are necessary to explain human judgements?

Theory
++++++

In formally modeling these agents, we make key observations. Firstly,
the observer's representation fo the world is composed of an
**environment state** and an **agent state**. An agent's desires are
represented by subjective rewards received for taking actions in certain
states. The **beliefs** are defined by their content and the strength
with which they are held - an agent's degree of belief reflects the
subjective probability it assigns to each possible world.

The principles governing the relation between the world and the agent's
beliefs, desires, and actions can be expressed with partially observable
Markov decision processes (POMDPs). POMDPs represent how beliefs and
desires cause actions via the principle of rational action (aka rational
planning), as previously explained. POMDPs provide a model for agent
optimization in the tradeoff between exploring the environment to discover
the best rewards and exploiting already known rewards to minimize costs.

After observing an agent's behavior within an environment, Bayesian inference
can be used to infer the beliefs and desires which caused this action. The
observer maintains a hypothesis space, and for each hypothesis, it evaluates
the likelihood of the observed actions coming from the given belief or desire.
BToM infers the best explanation for the observed behavior that consistently
matches the observed actions.

Formal Modeling
+++++++++++++++

To formally model BToM agents, we need:

* X: discrete state space of points in a 2D grid the agent can occupy;
* y: environment state; the set of possible assignments;
* The set of possible actions;
* Valid actions that yield the intended transition with a probability of 1 - epsilon and do nothing otherwise (i.e. invalid actions have no effect on the state);
* *isovisit*: represents the agent's visual observations from its given location; polygonal region containing all points of the environment within the agent's 360-degree field of view;
* P(o|x,y): encodes which environments in epsilon are consistent with the contents of the *isovisit* from location x;
* Observation noise modeled with the assumption that ambiguous observations occur with a probability of v (such as an agent missing something that should be visible);
* Observer represents agent's beliefs as a probabilistic distribution over epsilon; y in epsilon, b(y) gives the agent's degree of belief that y is the true state of the environment;
* **Bayesian belief updating**: deterministic function of prior belief, observation, and world state as a function of time;
* **Reward function**: the reward function for an agent given by R(x,y,a) which encodes the subjective utility an agent gets from taking the action a from state <xt, yt>; each action is assumed to incur a cost of 1; and
* **POMDP**: defined by the state space, action space, world dynamics, observation model, and reward function; approximated optimal value of POMDP is given for each hypothesized reward function using a point-based value iteration algorithm over a uniform discretization of belief space.