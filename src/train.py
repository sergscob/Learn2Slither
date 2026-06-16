import argparse
import sys
from state import MapState
from plot import GamePlot
from agent import QAgent


def train(episode_count, show_freq, pring_freq, learn, grid_size, filename):
    agent = QAgent()
    env = MapState(grid_size)
    plot = GamePlot(grid_size, agent)
    userBreak = False
    max_steps = 0
    max_len = 0
    total_len = 0
    if (filename):
        agent.load_model(filename)

    for episode in range(episode_count):
        if userBreak:
            break

        state = env.reset()
        done = False
        episode_reward = 0
        steps = 0
        show = True if episode % show_freq == 0 else False
        if show:
            print(f"Show episode {episode}")

        while not done:
            action = agent.choose_action(state, learn)
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

            if learn:
                agent.learn(state, action, reward, next_state, done)
            state = next_state
            steps = steps + 1
            env.set_stat(episode, total_len+len(env.snake), steps)

        agent.end_episode()

        if episode % pring_freq == 0 or episode % show_freq == 0:
            print(
                f"ep: {episode} | "
                f"reward: {episode_reward:.1f} | "
                f"epsilon: {agent.epsilon:.2f} | "
                f"steps: {steps} | "
                f"snake_len: {len(env.snake)}"
            )
        max_steps = max(max_steps, steps)
        max_len = max(max_len, len(env.snake))
        total_len += len(env.snake)

    plot.show_final(env, episode+1, max_len, max_steps)
    print(f"\nTraining finished. episodes: {episode+1}."
          f" Max steps={max_steps}. Max snake len={max_len}."
          f" Average len: {round(total_len / (episode+1))}")
    if not userBreak:
        plot.wait_until_close(True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grid", default="10", help="grid size")
    parser.add_argument("-c", "--count", default="100000", help="episodes cnt")
    parser.add_argument("-s", "--show", default="10000", help="show freq")
    parser.add_argument("-p", "--print", default="100", help="print freq")
    parser.add_argument("-m", "--model", default="", help="model file")
    parser.add_argument("-l", "--learn", default=True, help="allow to learn")
    args = parser.parse_args()

    grid_size = int(args.grid) if args.grid.isdigit() else 0
    episode_count = int(args.count) if args.count.isdigit() else 0
    show_freq = int(args.show) if args.show.isdigit() else 0
    pring_freq = int(args.print) if args.print.isdigit() else 0
    learn = int(args.learn)

    if grid_size < 7 or grid_size > 20:
        print("\nGrid size must be between 7 and 20")
        sys.exit(1)
    if episode_count < 1 or episode_count > 1000000:
        print("\ncount must be between 1 and 1000000")
        sys.exit(1)
    if show_freq < 1:
        print("\nshow must be greater than 0")
        sys.exit(1)
    if pring_freq < 1:
        print("\nprint must be greater than 0")
        sys.exit(1)

    print("Start")
    print(f"Learn={learn}")
    print(f"Episodes count={episode_count}")
    print(f"Live show every {show_freq} episodes")
    print(f"Print result every {pring_freq} episodes")

    train(episode_count, show_freq, pring_freq, learn, grid_size, args.model)


if __name__ == "__main__":
    main()
