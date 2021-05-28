[![Build Status](https://www.travis-ci.com/ileefmans/stock-sentiment.svg?branch=main)](https://www.travis-ci.com/ileefmans/stock-sentiment)
![GitHub last commit](https://img.shields.io/github/last-commit/ileefmans/stock-sentiment)
![GitHub repo size](https://img.shields.io/github/repo-size/ileefmans/stock-sentiment.svg)
![GitHub top language](https://img.shields.io/github/languages/top/ileefmans/stock-sentiment)  

  
  
# Stock Sentiment  
![Cloud Computing](https://img.shields.io/badge/Cloud-AWS-orange&?style=flat&logo=Amazon-AWS&color=9cf)
![Database](https://img.shields.io/badge/Database-MySQL-informational&?style=flat&logo=MySQL&color=informational&logoColor=white)  

This application scrapes Reddit to extract sentiment for a desired stock and then factors this information into predictions about the stocks future direction.



## TODO:  
  1) Move from local device to AWS 🏼    
  2) Model for deriving sentiment 👈 
  3) Model for predicting stock direction  
  4) Build Web App  
  5) Set up monitoring  
 
## SMALL TODO:        
  1) Make sure to check if stock already exists before editing STOCK table  
  2) Update dataloader to use both POSTS and COMMENTS  
  3) Write training script    
   
  
## Getting Started  
  
  **With Conda Environement**  
  
  If you have not already, [download Anaconda](https://www.anaconda.com/products/individual/get-started).  
  
  Clone Repository and Change Directory:  
  
  1) ```git clone https://github.com/ileefmans/stock-sentiment```  
  2) ```cd stock-sentiment```  
  
  Create and Activate Conda Environemnt:  
  
  1) ```conda create --name StockSentiment python=3.7```  
  2) ```conda activate StockSentiment```  
  3) ```pip install -r requirements.txt```  

  Deactivate Conda Environment:  
  
  1) ``` conda deactivate```  
  
