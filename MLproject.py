import numpy as np
import random
import pygame


# Q学习部分
class TicTacToe:
    def __init__(self):
        self.state_space = self.create_state_space()
        self.q_table = np.zeros((len(self.state_space), 9))  # 9 possible actions
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1  # Exploration rate

    def create_state_space(self):
        return ["".join([" "] * 9)]  # 初始状态为空棋盘

    def get_available_actions(self, state):
        return [i for i in range(9) if state[i] == " "]

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.get_available_actions(state))  # 随机选择动作
        else:
            state_index = self.state_space.index(state)
            return np.argmax(self.q_table[state_index])  # 选择最大Q值的动作

    def update_q_value(self, state, action, reward, next_state):
        state_index = self.state_space.index(state)
        next_state_index = self.state_space.index(next_state)
        best_next_action = np.argmax(self.q_table[next_state_index])
        td_target = reward + self.discount_factor * self.q_table[next_state_index][best_next_action]
        self.q_table[state_index][action] += self.learning_rate * (td_target - self.q_table[state_index][action])


# 游戏状态管理
class Game:
    def __init__(self):
        self.board = [" "] * 9  # 初始化棋盘
        self.current_player = "X"  # "X"先手
        self.winner = None  # 跟踪赢家

    def reset(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None

    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
                return 1  # 赢
            elif " " not in self.board:
                return 0  # 平局
            self.current_player = "O" if self.current_player == "X" else "X"
        return None  # 继续游戏

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 行
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 列
            [0, 4, 8], [2, 4, 6]  # 对角线
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                return True
        return False


# Pygame部分
def draw_board(board):
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, (255, 255, 255), (j * 100, i * 100, 100, 100), 1)
            if board[i * 3 + j] == 'X':
                pygame.draw.line(screen, (255, 0, 0), (j * 100, i * 100), ((j + 1) * 100, (i + 1) * 100), 5)
                pygame.draw.line(screen, (255, 0, 0), ((j + 1) * 100, i * 100), (j * 100, (i + 1) * 100), 5)
            elif board[i * 3 + j] == 'O':
                pygame.draw.circle(screen, (0, 0, 255), (j * 100 + 50, i * 100 + 50), 45, 5)


# 初始化Pygame
pygame.init()
screen = pygame.display.set_mode((300, 300))
game = Game()

# 运行游戏
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game.winner is None:
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
                game.reset()  # 重置游戏

    screen.fill((0, 0, 0))
    draw_board(game.board)  # 更新棋盘状态
    pygame.display.flip()

pygame.quit()
