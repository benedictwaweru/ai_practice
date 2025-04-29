import time
import math
from copy import deepcopy

class TicTacToe:
	def __init__(self):
		self.board = [[' ' for _ in range(3)] for _ in range(3)]
		self.current_player = 'X'
		self.game_over = False
		self.winner = None
		self.move_history = []

	def print_board(self):
		for row in self.board:
			print('|' + '|'.join(row) + '|')
		print()

	def make_move(self, row, col):
		if self.game_over or self.board[row][col] != ' ':
			return False

		self.board[row][col] = self.current_player
		self.move_history.append((row, col, self.current_player))

		if self.check_winner(row, col):
			self.game_over = True
			self.winner = self.current_player
		elif self.is_board_full():
			self.game_over = True
		else:
			self.current_player = 'O' if self.current_player == 'X' else 'X'

		return True

	def check_winner(self, row, col):
		# Check row
		if all([cell == self.current_player for cell in self.board[row]]):
			return True
		# Check column
		if all([self.board[i][col] == self.current_player for i in range(3)]):
			return True
		# Check diagonals
		if row == col and all([self.board[i][i] == self.current_player for i in range(3)]):
			return True
		if row + col == 2 and all([self.board[i][2-i] == self.current_player for i in range(3)]):
			return True

		return False

	def is_board_full(self):
		return all([cell != ' ' for row in self.board for cell in row])

	def get_available_moves(self):
		return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

	def undo_move(self):
		if not self.move_history:
				return

		row, col, player = self.move_history.pop()
		self.board[row][col] = ' '
		self.current_player = player
		self.game_over = False
		self.winner = None

"""
Acts as a guide for the algorithm to choose the most favourable outcome for the player it's representing
"""
def evaluate_board(game):
	if game.winner == 'X':
			return 1
	elif game.winner == 'O':
			return -1
	else:
			return 0

def minimax(game, depth, is_maximizing):
	# Check the base case, i.e., the terminal state, meaning the game ended in a win, loss or draw
	# It calls the evaluate_board() to assign a score based on the outcome
	if game.game_over:
		return evaluate_board(game)

	"""
	With the base case in place, the algorithm explores the game tree recursively.
	"""
	if is_maximizing:
		max_eval = -math.inf

		for move in game.get_available_moves():
			game.make_move(*move)
			evaluation = minimax(game, depth + 1, False)
			game.undo_move()
			max_eval = max(max_eval, evaluation)

		return max_eval
	else:
			min_eval = math.inf
			for move in game.get_available_moves():
					game.make_move(*move)
					evaluation = minimax(game, depth + 1, True)
					game.undo_move()
					min_eval = min(min_eval, evaluation)
			return min_eval

# This function allows the algorithm to choose the most favourable option for the player it's representing via backtracking
def get_best_move_minimax(game):
		best_move = None
		best_eval = -math.inf if game.current_player == 'X' else math.inf

		for move in game.get_available_moves():
				game.make_move(*move)
				evaluation = minimax(game, 0, game.current_player == 'X')
				game.undo_move()

				if game.current_player == 'X':
						if evaluation > best_eval:
								best_eval = evaluation
								best_move = move
				else:
						if evaluation < best_eval:
								best_eval = evaluation
								best_move = move

		return best_move

def alphabeta(game, depth, alpha, beta, is_maximizing):
		# Check the base case, i.e., the terminal state, meaning the game ended in a win, loss or draw
		# It calls the evaluate_board() to assign a score based on the outcome
		if game.game_over:
				return evaluate_board(game)

		if is_maximizing:
				max_eval = -math.inf
				for move in game.get_available_moves():
						game.make_move(*move)
						evaluation = alphabeta(game, depth + 1, alpha, beta, False)
						game.undo_move()
						max_eval = max(max_eval, evaluation)
						alpha = max(alpha, evaluation)

						if beta <= alpha:
								break
				return max_eval
		else:
				min_eval = math.inf
				for move in game.get_available_moves():
						game.make_move(*move)
						evaluation = alphabeta(game, depth + 1, alpha, beta, True)
						game.undo_move()
						min_eval = min(min_eval, evaluation)
						beta = min(beta, evaluation)
						if beta <= alpha:
								break
				return min_eval

