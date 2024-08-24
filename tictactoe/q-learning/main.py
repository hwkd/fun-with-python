#!/usr/bin/env python3

import sys
import signal
import numpy as np
import matplotlib.pyplot as plt

from game import GameEnv


def main():
    epsilon = 0.9  # exploration rate
    epsilon_min = 0.1  # minimum exploration rate
    decay = 0.99  # epsilon decay rate
    alpha = 0.1  # learning rate
    gamma = 0.95  # discount rate
    num_episodes = 10000

    env = GameEnv()
    q_table = np.zeros((env.state_space, env.action_space))
    all_rewards = []
    all_steps = []

    for episode in range(num_episodes):
        # Each episode is a new game.
        state = env.reset()
        gameover = False
        episode_reward = 0
        steps = 0

        # The agent is always player 0.
        while not gameover:
            # Determine the next move.
            if np.random.uniform(0, 1) < epsilon:
                # Random move.
                position = env.get_random_move()
            else:
                # Greedy move.
                position = random_argmax(q_table[state, :])

            # Every move returns the next state, reward and gameover status.
            next_state, reward, gameover = env.make_move(position)

            # Update q-table.
            q_table[state, position] = calc_q_value(
                q_table[state, position],
                np.max(q_table[next_state, :]),
                alpha,
                reward,
                gamma,
            )

            # env.display()

            # Player 1's random move.
            if not gameover:
                position = env.get_random_move()
                next_state, _, gameover = env.make_move(position)
                # env.display()

            state = next_state
            episode_reward += reward
            steps += 1

        # Decay the exploration rate after each episode.
        epsilon = max(epsilon_min, epsilon * decay)

        all_rewards.append(episode_reward)
        all_steps.append(steps)

    print("Average reward: ", np.mean(all_rewards))
    print("Average steps: ", np.mean(all_steps))

    _, axs = plt.subplots(1, 2, figsize=(14, 5))

    axs[0].plot(all_rewards)
    axs[0].set_xlabel("Episode")
    axs[0].set_ylabel("Accumulated Reward")
    axs[0].set_title("Q-Learning: Accumulated Reward per Episode")

    axs[1].plot(all_steps)
    axs[1].set_xlabel("Episode")
    axs[1].set_ylabel("Steps")
    axs[1].set_title("Q-Learning: Steps per Episode")

    plt.tight_layout()
    plt.show()


def calc_q_value(q_value, max_q_value, learning_rate, reward, decay):
    return q_value + learning_rate * (reward + decay * max_q_value - q_value)


def random_argmax(arr):
    # Find the maximum value in the array
    max_value = np.max(arr)

    # Find all indices where the array value equals the max value
    max_indices = np.flatnonzero(arr == max_value)

    # Randomly choose one of these indices
    return np.random.choice(max_indices)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda _x, _y: sys.exit(0))
    main()
