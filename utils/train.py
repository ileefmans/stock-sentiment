import torch
from torch import nn
from torch.utils.data import DataLoader
from datahelper import PostDataset, CommentDataset, get_indices
from models import SentimentModel
import yaml
from tqdm import tqdm



def get_config():
    with open("config.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config['Training']


class Train:
	"""
		Class for finetuning BERT
	"""
	def __init__(self):

		self.config = get_config()

		self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

		if self.config['model']=='pretrained':
			self.model = SentimentModel().to(self.device)
		elif self.config['model'] == 'finetuned':
			pass ########### INSERT MODEL FOR FINETUNING HERE

		self.indices = get_indices("no_stock_id")

		# Create PyTorch Datasets and instantiate PyTorch Dataloaders
		self.post_train = PostDataset(self.config['embedding_max_len'], 
									  self.indices['post_train']
									 )
		self.post_test = PostDataset(self.config['embedding_max_len'], 
									 self.indices['post_test']
									)
		self.comment_train = CommentDataset(self.config['embedding_max_len'], 
											self.indices['comment_train']
											)
		self.comment_test = CommentDataset(self.config['embedding_max_len'], 
										   self.indices['comment_test']
										   )

		self.post_trainloader = DataLoader(dataset=self.post_train, 
									 batch_size=self.config['batch_size'], 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )
		self.post_testloader = DataLoader(dataset=self.post_test, 
									 batch_size=self.config['batch_size'], 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )
		self.comment_trainloader = DataLoader(dataset=self.comment_train, 
									 batch_size=self.config['batch_size'], 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )
		self.comment_testloader = DataLoader(dataset=self.comment_test, 
									 batch_size=self.config['batch_size'], 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )





