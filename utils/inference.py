import torch
from torch.utils.data import DataLoader
from datahelper import Dataset, get_indices
from models import SentimentModel
import yaml



def pull():

	"""
		Helper function that checks whether or not knew reddit comments and posts need to be scraped
	"""
	pass


def get_config():
    with open("config.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config['Inference']


class RunInference:
	"""
		Class for running inference to gather stock sentiment
	"""
	def __init__(self, stock_id):

		self.config = get_config()


		self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
		
		if self.config['model']=='pretrained':
			self.model = SentimentModel.to(self.device)

		self.stock_id = stock_id

		self.indices = get_indices(self.stock_id, inference=True)

		self.data = Dataset(max_len, self.indices['post_ids'], self.indices['comment_ids'])

		self.dataloader = DataLoader(dataset=self.data, 
									 batch_size=self.config['batch_size'], 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )





		

