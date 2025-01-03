from board import Board
class Game:
	"""
	Defines the state of the game
	"""
	def __init__(self, size: int, filled_number: int, lives: int = 3, score: int = 0):
		# parameters of the board
		self.size: int = size
		self.filled_number: int = filled_number

		# the board object
		self.board: Board = Board(size, filled_number)

		# the number of wrong guesses
		self.wrong_guesses: int = 0

		# the number of correctly guessed cells
		self.correct_guess_number: int = self.board.find_correctly_guessed_cells_number()

		self.lives: int = lives
		self.score: int = score
		self.level: int = 1

	def advance_level(self) -> None:
		if self.level % 2 == 0:  # Every second level, increase board size
			self.size += 1
		self.level += 1
		self.filled_number += 1  # Add one more filled tile per level
		self.board.reset_board(self.size, self.filled_number)

	def lose_life(self) -> bool:
		self.lives -= 1
		return self.lives > 0

	def reset_game(self) -> None:
		self.size = 3
		self.filled_number = 3
		self.lives = 3
		self.score = 0
		self.level = 1
		self.board.reset_board(self.size, self.filled_number)
