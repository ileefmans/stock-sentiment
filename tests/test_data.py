import unittest
import utils

class test_ScrapeWSB(unittest.TestCase):

	def test_equal_comment_posts(self):
		self.assertEqual(len(ScrapeWSB("GME", 10, 10).process()), 10)
	print("DONE SCRAPE TEST")
