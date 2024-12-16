class Cell:
	"""
	Represents a single cell in a Board
	"""
	def __init__(self, x, y, is_filled: bool = False, is_discovered: bool = False):
		# coordinates of a cell
		self.x = x
		self.y = y

		# True if the cell is filled
		self.is_filled = is_filled
		# True if the cell is discovered
		self.is_discovered = is_discovered

	def __str__(self):
		line = ""
		line += "+F" if self.is_filled else "-F"
		line += "+D" if self.is_discovered else "-D"
		return line
