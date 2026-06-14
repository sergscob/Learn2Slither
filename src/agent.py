from collections import defaultdict
import ast
import random
import json
import os
from datetime import datetime


class QAgent:

    def __init__(self):
        self.current_direction = 0
        self.lr = 0.05
        self.gamma = 0.9

        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05
        self.last_states = []
        self.loop_penalty = 0.2

        self.q_table = defaultdict(
            lambda: [0.0, 0.0, 0.0, 0.0]
        )

    def encode_state(self, state):
        return tuple(state)

    def choose_action(self, state):
        # нормализуем state (ВАЖНО для Q-table ключа)
        state = self.encode_state(state)

        # 0=UP,1=DOWN,2=LEFT,3=RIGHT
        opposite = {
            0: 1,
            1: 0,
            2: 3,
            3: 2
        }
        current_dir = self.current_direction  # хранишь в agent

        # 1. exploration (случайный выбор)
        if random.random() < self.epsilon:

            valid_actions = [
                a for a in range(4)
                if a != opposite[current_dir]
            ]
            self.current_direction = random.choice(valid_actions)
            return self.current_direction

        # 2. exploitation (лучшее Q значение)
        q_values = self.q_table[state]

        # запрещаем разворот
        best_action = None
        best_value = float("-inf")

        for a in range(4):

            if a == opposite[current_dir]:
                continue

            if q_values[a] > best_value:
                best_value = q_values[a]
                best_action = a

        # fallback (если вдруг всё запрещено)
        if best_action is None:
            best_action = random.randint(0, 3)

        self.current_direction = best_action
        return best_action

    def learn(self, state, action, reward, next_state, done):

        if state in self.last_states[-10:]:
            reward -= self.loop_penalty

        state = state = self.encode_state(state)
        next_state = self.encode_state(next_state)

        old_q = self.q_table[state][action]

        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self.q_table[next_state])

        self.q_table[state][action] = (old_q + self.lr * (target - old_q))
        self.last_states.append(state)
        if len(self.last_states) > 50:
            self.last_states.pop(0)

    def end_episode(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save_model(self):
        fname = "model/" + datetime.now().strftime("model_%Y%m%d_%H%M%S.json")
        data = {
            "q_table": {str(k): v for k, v in self.q_table.items()},
            "epsilon": self.epsilon,
            "current_direction": self.current_direction,
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
        self.current_direction = data["current_direction"]
        print(f"Model loaded from {filename}")
