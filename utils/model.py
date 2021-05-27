import torch
from torch import nn
import transformers
from transformers import BertForSequenceClassification



class SentimentModel(nn.Module):
	def __init__(self):
		super(SentimentModel, self).__init__()

		self.bert = BertForSequenceClassification.from_pretrained('bert-base-cased')

	def forward(self, x):

		return self.bert(x)