from data import Database, ScrapeWSB, Stock
import torch
import transformers
from transformers import BertTokenizer


class Dataset(torch.utils.data.Dataset):
    def __init__(self, max_len):
        self.max_len = max_len
        self.PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
        self.tokenizer = BertTokenizer.from_pretrained(self.PRE_TRAINED_MODEL_NAME)
        self.db = Database()
        self.db.use_database('DB1')
        self.indexes = self.db.query('''SELECT POST_ID FROM POSTS;''')
        
        
    def __len__(self):
        return len(self.indexes)
        
    def __getitem__(self, index):
        post = db.query("SELECT TITLE FROM POSTS WHERE POST_ID='{}'".format(indexes[index][0]))[0][0]
        encoding = self.tokenizer.encode_plus(
            post,
            max_length=self.max_len,
            add_special_tokens=True, # Add '[CLS]' and '[SEP]'
            return_token_type_ids=False,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',  # Return PyTorch tensors
            )
        
        return {
            'post': post,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            #'targets': torch.tensor(target, dtype=torch.long)
            }
