import torch
from torch import nn
from torch.utils.data import DataLoader
from datahelper import PostDataset, CommentDataset, get_indices
from data import Database
from models import SentimentModel
import yaml
from tqdm import tqdm



def pull(value, stock_id num_posts, num_comments, increment='HOUR'):

	"""
		Helper function that checks whether or not knew reddit comments and posts need to be scraped

		Args:

			value (int): 	Value of desired increment ex: if value=24 and increment='HOUR' rescrape if 
							last scraping ocurred more than 24 hours ago
			increment (str): Desired increment either 'HOUR' or 'DAY'
	"""


	db = Database()
	db.use_database('DB1')
	if len(db.query("SELECT * FROM STOCKS WHERE STOCK_ID='{}}' AND LAST_SCRAPED >= DATE_SUB(NOW(),INTERVAL {} {})".format(stock_id, value, increment)))==0:
		
		scrapewsb = ScrapeWSB(stock_id, num_posts, num_comments)

		df = scrapewsb.scrape()
		scrapewsb.convert(df)

	return


def get_config():
	"""
		Helper function to get configuration
	"""
    with open("config.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config['Inference']


class RunInference:
	"""
		Class for running inference to gather stock sentiment
	"""
	def __init__(self, stock_id, scrape_time=6):
		"""
			Args:

			 	stock_id (str): 	Symbol of stock to run inference on
			 	scrape_time (int):	Interval of time prior to scraping timestamp from which to use 
			 						comments and posts (Not meant to be externally manipulated)
		"""

		self.config = get_config()


		self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
		
		if self.config['model']=='pretrained':
			self.model = SentimentModel().to(self.device)

		elif self.config['model']=='finetuned':
			self.model = torch.load("models/finetuned.pt")
			

		self.stock_id = stock_id

		self.indices = get_indices(self.stock_id, inference=True, scrape_time=scrape_time)

		self.post_data = PostDataset(self.config['embedding_max_len'], 
									 self.indices['post_ids']
									 )
		self.comment_data = CommentDataset(self.config['embedding_max_len'], 
										   self.indices['comment_ids']
										   )

		self.post_dataloader = DataLoader(dataset=self.post_data, 
									 batch_size=self.config['batch_size'], 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )
		self.comment_dataloader = DataLoader(dataset=self.comment_data, 
									 batch_size=self.config['batch_size'], 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )

	def evaluate(self):

		# Set model to evaluate
		with torch.no_grad():

			total_post_probs = torch.zeros([2])
			for post in tqdm(self.post_dataloader, desc='Determining Sentiment From Posts: '):
				post_input_ids = post['post_input_ids'].to(self.device)
				post_attention_masks = post['post_attention_mask'].to(self.device)

				post_output = self.model(input_ids=post_input_ids, attention_masks=post_attention_masks)
				softmax = nn.Softmax(dim=1)
				post_probs= softmax(post_output.logits)
				total_post_probs += post_probs.mean(dim=0)

			avg_post_probs = total_post_probs/len(self.post_dataloader)


			total_comment_probs = torch.zeros([2])
			for comment in tqdm(self.comment_dataloader, desc='Determining Sentiment From Comments: '):
				comment_input_ids = comment['comment_input_ids'].to(self.device)
				comment_attention_masks = comment['comment_attention_mask'].to(self.device)

				comment_output = self.model(input_ids=comment_input_ids, attention_masks=comment_attention_masks)
				softmax = nn.Softmax(dim=1)
				comment_probs= softmax(comment_output.logits)
				total_comment_probs += comment_probs.mean(dim=0)

			avg_comment_probs = total_comment_probs/len(self.comment_dataloader)


			return {'avg_post_probs': avg_post_probs,
					'avg_comment_probs': avg_comment_probs
					}


if __name__ == '__main__':
	run =RunInference('GME')
	print(run.evaluate())









