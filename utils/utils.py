from data import ScrapeWSB, Stock

class ScrapeWSBTest(ScrapeWSB):
	"""
		Class inheriting functionality of ScrapeWSB, to be run in unitest via Travis
	"""

	def __init__(self):
		super(ScrapeWSBTest, self).__init__()
		self.test = True

class StockTest(Stock):
	"""
		Class inheriting functionality of Stock, to be run in unitest via Travis
	"""

	def __init__(self):
		super(StockTest, self).__init__()
		self.test = True