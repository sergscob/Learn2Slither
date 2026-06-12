import argparse
from state import MapState
from plot import GamePlot
from agent import QAgent


SIZE = 10


def train(episode_count):
    agent = QAgent()
    env = MapState(SIZE)
    plot = GamePlot(SIZE)
    userBreak = False

    for episode in range(episode_count):

        state = env.reset()
        done = False
        show = True if episode % 1000 == 0 else False
        episode_reward = 0
        while not done:

            action = agent.choose_action(state)
            if action == 0:   # UP
                dx, dy = 0, -1
            elif action == 1: # DOWN
                dx, dy = 0, 1
            elif action == 2: # LEFT
                dx, dy = -1, 0
            elif action == 3: # RIGHT
                dx, dy = 1, 0

            env.changeDirection(dx, dy)
            next_state, reward, done = env.move()
            episode_reward += reward
            if show: 
                userBreak = plot.tick(env)
            if userBreak:
                break

            agent.learn(state, action, reward, next_state, done)
            state = next_state

        agent.end_episode()        
        if episode % 50 == 0:
            print(
                "ep:", episode,
                "reward:", int(episode_reward),
                "epsilon:", agent.epsilon,
                "snake_len:", len(env.snake)
            )
        if userBreak:
            break            
    plot.end()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", default="result/model.json", help="episode_count")
    # parser.add_argument("-d", "--data", default="data/valid.csv", help="path to dataset for prediction")
    args = parser.parse_args()
    train(args.count)


if __name__ == "__main__":
    main()