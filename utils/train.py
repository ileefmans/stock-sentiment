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