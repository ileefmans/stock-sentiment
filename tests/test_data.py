import unittest
import utils
import pandas as pd

class test_ScrapeWSB(unittest.TestCase):

	def setUp(self):
		o = [1,1,1]
		h = [4,4,4]
		l = [0.5, 0.5, 0.5]
		c = [2,2,2]
		v = [250, 250, 300]
		t = [556733, 5733677, 5983000]
		s = ['ok', 'ok', 'ok']

		df = {'o': o, 'h': h, 'l': l, 'c': c, 'v': v, 't': t, 's': s}

		self.df = pd.DataFrame(df)




	def test_convert(self):
		self.assertEqual(utils.ScrapeWSB("GME", 10, 10).convert()['open'], [1,1,1])

	# def test_equal_comment_posts(self):
	# 	self.assertEqual(len(utils.ScrapeWSB("GME", 10, 10).process()), 10)
	print("DONE SCRAPE TEST")


