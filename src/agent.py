from collections import defaultdict
import random


class QAgent:

    def __init__(self):

        self.lr = 0.1
        self.gamma = 0.95

        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        self.q_table = defaultdict(
            lambda: [0.0, 0.0, 0.0, 0.0]
        )


    def choose_action(self, state):

        state = tuple(int(v * 10) for v in state)

        if random.random() < self.epsilon:
            return random.randint(0, 3)

        q_values = self.q_table[state]

        return q_values.index(max(q_values))        


    def learn(self, state, action, reward, next_state, done):

        state = tuple(int(v * 10) for v in state)
        next_state = tuple(int(v * 10) for v in next_state)

        old_q = self.q_table[state][action]

        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self.q_table[next_state])

        self.q_table[state][action] = (old_q + self.lr * (target - old_q))    


    def end_episode(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)        


