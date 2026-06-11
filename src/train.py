from state import MapState
from plot import plot
from agent import QAgent


SIZE = 10

agent = QAgent()
env = MapState(SIZE)

for episode in range(10):

    state = env.reset()
    done = False

    while not done:

        action = agent.choose_action(state)

        next_state, reward, done = env.step(action)

        agent.learn(
            state,
            action,
            reward,
            next_state,
            done
        )

        state = next_state

    agent.end_episode()        