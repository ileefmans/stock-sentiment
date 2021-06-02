import torch
from torch import nn
from torch.utils.data import DataLoader
from transformers import AdamW, get_linear_schedule_with_warmup
from datahelper import PostDataset, CommentDataset, get_indices
from models import SentimentModel
import yaml
from tqdm import tqdm
import argparse



def get_config():
    with open("config.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config['Training']


def get_args():
	parser = argparse.ArgumentParser(description="Model Options")
	parser.add_argument(
		"--local",
		type=bool,
		default=True,
		help="True if running on local machine, False if running on AWS",
		)
	return parser.parse_args()



class Train:
	"""
		Class for finetuning BERT
	"""
	def __init__(self):

		self.config = get_config()
		self.ops = get_args()
		self.local = self.ops.local

		self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

		# Num Epochs
		self.epochs = self.config['epochs']

		# Batch Size
		self.batch_size = self.config['batch_size']

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
									 batch_size=self.batch_size, 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )
		self.post_testloader = DataLoader(dataset=self.post_test, 
									 batch_size=self.batch_size, 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )
		self.comment_trainloader = DataLoader(dataset=self.comment_train, 
									 batch_size=self.batch_size, 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )
		self.comment_testloader = DataLoader(dataset=self.comment_test, 
									 batch_size=self.batch_size, 
									 num_workers=self.config['num_workers'],
									 shuffle=self.config['shuffle']
									 )

		# Optimizer
		self.optimizer = AdamW(model.parameters(),lr=2e-5, correct_bias=False)

		# Set up learning rate scheduler
		total_steps = (len(self.post_trainloader) + len(self.comment_trainloader)) * self.epochs
		self.scheduler = get_linear_schedule_with_warmup(
			optimizer,
			num_warmup_steps=0,
			num_training_steps=total_steps
			)

		# Initialize Loss Function
		loss_fcn = nn.CrossEntropyLoss().to(device)


	def train(self):
		if not self.local:
			torch.set_default_tensor_type(torch.cuda.FloatTensor)
			print("\n \n EVERYTHING TO CUDA \n \n")


		start_epoch = 0
		total_loss = 0
		summed_acc = 0
		# Start Training Loop
		for epoch in range(start_epoch, self.epochs+1):

			# Train
			if epoch>0:


				epoch_loss = 0
				total_epoch_acc = 0
				# Set model to training mode
				self.model.train()
				for post_batch in tqdm(self.post_trainloader, desc='Train Epoch {}'.format(epoch)):

					# Send input ids and attention masks to device
					post_input_ids = post_batch['post_input_ids'].to(self.device)
					post_attention_masks = post_batch['post_attention_mask'].to(self.device)
					post_targets = post_batch['target'].reshape(-1,2).to(self.device)

					post_output = self.model(input_ids=post_input_ids, attention_masks=post_attention_masks)

					# Calculate Loss
					loss = loss_fcn(post_output, post_targets)

					# Make Predictions
					_, preds = torch.max(post_output, dim=1)
					_, ground_truths = torch.max(post_targets, dim=1)

					# Calculate Accuracy
					acc = torch.sum(preds==ground_truths)/len(preds)

					epoch_loss+=loss
					total_epoch_acc+=acc

					# Clear optimizer gradient
					self.optimizer.zero_grad()

					# Backprop
					loss.backward()

					# Clip gradients
					nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)

					# Take a step with optimizer
					self.optimizer.step()
					self.scheduler.step()






































