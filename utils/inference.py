import torch
from torch import nn
from torch.utils.data import DataLoader
from datahelper import PostDataset, CommentDataset, get_indices
from models import SentimentModel
import yaml
from tqdm import tqdm



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
			self.model = SentimentModel().to(self.device)

		self.stock_id = stock_id

		self.indices = get_indices(self.stock_id, inference=True)

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

			total_probs = torch.zeros([2])
			for post in tqdm(self.post_dataloader, desc='Determining Sentiment From Posts: '):
				input_ids = post['post_input_ids'].to(self.device)
				attention_masks = post['post_attention_mask'].to(self.device)

				output = self.model(input_ids=input_ids, attention_masks=attention_masks)
				softmax = nn.Softmax(dim=1)
				probs= softmax(output.logits)
				total_probs += probs.mean(dim=0)

			avg_probs = total_probs/len(self.post_dataloader)

			return avg_probs


if __name__ == '__main__':
	run =RunInference('GME')
	print(run.evaluate())









