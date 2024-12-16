import random
from cell import Cell
from itertools import chain
from typing import List

class Board:
	"""
	This class represents the board of the game. Essentially, this class stores the current configuration of the game.
	This includes which cells have to be remembered, and which ones have been chosen by the player
	"""
	def __init__(self, size: int, filled_number: int) -> None:
		# the size of the playing board
		self.size: int = size

		# the number of squares that you have to remember
		self.filled_number = filled_number
		assert filled_number <= size**2/2, "The number of filled numbers exceeds the half of the total number of elements"

		self.board = self.create_board()

	def __str__(self) -> str:
		result = ""
		for row in self.board:
			line = ""
			for cell in row:
				line += str(cell) + " "
			result += line + "\n"
		return result

	def create_board(self) -> List[List[Cell]]:
		board = list()
		for x in range(self.size):
			row = []
			for y in range(self.size):
				cell = Cell(x, y)
				row.append(cell)
			board.append(row)

		filled_coords = set()

		while len(filled_coords) < self.filled_number:
			x = random.randint(0, self.size - 1)
			y = random.randint(0, self.size - 1)
			filled_coords.add((x, y))

		for coord in filled_coords:
			board[coord[0]][coord[1]].is_filled = True

		return board

	def find_correctly_guessed_cells_number(self) -> int:
		return sum(cell.is_discovered and cell.is_filled for cell in chain.from_iterable(self.board))


# b = Board(5, 4)
# print(b)