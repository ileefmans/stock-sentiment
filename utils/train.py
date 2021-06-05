import torch
from torch import nn
from torch.utils.data import DataLoader
from transformers import AdamW, get_linear_schedule_with_warmup
from datahelper import PostDataset, CommentDataset, get_indices
from models import SentimentModel, FineTuneBaseModel
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
	parser.add_argument(
		"--load_weights",
		type=bool,
		default=False,
		help="True to load checkpoint from previous training session, False to start training from base")
	return parser.parse_args()



class Train:
	"""
		Class for finetuning BERT
	"""
	def __init__(self):

		self.config = get_config()
		self.ops = get_args()
		self.local = self.ops.local
		self.load_weights = self.ops.load_weights

		self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

		# Num Epochs
		self.epochs = self.config['epochs']

		# Batch Size
		self.batch_size = self.config['batch_size']

		if self.config['model']=='pretrained':
			self.model = SentimentModel().to(self.device)
		elif self.config['model'] == 'finetuned':
			self.model = FineTuneBaseModel().to(self.device)

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
		self.optimizer = AdamW(self.model.parameters(),lr=2e-5, correct_bias=False)

		# Set up learning rate scheduler
		total_steps = (len(self.post_trainloader) + len(self.comment_trainloader)) * self.epochs
		self.scheduler = get_linear_schedule_with_warmup(
			self.optimizer,
			num_warmup_steps=0,
			num_training_steps=total_steps
			)

		# Initialize Loss Function
		self.loss_fcn = nn.CrossEntropyLoss().to(self.device)


	def train(self):

		
		if not self.local:
			torch.set_default_tensor_type(torch.cuda.FloatTensor)
			print("\n \n EVERYTHING TO CUDA \n \n")

		if self.load_weights:
			start_epoch, losses, accuracies = self.load_checkpoint()
			print("\nWeights Loaded\n")
			start_epoch+=1
		else:
			start_epoch = 0
			losses = []
			accuracies = []

		test_losses = []
		test_accuracies = []

		# Start Training Loop
		for epoch in range(start_epoch, self.epochs+1):

			# Train
			if epoch>0:


				epoch_train_loss = 0
				total_epoch_train_acc = 0
				# Set model to training mode
				self.model.train()
				for post_batch in tqdm(self.post_trainloader, desc='Post Train Epoch {}'.format(epoch)):

					# Send input ids and attention masks to device
					post_input_ids = post_batch['post_input_ids'].to(self.device)
					post_attention_masks = post_batch['post_attention_mask'].to(self.device)
					post_targets = post_batch['target'].reshape(-1,2).to(self.device)

					post_output = self.model(input_ids=post_input_ids, attention_masks=post_attention_masks)
					# print(post_output)
					# print(type(post_output))
					# Calculate Loss
					loss = self.loss_fcn(post_output, post_targets)

					# Make Predictions
					_, preds = torch.max(post_output, dim=1)
					_, ground_truths = torch.max(post_targets, dim=1)

					# Calculate Accuracy
					acc = torch.sum(preds==ground_truths)/len(preds)

					epoch_train_loss+=loss
					total_epoch_train_acc+=acc

					# Clear optimizer gradient
					self.optimizer.zero_grad()

					# Backprop
					loss.backward()

					# Clip gradients
					nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)

					# Take a step with optimizer
					self.optimizer.step()
					self.scheduler.step()




				for comment_batch in tqdm(self.comment_trainloader, desc='Comment Train Epoch {}'.format(epoch)):

					# Send input ids and attention masks to device
					comment_input_ids = comment_batch['comment_input_ids'].to(self.device)
					comment_attention_masks = comment_batch['comment_attention_mask'].to(self.device)
					comment_targets = comment_batch['target'].reshape(-1,2).to(self.device)

					comment_output = self.model(input_ids=comment_input_ids, attention_masks=comment_attention_masks)

					# Calculate Loss
					loss = self.loss_fcn(comment_output, comment_targets)

					# Make Predictions
					_, preds = torch.max(comment_output, dim=1)
					_, ground_truths = torch.max(comment_targets, dim=1)

					# Calculate Accuracy
					acc = torch.sum(preds==ground_truths)/len(preds)

					epoch_train_loss+=loss
					total_epoch_train_acc+=acc

					# Clear optimizer gradient
					self.optimizer.zero_grad()

					# Backprop
					loss.backward()

					# Clip gradients
					nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)

					# Take a step with optimizer
					self.optimizer.step()
					self.scheduler.step()

				avg_loss = epoch_train_loss / (len(self.post_trainloader.dataset)+len(self.comment_trainloader.dataset))
				losses.append(avg_loss)
				avg_acc = total_epoch_train_acc / (len(self.post_trainloader.dataset)+len(self.comment_trainloader.dataset))
				accuracies.append(avg_acc)

				self.save_checkpoint(
					epoch, 
					losses, 
					accuracies
				)
				
				print("\nWeights Saved\n")

				print(
					f"====> Epoch: {epoch} Average train loss: {avg_loss :.4f} Average train accuracy: {avg_acc :.4f}\n"
					)

			# Evaluate on Test set
			with torch.no_grad():
				# Set model to evaluation mode
				self.model.eval()

				epoch_test_loss = 0
				total_epoch_test_acc = 0
				for post_batch in tqdm(self.post_testloader, desc='Post Test Epoch {}'.format(epoch)):

					# Send input ids and attention masks to device
					post_input_ids = post_batch['post_input_ids'].to(self.device)
					post_attention_masks = post_batch['post_attention_mask'].to(self.device)
					post_targets = post_batch['target'].reshape(-1,2).to(self.device)

					post_output = self.model(input_ids=post_input_ids, attention_masks=post_attention_masks)

					# Calculate Loss
					loss = self.loss_fcn(post_output, post_targets)

					# Make Predictions
					_, preds = torch.max(post_output, dim=1)
					_, ground_truths = torch.max(post_targets, dim=1)

					# Calculate Accuracy
					acc = torch.sum(preds==ground_truths)/len(preds)

					epoch_test_loss+=loss
					total_epoch_test_acc+=acc

				for comment_batch in tqdm(self.comment_testloader, desc='Comment Test Epoch {}'.format(epoch)):

					# Send input ids and attention masks to device
					comment_input_ids = comment_batch['comment_input_ids'].to(self.device)
					comment_attention_masks = comment_batch['comment_attention_mask'].to(self.device)
					comment_targets = comment_batch['target'].reshape(-1,2).to(self.device)

					comment_output = self.model(input_ids=comment_input_ids, attention_masks=comment_attention_masks)

					# Calculate Loss
					loss = self.loss_fcn(comment_output, comment_targets)

					# Make Predictions
					_, preds = torch.max(comment_output, dim=1)
					_, ground_truths = torch.max(comment_targets, dim=1)

					# Calculate Accuracy
					acc = torch.sum(preds==ground_truths)/len(preds)

					epoch_test_loss+=loss
					total_epoch_test_acc+=acc

				avg_test_loss = epoch_test_loss / (len(self.post_testloader.dataset)+len(self.comment_testloader.dataset))
				test_losses.append(avg_test_loss)
				avg_test_acc = total_epoch_test_acc / (len(self.post_testloader.dataset)+len(self.comment_testloader.dataset))
				test_accuracies.append(avg_test_acc)

				print(
					f"====> Epoch: {epoch} Average train loss: {avg_test_loss :.4f} Average train accuracy: {avg_test_acc :.4f}\n"
					)






		# Save model after training is complete
		if self.local:
			torch.save(
				self.model, "models/{}.pt".format(self.config['model'])
				)
		else:
			torch.save(
				self.model, "{}.pt".format(self.config['model'])
				)


		return {
				'train losses': losses,
				'train accuracies': accuracies,
				'test losses': test_losses,
				'test accuracies': test_accuracies
				}

	def save_checkpoint(self, epoch, loss, accuracy):
		if self.local:
			torch.save(
				{
					"epoch": epoch,
					"model_state_dict": self.model.state_dict(),
					"optimizer_state_dict": self.optimizer.state_dict(),
					"loss": loss,
					"accuracy": accuracy
				},
				"models/params/{}.tar".format(self.config['model'])
			)

		else:
			torch.save(
				{
					"epoch": epoch,
					"model_state_dict": self.model.state_dict(),
					"optimizer_state_dict": self.optimizer.state_dict(),
					"loss": loss,
					"accuracy": accuracy
				},
				"{}.tar".format(self.config['model'])
			)

	def load_checkpoint(self):
		if self.local:
			checkpoint = torch.load("models/params/{}.tar".format(self.config['model']))
		else:
			checkpoint = torch.load("{}.tar".format(self.config['model']))

		self.model.load_state_dict(checkpoint['model_state_dict'])
		self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

		return {
				'epoch': checkpoint['epoch'], 
				'loss': checkpoint['loss'],
				'accuracy': checkpoint['accuracy']
				}


if __name__ == '__main__':
	trainer = Train()
	training_output = trainer.train()