def get_best_move_alphabeta(game):
		best_move = None
		best_eval = -math.inf if game.current_player == 'X' else math.inf
		alpha = -math.inf
		beta = math.inf

		for move in game.get_available_moves():
				game.make_move(*move)
				evaluation = alphabeta(game, 0, alpha, beta, game.current_player == 'X')
				game.undo_move()

				if game.current_player == 'X':
						if evaluation > best_eval:
								best_eval = evaluation
								best_move = move
						alpha = max(alpha, evaluation)
				else:
						if evaluation < best_eval:
								best_eval = evaluation
								best_move = move
						beta = min(beta, evaluation)

		return best_move

""" def play_game(algorithm):
		game = TicTacToe()
		move_count = 0

		while not game.game_over:
				move_count += 1
				if algorithm == 'minimax':
						move = get_best_move_minimax(game)
				else:
						move = get_best_move_alphabeta(game)

				game.make_move(*move)

		return game.winner, move_count """

""" def play_game(algorithm):
    game = TicTacToe()
    move_count = 0

    while not game.game_over:
        move_count += 1
        if algorithm == 'minimax':
            if game.current_player == 'X':
                move = get_best_move_minimax(game)
            else:
                move = get_best_move_minimax(game)  # O also thinks
        else:
            if game.current_player == 'X':
                move = get_best_move_alphabeta(game)
            else:
                move = get_best_move_alphabeta(game)  # O also thinks

        game.make_move(*move)

    return game.winner, move_count

def compare_algorithms():
		num_games = 10
		algorithms = ['minimax', 'alphabeta']

		for algo in algorithms:
				total_time = 0
				results = {'X': 0, 'O': 0, None: 0}

				print(f"\nTesting {algo} algorithm:")
				for _ in range(num_games):
						start_time = time.time()
						winner, moves = play_game(algo)
						end_time = time.time()

						total_time += (end_time - start_time)
						results[winner] += 1

				avg_time = total_time / num_games
				print(f"Results after {num_games} games:")
				print(f"X wins: {results['X']}, O wins: {results['O']}, Draws: {results[None]}")
				print(f"Average time per game: {avg_time:.6f} seconds")

# Run the comparison
compare_algorithms()
 """

def play_game(algorithm, print_final=False):
    game = TicTacToe()
    move_count = 0

    while not game.game_over:
        move_count += 1
        if algorithm == 'minimax':
            move = get_best_move_minimax(game)
        else:
            move = get_best_move_alphabeta(game)

        game.make_move(*move)

    if print_final:
        print("\nFinal Board State:")
        game.print_board()
        if game.winner:
            print(f"Player {game.winner} wins!")
        else:
            print("The game ended in a draw!")
        print(f"Total moves: {move_count}\n")

    return game.winner, move_count

def compare_algorithms(print_boards=False):
    num_games = 10
    algorithms = ['minimax', 'alphabeta']

    for algo in algorithms:
        total_time = 0
        results = {'X': 0, 'O': 0, None: 0}

        print(f"\nTesting {algo} algorithm:")
        for game_num in range(num_games):
            start_time = time.time()
            winner, moves = play_game(algo, print_boards)
            end_time = time.time()

            total_time += (end_time - start_time)
            results[winner] += 1

            if print_boards:
                print(f"Game {game_num + 1} result: {'X won' if winner == 'X' else 'O won' if winner == 'O' else 'Draw'}")

        avg_time = total_time / num_games
        print(f"\nResults after {num_games} games:")
        print(f"X wins: {results['X']}, O wins: {results['O']}, Draws: {results[None]}")
        print(f"Average time per game: {avg_time:.6f} seconds")

# Run the comparison with board printing enabled
compare_algorithms(print_boards=True)
