import numpy as np
import random
import pygame


class TicTacToe:
    def __init__(self):
        self.state_space = self.create_state_space()
        self.q_table = np.zeros((len(self.state_space), 9))
        self.learning_rate = 0.5 # 学习率
        self.discount_factor = 0.5 # 折扣因子
        self.epsilon = 0.1  # 探索因子

    def create_state_space(self):
        return ["".join([" "] * 9)]

    def get_available_actions(self, state):
        return [i for i in range(9) if state[i] == " "]

    def choose_action(self, state):
        if state not in self.state_space:
            self.state_space.append(state)
            self.q_table = np.vstack((self.q_table, np.zeros(9)))

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.get_available_actions(state))
        else:
            state_index = self.state_space.index(state)
            return np.argmax(self.q_table[state_index])

    def update_q_value(self, state, action, reward, next_state):
        if next_state not in self.state_space:
            self.state_space.append(next_state)
            self.q_table = np.vstack((self.q_table, np.zeros(9)))

        state_index = self.state_space.index(state)
        next_state_index = self.state_space.index(next_state)
        best_next_action = np.argmax(self.q_table[next_state_index])
        td_target = reward + self.discount_factor * self.q_table[next_state_index][best_next_action]
        self.q_table[state_index][action] += self.learning_rate * (td_target - self.q_table[state_index][action])


class Game:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None

    def reset(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None

    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
                return 1
            elif " " not in self.board:
                return 0
            self.current_player = "O" if self.current_player == "X" else "X"
        return None

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                return True
        return False


def draw_board(board):
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, (255, 255, 255), (j * 100, i * 100, 100, 100), 1)
            if board[i * 3 + j] == 'X':
                pygame.draw.line(screen, (255, 0, 0), (j * 100, i * 100), ((j + 1) * 100, (i + 1) * 100), 5)
                pygame.draw.line(screen, (255, 0, 0), ((j + 1) * 100, i * 100), (j * 100, (i + 1) * 100), 5)
            elif board[i * 3 + j] == 'O':
                pygame.draw.circle(screen, (0, 0, 255), (j * 100 + 50, i * 100 + 50), 45, 5)


pygame.init()
screen = pygame.display.set_mode((300, 300))

game = Game()
q_learning = TicTacToe()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game.winner is None and game.current_player == "X":
            x, y = event.pos
            row = y // 100
            col = x // 100
            position = row * 3 + col
            result = game.make_move(position)
            if result is not None:
                if game.winner:
                    print(f"{game.winner} 获胜！")
                else:
                    print("平局！")
                game.reset()

    if game.current_player == "O":
        state = "".join(game.board)
        action = q_learning.choose_action(state)
        game.make_move(action)

        reward = 1 if game.winner == "O" else -1 if game.winner == "X" else 0
        next_state = "".join(game.board)
        q_learning.update_q_value(state, action, reward, next_state)

        if game.winner:
            print(f"{game.winner} 获胜！")
            game.reset()
        elif " " not in game.board:
            print("平局！")
            game.reset()

    screen.fill((0, 0, 0))
    draw_board(game.board)
    pygame.display.flip()

pygame.quit()
