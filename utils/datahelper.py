from data import Database, ScrapeWSB, Stock
import torch
import transformers
from transformers import BertTokenizer
from sklearn.model_selection import train_test_split


def get_indices(stock_id, train=.7, test=.3, val_set=False, val=0, inference=False, scrape_time=6):
	"""
		Helper function to get comment and post indices to feed into custom PyTorch Datasets

		Args:

			stock_id (str): Symbol of desired stock
	"""
	if inference:
		db = Database()
		db.use_database('DB1')
		post_ids = db.query("SELECT POST_ID FROM POSTS WHERE STOCK_ID='{}' AND LAST_SCRAPED >= DATESUB((SELECT LAST_SCRAPED FROM STOCKS WHERE STOCK_ID = '{}'), INTERVAL {} HOUR)".format(stock_id, stock_id, scrape_time))
		comment_ids = db.query("SELECT COMMENT_ID FROM COMMENTS WHERE STOCK_ID='{}' AND LAST_SCRAPED >= DATESUB((SELECT LAST_SCRAPED FROM STOCKS WHERE STOCK_ID = '{}'), INTERVAL {} HOUR)".format(stock_id, stock_id, scrape_time))

		return {'post_ids': post_ids,
			'comment_ids': comment_ids}

	if not val_set:
		if not (0<=train<=1):
			raise Exception("Argument 'train' must be between 0 and 1")
		if not (0<=test<=1):
			raise Exception("Argument 'test' must be between 0 and 1")
		if train+test!=1:
			raise Exception("Arguments 'train' and 'test' must sum to 1")
	else:
		if val==0:
			raise Exception("If argument 'val_set' is True 'val must be a positive value less than 1")
		if not (0<=test<=1):
			raise Exception("Argument 'test' must be between 0 and 1")
		if train+test!=1:
			raise Exception("Arguments 'train' and 'test' must sum to 1")
		if not (0<val<=1):
			raise Exception("Argument 'val' must be between 0 and 1")
		if train+val+test!=1:
			raise Exception("Arguments 'train', 'test', and 'val' must sum to 1")


	db = Database()
	db.use_database('DB1')

	post_ids = db.query("SELECT POST_ID FROM POSTS WHERE TARGET IN (0, 1)")
	comment_ids = db.query("SELECT COMMENT_ID FROM COMMENTS WHERE TARGET IN (0, 1)")


	if not val:
		post_train, post_test = train_test_split(post_ids, train_size = train, random_state=42)
		comment_train, comment_test = train_test_split(comment_ids, train_size = train, random_state=42)

		return {'post_train': post_train,
				'post_test': post_test,
				'comment_train': comment_train,
				'comment_test': comment_test}

	else:
		post_train, post_val_test = train_test_split(post_ids, train_size = train, random_state=42)
		post_val, post_test = train_test_split(post_val_test, train_size = val, random_state=42)

		comment_train, comment_val_test = train_test_split(comment_ids, train_size = train, random_state=42)
		comment_val, comment_test = train_test_split(comment_val_test, train_size = val, random_state=42)

		return {'post_train': post_train,
				'post_val': post_val,
				'post_test': post_test,
				'comment_train': comment_train,
				'comment_val': comment_val,
				'comment_test': comment_test}





class PostDataset(torch.utils.data.Dataset):
	"""
		Class for creating custom PyTorch Dataset for Posts
	"""
	def __init__(self, max_len, post_indices):
		"""
			Args:

				max_len (int):          maximum length for text fed into of Bert Tokenizer
				post_indices (list):    List of post indices for posts to be pulled from Relational Database
		"""
		self.max_len = max_len
		self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
		self.db = Database()
		self.db.use_database('DB1')
		self.post_indices = post_indices
		
		# self.indexes = self.db.query('''SELECT POST_ID FROM POSTS;''')
		
		
	def __len__(self):
		return len(self.post_indices)
		
	def __getitem__(self, index):
		post_target = self.db.query("SELECT TITLE, TARGET FROM POSTS WHERE POST_ID='{}'".format(self.post_indices[index][0]))
		post, target = post_target[0][0], post_target[0][1]
		post_encoding = self.tokenizer.encode_plus(
			post,
			max_length=self.max_len,
			add_special_tokens=True, # Add '[CLS]' and '[SEP]'
			return_token_type_ids=False,
			pad_to_max_length=True,
			return_attention_mask=True,
			return_tensors='pt',  # Return PyTorch tensors
			truncation=True
			)
		
	   
		return {
			'post': post,
			'post_input_ids': post_encoding['input_ids'].flatten(),
			'post_attention_mask': post_encoding['attention_mask'].flatten(),
			'target': torch.tensor(target, dtype=torch.long)
			}



class CommentDataset(torch.utils.data.Dataset):
	"""
		Class for creating custom PyTorch Dataset for Comments
	"""
	def __init__(self, max_len, comment_indices):
		"""
			Args:

				max_len (int):          maximum length for text fed into of Bert Tokenizer
				post_indices (list):    List of comment indices for posts to be pulled from Relational Database                
		"""
		self.max_len = max_len
		self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
		self.db = Database()
		self.db.use_database('DB1')
		self.comment_indices = comment_indices
		# self.indexes = self.db.query('''SELECT POST_ID FROM POSTS;''')
		
		
	def __len__(self):
		return len(self.comment_indices)
		
	def __getitem__(self, index):
		comment_target = self.db.query("SELECT COMMENT, TARGET FROM COMMENTS WHERE COMMENT_ID='{}'".format(self.comment_indices[index][0]))
		comment, target = comment_target[0][0], comment_target[0][1]
		comment_encoding = self.tokenizer.encode_plus(
			comment,
			max_length=self.max_len,
			add_special_tokens=True, # Add '[CLS]' and '[SEP]'
			return_token_type_ids=False,
			pad_to_max_length=True,
			return_attention_mask=True,
			return_tensors='pt',  # Return PyTorch tensors
			truncation=True
			)
		
		
		return {
			'comment': comment,
			'comment_input_ids': comment_encoding['input_ids'].flatten(),
			'comment_attention_mask': comment_encoding['attention_mask'].flatten(),
			'target': torch.tensor(target, dtype=torch.long)
			}





