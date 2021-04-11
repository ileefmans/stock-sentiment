import mysql.connector
#import argparse
#import boto3
#import sys
#import os
import yaml





# Open yml to get connectivity info
with open("IDs.yml") as file:
    info = yaml.load(file, Loader=yaml.FullLoader)

ENDPOINT = info['MySQL']['ENDPOINT']
PORT = info['MySQL']['PORT']
REGION = info['MySQL']['REGION']
USR = info['MySQL']['USR']
DBNAME = info['MySQL']['DBNAME']
PASSWORD = info['MySQL']['master_password']

# Connect to database
try:
    conn =  mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PASSWORD)#, database=DBNAME)
    print('connection established')
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e)) 





