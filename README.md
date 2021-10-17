[![Build Status](https://www.travis-ci.com/ileefmans/stock-sentiment.svg?branch=main)](https://www.travis-ci.com/ileefmans/stock-sentiment)
![GitHub last commit](https://img.shields.io/github/last-commit/ileefmans/stock-sentiment)
![GitHub repo size](https://img.shields.io/github/repo-size/ileefmans/stock-sentiment.svg)
![GitHub top language](https://img.shields.io/github/languages/top/ileefmans/stock-sentiment)  

  
  
# Stock Sentiment  
![Streamlit](https://img.shields.io/badge/Webapp-Streamlit-critical?&color=red&logo=streamlit)
![Framework](https://img.shields.io/badge/Framework-Pytorch-orange&?style=flat&logo=PyTorch&color=orange)
![Huggingface](https://img.shields.io/badge/🤗%20Framework-Huggingface-9cf?color=royalblue)
![Cloud Computing](https://img.shields.io/badge/Cloud-AWS-orange&?style=flat&logo=Amazon-AWS&color=9cf)
![Database](https://img.shields.io/badge/Database-MySQL-informational&?style=flat&logo=MySQL&color=informational&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-Travis%20CI-lightgrey?&style=flat&logo=Travis-CI&color=yellow&logoColor=yellow)
![Container](https://img.shields.io/badge/Container-Docker-blue?&logo=docker)  

*Note that this app is in the middle stages of production*  
This application scrapes Reddit to extract sentiment for a desired stock and then factors this information into predictions about the stocks future direction.



## TODO:  
  1) Set up scraping and accessing stock values  
  2) Create relational database to store data  
  3) Move from local device to AWS     
  4) Model for deriving sentiment  
  5) Model for predicting stock direction        
  6) Build Web App 👈     
  7) Set up monitoring  
 
## SMALL TODO:           
   1) Add historical sentiment visualizations to app   
   2) Finish README      
          

## Overview  

Stock Sentiment is an webapp that gives real-time predictions and visualizations which capture the prevailing sentiment towards a particular stock on Reddit. Stock Sentiment's interface allows you to choose a stock and set the application to either "Visualization" mode or "Prediction" mode. As shown below in an example of "Visualization" mode, Stock Sentiment provides a host of visuals such as plots showing the predicted sentiment of all comments and posts scraped from Reddit within the past 48 hours. In additon, Stock Sentiment provides examples of posts and comments classified as "positive" or "negative" with extreme confidence.

<p>
<img src="https://github.com/ileefmans/stock-sentiment/blob/main/media/app_screenshot.png" width=700 align=center />  
</p>
  
## Getting Started  
  
  **With Conda Environment**  
  
  If you have not already, [download Anaconda](https://www.anaconda.com/products/individual/get-started).  
  
  Clone Repository and Change Directory:  
  
  1) ```git clone https://github.com/ileefmans/stock-sentiment```  
  2) ```cd stock-sentiment```  
  
  Create/Activate Conda Environment and Run App:  
  
  1) ```conda create --name StockSentiment python=3.7```  
  2) ```conda activate StockSentiment```  
  3) ```pip install -r requirements.txt```    
  4) ```streamlit run utils/app.py```   

  Deactivate Conda Environment:  
  
  1) ``` conda deactivate```    
  
    
    
    
  **With Docker**  
  
  If you have not already, [install Docker](https://www.docker.com).  
  
  Build and Run Image:  
  1) ```docker build -t app:1.0 -f Dockerfile .```    
  2) ```docker run -p 8501:8501 app:1.0```  
  3) Type *"localhost:8501"* into internet browser   
  
  Stop Container:  
  1) ```docker stop <container name>```
  
