from collections import defaultdict
import ast
import random
import json
import os
from datetime import datetime


class QAgent:
    def __init__(self):
        self.lr = 0.1         
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.9995 
        self.epsilon_min = 0.01

        # 3 actions: 0=forward, 1=left, 2=right
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0])

    def end_episode(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save_model(self):
        fname = "model/" + datetime.now().strftime("model_%Y%m%d_%H%M%S.json")
        data = {
            "q_table": {str(k): v for k, v in self.q_table.items()},
            "epsilon": self.epsilon,
        }
        with open(fname, "w") as f:
            json.dump(data, f)

        print(f"Model saved to {fname}")

    def load_model(self, filename="qtable.pkl"):
        if not os.path.exists(filename):
            print("No saved model found")
            return

        with open(filename, "r") as f:
            data = json.load(f)

        self.q_table = defaultdict(
            lambda: [0.0, 0.0, 0.0, 0.0]
        )

        for k, v in data["q_table"].items():
            self.q_table[ast.literal_eval(k)] = v

        self.epsilon = data["epsilon"]
        print(f"Model loaded from {filename}")


    def encode_state(self, state):
        return tuple(state)

    def choose_action(self, state):
        state = self.encode_state(state)
        
        # 1. Exploration
        if random.random() < self.epsilon:
            return random.randint(0, 2)

        # 2. Exploitation
        q_values = self.q_table[state]
        best_value = max(q_values)
        best_actions = [a for a in range(3) if q_values[a] == best_value]
        
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, done):
        state = self.encode_state(state)
        next_state = self.encode_state(next_state)

        old_q = self.q_table[state][action]

        if done:
            target = reward
        else:
            # Выбираем максимум из 3-х возможных относительных действий
            next_q = max(self.q_table[next_state])
            target = reward + self.gamma * next_q

        self.q_table[state][action] = old_q + self.lr * (target - old_q)