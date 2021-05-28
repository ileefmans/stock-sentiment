from data import Database, ScrapeWSB, Stock
import torch
import transformers
from transformers import BertTokenizer




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




            
