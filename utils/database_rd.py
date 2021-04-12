import mysql.connector
#import argparse
#import boto3
#import sys
#import os
import yaml
from pandas.io import sql






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
            self.conn =  mysql.connector.connect(host=self.ENDPOINT, user=self.USR, passwd=self.PASSWORD)#, database=self.DBNAME)
            print('connection established')
            self.cur = self.conn.cursor()
            self.cur.execute("""SELECT now()""")
            query_results = self.cur.fetchall()
            print(query_results)
        except Exception as e:
            print("Database connection failed due to {}".format(e)) 

    def initialize_database(self):
        sql1 = '''CREATE DATABASE DB1'''
        sql2 = '''USE DB1'''
        self.cur.execute(sql1)
        self.cur.execute(sql2)
        return

    def use_database(self, database_name):
        sql = '''USE {}'''.format(database_name)
        self.cur.execute(sql)

    def initialize_tables(self):
        sql1 = '''CREATE TABLE POSTS(
                POST_ID INT NOT NULL,
                STOCK_ID CHAR(20) NOT NULL,
                TITLE TEXT,
                SCORE INT,
                SUBREDDIT CHAR(20),
                URL CHAR(50),
                NUM_COMMENTS INT,
                BODY TEXT,
                CREATED FLOAT
            )'''

        sql2 = '''CREATE TABLE COMMENTS(
                COMMENT_ID INT NOT NULL,
                STOCK_ID CHAR(20) NOT NULL,
                COMMENT TEXT
            )'''
        sql3 = '''CREATE TABLE STOCKS(
                STOCK_ID INT NOT NULL,
                LAST_SCRAPED FLOAT
            )'''

        self.cur.execute(sql1)
        self.cur.execute(sql2)
        self.cur.execute(sql3)

        return

    def insert_posts(self, entry):
        sql = '''INSERT INTO POSTS (POST_ID, STOCK_ID, TITLE, SCORE, SUBREDDIT, URL, NUM_COMMENTS, BODY, CREATED) 
                VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {})'''.format(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8])
        
        self.cur.execute(sql)
        return


    def query(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()



if __name__=='__main__':
    db = Database()
    db.use_database('DB1')
    #db.initialize_tables()
    print(db.query('show tables;'))





