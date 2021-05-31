[![Build Status](https://www.travis-ci.com/ileefmans/stock-sentiment.svg?branch=main)](https://www.travis-ci.com/ileefmans/stock-sentiment)
![GitHub last commit](https://img.shields.io/github/last-commit/ileefmans/stock-sentiment)
![GitHub repo size](https://img.shields.io/github/repo-size/ileefmans/stock-sentiment.svg)
![GitHub top language](https://img.shields.io/github/languages/top/ileefmans/stock-sentiment)  

  
  
# Stock Sentiment  
![Cloud Computing](https://img.shields.io/badge/Cloud-AWS-orange&?style=flat&logo=Amazon-AWS&color=9cf)
![Database](https://img.shields.io/badge/Database-MySQL-informational&?style=flat&logo=MySQL&color=informational&logoColor=white)  

This application scrapes Reddit to extract sentiment for a desired stock and then factors this information into predictions about the stocks future direction.



## TODO:  
  1) Set up scraping and accessing stock values  
  2) Create relational database to store data  
  3) Move from local device to AWS     
  4) Model for deriving sentiment 👈 
  5) Model for predicting stock direction  
  6) Build Web App  
  7) Set up monitoring  
 
## SMALL TODO:         
  1) Make sure to check if stock already exists before editing STOCK table    
  2) Complete labeling interface sidebar for rescraping and add labels to db  
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
  
