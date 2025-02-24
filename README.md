Report
1.Introduce
This project, according to QLearning andgreedy algorithm, the completed chess game, and combined with Pygame to achieve the vision of the game. And give the core ideas and code ideas of Qlearning, as well as the specific implementation details.
Q-learning (Watkins, 1989) is a simple way for agents to learn how to act optimally in controlled Markovian domains. It amounts to an incremental method for dynamic programming which imposes limited computational demands. It works by successively improving its evaluations of the quality of particular actions at particular states.[1]
The nature of greedy selection means that when faced with a problem and needs to make a decision, the greedy algorithm will give preference to the solution that currently seems optimal, regardless of the global optimal solution. The key to greedy choice is that the choice at each step must be locally optimal,even if this choice may result in the final result not necessarily being globally optimal.Greedy selection is generally suitable for satisfying problems with specific properties that have optimal substructure properties and that produce optimal solutions. The optimal substructure property means that the overall optimal solution to the problem can be achieved by a series of local optimal choices.[2]
2.Project design and structure
This project is divided into the following modules:Q Learning module: a reinforcement learning algorithm for training AI.Game state management module: to realize the rules and logic of the game.Pygame Visualization module: Provide the game's graphical interface and user interaction.Each module plays a different role in the project, and its function and implementation are described in detail below.
3.Q-learning
The Q learning module is implemented by class TicTacToe. Its main functions include: initializing the state space and the Q table;Action selection based on the greedy policy; the Q-value update.
3.1状态空间的表示
The state space represents all possible board states of the board. Each state is represented by a string of length 9:" "Empty position; "X" is a piece of player X; and "O" is a piece of player O.
The initial state is an fully empty board:
self.state_space = ["".join([" "] * 9)]  
Action choice
In each round of decision, the program selects actions based on the greedy strategy：
if random.uniform(0, 1) < self.epsilon:
    return random.choice(self.get_available_actions(state))  
else:
    state_index = self.state_space.index(state)
    return np.argmax(self.q_table[state_index])  
Q value update
Update the current Q value for the best action for rewards and future status:
def update_q_value(self, state, action, reward, next_state):
    state_index = self.state_space.index(state)
    next_state_index = self.state_space.index(next_state)
    best_next_action = np.argmax(self.q_table[next_state_index])
    td_target = reward + self.discount_factor * self.q_table[next_state_index][best_next_action]
    self.q_table[state_index][action] += self.learning_rate * (td_target - self.q_table[state_index][action])
4.Game status management
Game status management is implemented by the Game class, and its main functions include:Board initialization;Action execution;Check that the game is over.
4.1 Board initialization
The checkboard is represented by a list of length 9, with a position corresponding to each element:
self.board = [" "] * 9
4.2 Action execution and status update
After the player drops, the program updates the board status and checks that the game is over:
def make_move(self, position):
    if self.board[position] == " ":
        self.board[position] = self.current_player
        if self.check_winner():
            self.winner = self.current_player
            return 1  # win
        elif " " not in self.board:
            return 0  # pingju
        self.current_player = "O" if self.current_player == "X" else "X"
    return None  # continue game
4.3 Victory condition inspection
Determine if a player wins by going through all possible winning combinations：
def check_winner(self):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # row
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # column
        [0, 4, 8], [2, 4, 6]              # diagonal
    ]
    for combo in winning_combinations:
        if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
            return True
    return False
5.Pygame
Pygame A graphical interface to provide game interaction with users, including board drawing, piece drawing, and mouse event processing.
Board drawing
3x3 grids are drawn through pygame.draw.rect as a well-written chess board
for i in range(3):
    for j in range(3):
        pygame.draw.rect(screen, (255, 255, 255), (j*100, i*100, 100, 100), 1)

5.1 Chess-piece drawing
Mark the player according to the board status:Player X is marked as the red "X";Player O is marked as the blue "O"
if board[i*3+j] == 'X':
    pygame.draw.line(screen, (255, 0, 0), (j*100, i*100), ((j+1)*100, (i+1)*100), 5)
    pygame.draw.line(screen, (255, 0, 0), ((j+1)*100, i*100), (j*100, (i+1)*100), 5)
elif board[i*3+j] == 'O':
    pygame.draw.circle(screen, (0, 0, 255), (j*100 + 50, i*100 + 50), 45, 5)
5.2User interaction
By listening to mouse click events, allowing the user to select the checkerboard position and interaction:
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
6. Summary and improvement direction
	
This project implements a complete well chess system through Q learning algorithm and Pygame, showing the application of reinforcement learning in classic games. Although it is simple, it provides a good starting point for the study of AI decisions. Through training, gradually learn how to choose the optimal action in different states, can effectively against human players.
6.1brightened dot
Application of reinforcement learning: the Q learning algorithm is used to enable to learn the optimal strategy of Chinese chess through trial and error and reward.
Greed strategy: achieves the balance between exploration and utilization, ensuring that AI can fully explore the state space in the early stage of training and gradually optimize the strategy in the later stage.
Game logic and Visualization: The Pygame provides an intuitive, user-friendly interface for players to clearly observe and interact with the AI decision-making process.
Modular design: separate Q learning, game logic and visualization, make the code clear and easy to read, easy to expand and maintain
6.2 shortcoming
In the early stage of learning, because the state space has not been fully explored, its strategies are relatively random and easy to make mistakes.
With the progress of learning, gradually mastered the basic rules of well word chess, and learned the defense and offensive strategy. After enough training, you can achieve a near-optimal strategy, and most probably avoid losing to the player.Users can play the real-time battle through the Pygame interface,
7.reference
[1]Watkins, Christopher JCH, and Peter Dayan. "Q-learning." Machine learning 8 (1992): 279-292.
[2]Wang,Y. (2023).Review on greedy algorithm.Theoretical and Natural Science,14,233-239.
[3]Sutton, Richard S., and Andrew G. Barto. Reinforcement learning: An introduction. Vol. 1. No. 1. Cambridge: MIT press, 1998.
[4]Szepesvári, Csaba. Algorithms for reinforcement learning. Springer nature, 2022.
