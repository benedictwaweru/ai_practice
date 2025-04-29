import tkinter as tk
from tkinter import messagebox
import time
import random
import math

class TicTacToe:
	def __init__(self, root):
		self.root = root
		self.root.title("Tic-Tac-Toe: Human vs AI")

		self.board = [" " for _ in range(9)]
		self.current_player = "X"
		self.game_active = False
		self.start_time = 0
		self.human_score = 0
		self.computer_score = 0
		self.ties = 0
		self.ai_algorithm = "minimax"
		
		self.setup_gui()
		
	def setup_gui(self):
		control_frame = tk.Frame(self.root)
		control_frame.pack(pady=10)
		
		algo_label = tk.Label(control_frame, text="AI Algorithm:")
		algo_label.grid(row=0, column=0, padx=5)

		self.algo_var = tk.StringVar(value="minimax")
		minimax_radio = tk.Radiobutton(control_frame, text="Minimax", variable=self.algo_var, 
																	value="minimax", command=self.set_algorithm)
		ab_radio = tk.Radiobutton(control_frame, text="Alpha-Beta", variable=self.algo_var, 
														 value="alphabeta", command=self.set_algorithm)
		minimax_radio.grid(row=0, column=1, padx=5)
		ab_radio.grid(row=0, column=2, padx=5)
		
		# Start button
		start_button = tk.Button(control_frame, text="New Game", command=self.start_new_game)
		start_button.grid(row=0, column=3, padx=10)
		
		# Score display
		score_frame = tk.Frame(self.root)
		score_frame.pack(pady=5)
		
		tk.Label(score_frame, text="Human (X):").grid(row=0, column=0)
		self.human_score_label = tk.Label(score_frame, text="0")
		self.human_score_label.grid(row=0, column=1, padx=5)
		
		tk.Label(score_frame, text="Computer (O):").grid(row=0, column=2)
		self.computer_score_label = tk.Label(score_frame, text="0")
		self.computer_score_label.grid(row=0, column=3, padx=5)
		
		tk.Label(score_frame, text="Ties:").grid(row=0, column=4)
		self.ties_label = tk.Label(score_frame, text="0")
		self.ties_label.grid(row=0, column=5, padx=5)
		
		# Timer display
		self.timer_label = tk.Label(self.root, text="Time: 0.00s", font=('Arial', 10))
		self.timer_label.pack()
		
		# Game board
		self.board_frame = tk.Frame(self.root)
		self.board_frame.pack(pady=10)
		
		self.buttons = []
		for i in range(9):
			row, col = divmod(i, 3)
			button = tk.Button(self.board_frame, text=" ", font=('Arial', 30), width=4, height=2,
											 command=lambda idx=i: self.human_move(idx))
			button.grid(row=row, column=col)
			self.buttons.append(button)
	
	def set_algorithm(self):
		self.ai_algorithm = self.algo_var.get()
	
	def start_new_game(self):
		# Reset board
		self.board = [" " for _ in range(9)]
		self.current_player = "X"
		self.game_active = True
		self.start_time = time.time()

		for i in range(9):
			self.buttons[i].config(text=" ", state=tk.NORMAL)
		
		self.update_timer()

		if random.choice([True, False]):
			self.current_player = "O"
			self.computer_move()
	
	def update_timer(self):
		if self.game_active:
			elapsed = time.time() - self.start_time
			self.timer_label.config(text=f"Time: {elapsed:.2f}s")
			self.root.after(100, self.update_timer)
	
	def human_move(self, position):
		if not self.game_active or self.current_player != "X" or self.board[position] != " ":
			return
			
		self.make_move(position, "X")
		
		if self.game_active:
			self.current_player = "O"
			self.computer_move()
	
	def computer_move(self):
		if not self.game_active or self.current_player != "O":
			return

		if self.ai_algorithm == "minimax":
			best_move = self.find_best_move_minimax()
		else:
			best_move = self.find_best_move_alphabeta()
		
		self.make_move(best_move, "O")
		self.current_player = "X"
	
	def make_move(self, position, player):
		self.board[position] = player
		self.buttons[position].config(text=player, state=tk.DISABLED)
		
		if self.check_winner(player):
			self.game_active = False
			elapsed = time.time() - self.start_time

			if player == "X":
				self.human_score += 1
				self.human_score_label.config(text=str(self.human_score))
				messagebox.showinfo("Game Over", f"You win! Time: {elapsed:.2f}s")
			else:
				self.computer_score += 1
				self.computer_score_label.config(text=str(self.computer_score))
				messagebox.showinfo("Game Over", f"Computer wins! Time: {elapsed:.2f}s")
		elif " " not in self.board:
			self.game_active = False
			elapsed = time.time() - self.start_time
			self.ties += 1
			self.ties_label.config(text=str(self.ties))
			messagebox.showinfo("Game Over", f"It's a tie! Time: {elapsed:.2f}s")
	
	def check_winner(self, player):
		# Check rows, columns, and diagonals
		win_conditions = [
			[0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
			[0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
			[0, 4, 8], [2, 4, 6]              # diagonals
		]
		
		for condition in win_conditions:
			if all(self.board[i] == player for i in condition):
				return True
		return False
	
	def find_best_move_minimax(self):
		best_score = -math.inf
		best_move = None
		
		for i in range(9):
			if self.board[i] == " ":
				self.board[i] = "O"
				score = self.minimax(self.board, 0, False)
				self.board[i] = " "
				
				if score > best_score:
					best_score = score
					best_move = i
		
		return best_move
	
	def minimax(self, board, depth, is_maximizing):
		if self.check_winner("O"):
			return 10 - depth
		if self.check_winner("X"):
			return -10 + depth
		if " " not in board:
			return 0
		
		if is_maximizing:
			best_score = -math.inf

			for i in range(9):
				if board[i] == " ":
					board[i] = "O"
					score = self.minimax(board, depth + 1, False)
					board[i] = " "
					best_score = max(score, best_score)

			return best_score
		else:
			best_score = math.inf

			for i in range(9):
				if board[i] == " ":
					board[i] = "X"
					score = self.minimax(board, depth + 1, True)
					board[i] = " "
					best_score = min(score, best_score)

			return best_score
	
	def find_best_move_alphabeta(self):
		best_score = -math.inf
		best_move = None
		
		for i in range(9):
			if self.board[i] == " ":
				self.board[i] = "O"
				score = self.alphabeta(self.board, 0, -math.inf, math.inf, False)
				self.board[i] = " "
				
				if score > best_score:
					best_score = score
					best_move = i
		
		return best_move
	
	def alphabeta(self, board, depth, alpha, beta, is_maximizing):
		if self.check_winner("O"):
				return 10 - depth
		if self.check_winner("X"):
				return -10 + depth
		if " " not in board:
				return 0
		
		if is_maximizing:
			best_score = -math.inf

			for i in range(9):
				if board[i] == " ":
					board[i] = "O"
					score = self.alphabeta(board, depth + 1, alpha, beta, False)
					board[i] = " "
					best_score = max(score, best_score)
					alpha = max(alpha, best_score)

					if beta <= alpha:
						break

			return best_score
		else:
			best_score = math.inf
			for i in range(9):
				if board[i] == " ":
					board[i] = "X"
					score = self.alphabeta(board, depth + 1, alpha, beta, True)
					board[i] = " "
					best_score = min(score, best_score)
					beta = min(beta, best_score)

					if beta <= alpha:
						break

			return best_score

if __name__ == "__main__":
	root = tk.Tk()
	game = TicTacToe(root)
	root.mainloop()
