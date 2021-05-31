import torch
from torch import nn
from torch.utils.data import DataLoader
from transformers import AdamW, get_linear_schedule_with_warmup
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

		# Optimizer
		self.optimizer = AdamW(model.parameters(),lr=2e-5, correct_bias=False)

		# Set up learning rate scheduler
		total_steps = (len(self.post_trainloader) + len(self.comment_trainloader)) * self.config['epochs']
		self.scheduler = get_linear_schedule_with_warmup(
			optimizer,
			num_warmup_steps=0,
			num_training_steps=total_steps
			)

		# Initialize Loss Function
		loss_fcn = nn.CrossEntropyLoss().to(device)



