import torch
from torch import nn
import transformers
from transformers import BertForSequenceClassification, BertModel



class SentimentModel(nn.Module):
	def __init__(self):
		super(SentimentModel, self).__init__()

		self.bert = BertForSequenceClassification.from_pretrained('bert-base-cased')

	def forward(self, input_ids, attention_masks):

		return self.bert(input_ids, attention_masks)


class FineTuneBaseModel(nn.Module):
	def __init__(self):
		super(FineTuneBaseModel, self).__init__()

		self.bert = BertModel.from_pretrained('bert-base-cased')

		self.drop = nn.Dropout(p=0.3)
		self.fc = nn.Linear(self.bert.config.hidden_size, 2)
		self.softmax = nn.Softmax(dim=1)

	def forward(self, input_ids, attention_masks):
		_, pooled_output = self.bert(
									input_ids=input_ids, 
									attention_mask = attention_masks
		)

		x = self.drop(pooled_output)
		x = self.fc(x)
		x = self.softmax(x)
		return x