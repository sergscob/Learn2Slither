import argparse
import sys
from state import MapState
from plot import GamePlot
from agent import QAgent

SIZE = 10


def train(episode_count, show_shaque):
    agent = QAgent()
    env = MapState(SIZE)
    plot = GamePlot(SIZE, agent)
    userBreak = False

    for episode in range(episode_count):
        if userBreak:
            break

        state = env.reset()
        done = False
        episode_reward = 0
        show = True if episode % show_shaque == 0 else False
        if show:
            print(f"Show episode {episode}")

        while not done:
            action = agent.choose_action(state)
            if action == 0:   # FORWARD
                dx, dy = env.direction[0], env.direction[1]
            elif action == 1:  # LEFT
                dx, dy = env.direction[1], -env.direction[0]
            elif action == 2:  # RIGHT
                dx, dy = -env.direction[1], env.direction[0]

            env.changeDirection(dx, dy)
            next_state, reward, done = env.move()
            episode_reward += reward

            if show:
                userBreak = plot.tick(env, state)
            else:
                userBreak = plot.checkPressButtons(env)
            if userBreak:
                break
            if plot.paused:
                userBreak = plot.wait_until_close(False)

            agent.learn(state, action, reward, next_state, done)
            state = next_state

        agent.end_episode()

        if episode % 100 == 0 or episode % show_shaque == 0:
            print(
                f"ep: {episode} | "
                f"reward: {episode_reward:.1f} | "
                f"epsilon: {agent.epsilon:.2f} | "
                f"snake_len: {len(env.snake)}"
            )

    print(f"\nTraining finished. episodes: {episode+1}.")
    if not userBreak:
        plot.wait_until_close(True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", default="100000", help="episodes cnt")
    parser.add_argument("-s", "--show", default="10000", help="show game")
    args = parser.parse_args()
    episode_count = int(args.count) if args.count.isdigit() else 0
    show_shaque = int(args.show) if args.show.isdigit() else 0
    if episode_count < 1 or episode_count > 1000000:
        print("\ncount must be between 1 and 1000000")
        sys.exit(1)
    if show_shaque < 1:
        print("\nshow must be greater than 0")
        sys.exit(1)

    train(episode_count, show_shaque)


if __name__ == "__main__":
    main()
