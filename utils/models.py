import torch
from torch import nn
import transformers
from transformers import BertForSequenceClassification, BertModel



class SentimentModel(nn.Module):
	"""
		Class for Pretrained (non finetuned) Sentiment Model
	"""
	def __init__(self):
		super(SentimentModel, self).__init__()

		self.bert = BertForSequenceClassification.from_pretrained('bert-base-cased')

	def forward(self, input_ids, attention_masks):

		return self.bert(input_ids, attention_masks)


class FineTuneBaseModel(nn.Module):
	"""
		Class for Sentiment Model fine-tuned from Bert Base
	"""
	def __init__(self):
		super(FineTuneBaseModel, self).__init__()

		self.bert = BertModel.from_pretrained('bert-base-cased')

		self.drop = nn.Dropout(p=0.3)
		self.fc = nn.Linear(self.bert.config.hidden_size, 2)
		self.softmax = nn.Softmax(dim=1)

	def forward(self, input_ids, attention_masks):
		output = self.bert(
									input_ids=input_ids, 
									attention_mask = attention_masks
		)
		
		
		x = self.drop(output.pooler_output)
		x = self.fc(x)
		x = self.softmax(x)
		return x




class FineTuneClassifier(nn.Module):
	"""
		Class for Sentiment Model fine-tuned from Bert Sentiment Classifier
	"""

	def __init__(self):
		super(FineTuneClassifier, self).__init__()

		self.bert = BertForSequenceClassification.from_pretrained('bert-base-cased')
		self.softmax = nn.Softmax(dim=1)

	def forward(self, input_ids, attention_masks):

		x = self.bert(input_ids, attention_masks)
		x = self.softmax(x.logits)
		return x


