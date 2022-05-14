import numpy as np


class QLearner(object):
    def __init__(
        self, num_states, num_actions, alpha, gamma, rar, radr, dyna, verbose=False
    ):
        """This is a Q learner object.

        :param num_states: The number of states to consider.
        :type num_states: int
        :param num_actions: The number of actions available.
        :type num_actions: int
        :param alpha: The learning rate used in the update rule. Should range between
        0.0 and 1.0 with 0.2 as a typical value.
        :type alpha: float
        :param gamma: The discount rate used in the update rule. Should range between
        0.0 and 1.0 with 0.9 as a typical value.
        :type gamma: float
        :param rar: Random action rate: the probability of selecting a random action at
        each step. Should range between 0.0 (no random actions) to 1.0
        (always random action) with 0.5 as a typical value.
        :type rar: float
        :param radr: Random action decay rate, after each update, rar = rar * radr.
        Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.
        :type radr: float
        :param dyna: The number of dyna updates for each regular update. When Dyna is
        used, 200 is a typical value.
        :type dyna: int
        :param verbose: If “verbose” is True, your code can print out information for
        debugging.
        :type verbose: bool
        """
        self.verbose = verbose
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        # Initial state and action
        self.state = 0
        self.action = 0

        # Initialize Q[s, a] with all zeros
        self.Q = np.zeros(shape=(self.num_states, self.num_actions))

        # Initialize Tc[s, a, s_prime] with 0.00001
        self.Tc = np.full(
            shape=(self.num_states, self.num_actions, self.num_states),
            fill_value=0.00001,
        )

        # Initialize T[s, a, s_prime]
        # Tc[s, a, s_prime] / T[s, a, s_prime].sum()
        # Sum across s_prime, copy over dimensions
        self.T = self.Tc / self.Tc.sum(axis=2, keepdims=True)

        # Initialize R[s, a] with all zeros
        self.R = np.zeros(shape=(self.num_states, self.num_actions))

    def querysetstate(self, s):
        """Update the state without updating the Q-table. Given a probability, we also
        choose a random action; Q-learning is successful when we explore.

        :param s: The new state
        :type s: int
        :return: The selected action
        :rtype: int
        """
        self.state = s

        if np.random.random() < self.rar:
            self.action = np.random.randint(self.num_actions)
        else:
            # Epsilon-Greedy Action Selection
            # https://www.baeldung.com/cs/epsilon-greedy-q-learning#2-epsilon-greedy-action-selection
            self.action = self.Q[
                self.state,
            ].argmax()

        if self.verbose:
            print(f"s = {self.state}, a = {self.action}")
        return self.action

    def query(self, s_prime, r):
        """Update the Q table and return an action

        :param s_prime: The new state
        :type s_prime: int
        :param r: The immediate reward
        :type r: float
        :return action_prime: The selected action
        :rtype action_prime: int
        """
        # Q-learn, update Q with <s, a, s', r>
        # Using numpy.argmax to resolve argmax in update rule function
        # https://numpy.org/doc/stable/reference/generated/numpy.argmax.html#numpy.argmax
        self.Q[self.state, self.action] = (
            (1 - self.alpha) * self.Q[self.state, self.action]
        ) + self.alpha * (
            r
            + self.gamma
            * self.Q[
                s_prime,
                self.Q[
                    s_prime,
                ].argmax(),
            ]
        )

        # Dyna-Q
        if self.dyna:
            # Update T'[s, a, s']
            self.Tc[self.state, self.action, s_prime] += 1
            self.T = self.Tc / self.Tc.sum(axis=2, keepdims=True)

            # Update R'[s, a]
            self.R[self.state, self.action] = (
                (1 - self.alpha) * self.R[self.state, self.action]
            ) + self.alpha * r

            states = np.random.randint(low=self.num_states, size=self.dyna)
            actions = np.random.randint(low=self.num_actions, size=self.dyna)
            # Acquire highest probable state_prime
            state_primes = self.T[states, actions, :].argmax(axis=1)
            rewards = self.R[states, actions]
            # Update Q with <s, a, s', r>; vectorized all the things
            self.Q[states, actions] = (
                (1 - self.alpha) * self.Q[states, actions]
            ) + self.alpha * (
                rewards
                + self.gamma
                * self.Q[
                    state_primes,
                    self.Q[
                        state_primes,
                    ].argmax(axis=1),
                ]
            )

        # Set our state to state_prime, find out what our next action is
        action_prime = self.querysetstate(s=s_prime)
        # Update random action rate using decay
        # https://stackoverflow.com/questions/48583396/q-learning-epsilon-greedy-update
        self.rar *= self.radr

        if self.verbose:
            print(f"s = {self.state}, a = {self.action}, r={r}")
        return action_prime
