from data import Database, ScrapeWSB, Stock
import torch
import transformers
from transformers import BertTokenizer
from sklearn.model_selection import train_test_split


def get_indices(stock_id, train=.7, test=.3, val_set=False, val=0):
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

	post_ids = db.query("SELECT POST_ID FROM POSTS WHERE STOCK_ID='{}'".format(stock_id))
	comment_ids = db.query("SELECT COMMENT_ID FROM COMMENTS WHERE STOCK_ID='{}'".format(stock_id))


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





class Dataset(torch.utils.data.Dataset):
    def __init__(self, max_len, post_indices, comment_indices):
        self.max_len = max_len
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        self.db = Database()
        self.db.use_database('DB1')
        self.post_indices = post_indices
        self.comment_indices = comment_indices
        # self.indexes = self.db.query('''SELECT POST_ID FROM POSTS;''')
        
        
    def __len__(self):
        return len(self.indexes)
        
    def __getitem__(self, index):
        post = self.db.query("SELECT TITLE FROM POSTS WHERE POST_ID='{}'".format(self.post_indices[index][0]))[0][0]
        comment = self.db.query("SELECT COMMENT FROM COMMENTS WHERE COMMENT_ID='{}'".format(self.comment_indices[index][0]))[0][0]
        post_encoding = self.tokenizer.encode_plus(
            post,
            max_length=self.max_len,
            add_special_tokens=True, # Add '[CLS]' and '[SEP]'
            return_token_type_ids=False,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',  # Return PyTorch tensors
            )
        comment_encoding = self.tokenizer.encode_plus(
            comment,
            max_length=self.max_len,
            add_special_tokens=True, # Add '[CLS]' and '[SEP]'
            return_token_type_ids=False,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',  # Return PyTorch tensors
            )
        
        return {
            'post': post,
            'post_input_ids': post_encoding['input_ids'].flatten(),
            'post_attention_mask': post_encoding['attention_mask'].flatten(),
            'comment': comment,
            'comment_input_ids': comment_encoding['input_ids'].flatten(),
            'comment_attention_mask': comment_encoding['attention_mask'].flatten()
            #'targets': torch.tensor(target, dtype=torch.long)
            }




