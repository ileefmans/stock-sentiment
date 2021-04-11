import mysql.connector
#import argparse
#import boto3
#import sys
#import os
import yaml






class Database:
    def __init__(self):

        # Open yml to get connectivity info
        with open("IDs.yml") as file:
            self.info = yaml.load(file, Loader=yaml.FullLoader)

        self.ENDPOINT = self.info['MySQL']['ENDPOINT']
        self.PORT = self.info['MySQL']['PORT']
        self.REGION = self.info['MySQL']['REGION']
        self.USR = self.info['MySQL']['USR']
        self.DBNAME = self.info['MySQL']['DBNAME']
        self.PASSWORD = self.info['MySQL']['master_password']

        # Connect to database
        try:
            self.conn =  mysql.connector.connect(host=self.ENDPOINT, user=self.USR, passwd=self.PASSWORD)#, database=DBNAME)
            print('connection established')
            self.cur = conn.cursor()
            cur.execute("""SELECT now()""")
            query_results = cur.fetchall()
            print(query_results)
        except Exception as e:
            print("Database connection failed due to {}".format(e)) 

    def initialize_tables(self):
        sql1 = '''CREATE TABLE POSTS(
                POST_ID INT NOT NULL,
                STOCK_ID CHAR(20) NOT NULL,
                TITLE CHAR(500),
                SCORE INT,
                NUM_COMMENTS INT
                CREATED FLOAT
            )'''

        sql2 = '''CREATE TABLE COMMENTS(
                COMMENT_ID INT NOT NULL,
                STOCK_ID CHAR(20) NOT NULL,
                COMMENT CHAR(1000)
            )'''
        sql3 = '''CREATE TABLE STOCKS(
                STOCK_ID INT NOT NULL,
                LAST_SCRAPED FLOAT
            )'''

    def insert(self):
        pass





