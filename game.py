from board import Board
class Game:
	"""
	Defines the state of the game
	"""
	def __init__(self, size: int, filled_number: int):
		# parameters of the board
		self.size: int = size
		self.filled_number: int = filled_number

		# the board object
		self.board: Board = Board(size, filled_number)

		# the number of wrong guesses
		self.wrong_guesses: int = 0

		# the number of correctly guessed cells
		self.correct_guess_number: int = self.board.find_correctly_guessed_cells_number()

	def update_correct_guess_number(self) -> None:
		"""
		Updates the correct guess number by counting the number of cells that are both filled and discovered
		:return: the number of correct guesses
		"""
		self.correct_guess_number = self.board.find_correctly_guessed_cells_number()

game = Game(5, 4)
game.board.board[0][0].is_discovered = True
game.board.board[0][0].is_filled = True

game.update_correct_guess_number()
print(game.board)
print(game.correct_guess_number)
