import mysql.connector
from pandas.io import sql
import praw
from praw.models import MoreComments
import pandas as pd
import finnhub
import yaml
import datetime
import time
from tqdm import tqdm


class Database:

    """
        Class for connecting to and manipulating relational database
    """
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
        """
            Method initializing database
        """
        sql1 = '''CREATE DATABASE DB1'''
        sql2 = '''USE DB1'''
        self.cur.execute(sql1)
        self.cur.execute(sql2)
        return

    def use_database(self, database_name):
        """
            Method determining what database to use

            Args:

                database_name (str): Name of database to be used
        """
        sql = '''USE {}'''.format(database_name)
        self.cur.execute(sql)

    def initialize_tables(self):
        """
            Method initializing tables
        """
        sql1 = '''CREATE TABLE POSTS(
                POST_ID CHAR(20) PRIMARY KEY NOT NULL,
                STOCK_ID CHAR(20) NOT NULL,
                TITLE CHAR(100),
                SCORE INT,
                SUBREDDIT CHAR(20),
                URL CHAR(50),
                NUM_COMMENTS INT,
                BODY TEXT,
                TARGET INT,
                CREATED FLOAT,
                LAST_SCRAPED DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )'''

        sql2 = '''CREATE TABLE COMMENTS(
                COMMENT_ID CHAR(20) PRIMARY KEY NOT NULL,
                POST_ID CHAR(20) NOT NULL,
                STOCK_ID CHAR(20) NOT NULL,
                TARGET INT,
                COMMENT TEXT,
                LAST_SCRAPED DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )'''
        sql3 = '''CREATE TABLE STOCKS(
                STOCK_ID CHAR(20) PRIMARY KEY NOT NULL,
                LAST_SCRAPED DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )'''

        self.cur.execute(sql1)
        self.cur.execute(sql2)
        self.cur.execute(sql3)

        return

    def insert(self, table, data):
        """
            Method for inserting row into table

            Args:

                table (str): Table to be inserted into
                data (list): List of data to be inserted into table
        """
        if table == 'POSTS':
            sql = '''INSERT INTO POSTS (POST_ID, STOCK_ID, TITLE, SCORE, SUBREDDIT, URL, NUM_COMMENTS, BODY, TARGET, CREATED) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        
            self.cur.execute(sql, (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]))
            self.conn.commit()
            return
        
        elif table == 'COMMENTS':
            sql = '''INSERT INTO COMMENTS(COMMENT_ID, POST_ID, STOCK_ID, TARGET, COMMENT)
                VALUES (%s, %s, %s, %s, %s);'''

            self.cur.execute(sql, (data[0], data[1], data[2], data[3], data[4]))
            self.conn.commit()
            return

        elif table == 'STOCKS':
            # sql = '''INSERT INTO STOCKS(STOCK_ID, LAST_SCRAPED)
            #     VALUES (%s, NOW());'''

            sql = '''INSERT INTO STOCKS(STOCK_ID)
                VALUES('{}');'''.format(data)

            self.cur.execute(sql)
            self.conn.commit()
            return

        else:
            raise Exception("Only 'POSTS', 'COMMENTS' or 'STOCKS' valid arguments for 'table'")

    def label(self, table_name, ID, label):
        """
            Method for labeling unlabeled posts and comments

            Args:

                table_name (str): Name of desired table
                ID (str): ID of post or comment to be labeled
                label (int): label of post or comment (either 1 or 0)
        """
        if table_name=='POSTS':
            sql = "UPDATE POSTS SET TARGET={} WHERE POST_ID='{}';".format(label, ID)
        elif table_name=='COMMENTS':
            sql = "UPDATE COMMENTS SET TARGET={} WHERE COMMENT_ID='{}';".format(label, ID)
        else:
            raise Exception("Only 'POSTS' or 'COMMENTS' valid arguments for 'table_name'")
        self.cur.execute(sql)
        self.conn.commit()
        return

    def update_last_scraped(self, stock_id):
        """
            Method to update Stock table to show the last time the stock was scraped

            Args:

                stock_id (str): Id of stock to update
        """
        sql = "UPDATE STOCKS SET LAST_SCRAPED=NOW() WHERE STOCK_ID='{}';".format(stock_id)
        self.cur.execute(sql)
        self.conn.commit()
        return

    def query(self, sql):

        """
            Method ot query database

            Args:

                sql (str): SQL Statement
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

    def drop_table(self, table_name):
        """
            Method to drop table from database

            Args:

                table_name (str): Name of table to be dropped
        """
        sql = '''DROP TABLE {} ;'''.format(table_name)
        self.cur.execute(sql)
        return


def get_keys(website):
    """
        Helper fucntion to get passwords for external APIs

        Args:

            website (str): name of website
    """
    with open("IDs.yml") as file:
        IDs = yaml.load(file, Loader=yaml.FullLoader)
    if website=="Reddit":
        client_id = IDs['Reddit']['client_id']
        client_secret = IDs['Reddit']['client_secret']
        return client_id, client_secret
    if website=="Finnhub":
        api_key = IDs["Finnhub"]["api_key"]
        return api_key



class ScrapeWSB:
    """
        Class to scrape r/wallstreetbets
    """
    def __init__(self, stock_name, num_posts, num_comments, sort_type="hot", time_filter="day"):
        """
            Args:

                stock_name (str):       Name of stock to be scraped
                num_posts (int):        Number of posts to be scraped
                num_comments (int):     Number of comments to be scraped
                sort_type (str):        Way to sort top posts ("hot", etc) <--- FILL IN LATER
                time_filter(str):       Time period from which to scrape posts ("day", "week", "month")

        """


        self.stock_name = stock_name
        self.num_posts = num_posts
        self.num_comments = num_comments
        self.sort_type=sort_type
        self.time_filter = time_filter

        # Create "reddit" object
        #self.reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent='WebScraping')
    
    def scrape(self):
        #Blank list for hottest posts and their attributes
        #posts = []

        # obtain most recent posts from wallstreetbets with regard to GME
        self.client_id, self.client_secret = get_keys("Reddit")
        self.reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent='WebScraping')
        queried_posts = self.reddit.subreddit('wallstreetbets').search(self.stock_name, 
                                                                self.sort_type, 
                                                                self.time_filter,
                                                                limit=self.num_posts)



        # Loop through 10 GME posts and print title
        db = Database()
        db.use_database('DB1')
        post_id_list = []
        for post in queried_posts:
            
            # append post attributes to list
            # posts.append([post.id, self.stock_name, post.title, post.score, post.subreddit, post.url, post.num_comments, 
            #             post.selftext, post.created])


            if len(db.query("SELECT * FROM POSTS WHERE POST_ID='{}';".format(post.id)))==0:
                db.insert('POSTS', [post.id, self.stock_name, post.title, post.score, str(post.subreddit), post.url, post.num_comments, 
                            post.selftext, -1, post.created])
                

                post_id_list.append(post.id)

        # Create Dataframe for top 10 hottest posts
        # posts = pd.DataFrame(posts,columns=['post_id', 'stock_id', 'title', 'score', 'subreddit', 'url', 'num_comments', 'body', 'created'])

        
        return post_id_list

    def convert(self, df, training=False):
        # Initialize dictionary
        stock = []
        

        db = Database()
        db.use_database('DB1')
        # Loop through all top posts
        for i in tqdm(range(len(df))):
            
            # Extract ID
            ID = df[i]
            #ID = df.post_id[i]
            # Create submission object to extract comments for each post
            submission = self.reddit.submission(id = ID)
            submission.comments.replace_more(limit=0)

            # Initialize list for commments
            #comments = []
            count = 0
            # Loop through comments
            for top_level_comment in submission.comments:
                # append comments to list
                if count<self.num_comments:
                    #comments.append(top_level_comment.body)

                    if len(db.query("SELECT * FROM COMMENTS WHERE COMMENT_ID='{}';".format(top_level_comment.id)))==0:
                        db.insert('COMMENTS', [top_level_comment.id, ID, self.stock_name, -1, top_level_comment.body])

                else:
                    break
                count+=1 

        if len(db.query("SELECT * FROM STOCKS WHERE STOCK_ID='{}';".format(self.stock_name)))==0:
            db.insert('STOCKS', self.stock_name)
        else:
            db.update_last_scraped(self.stock_name)
        return 

    def process(self):
        self.convert(self.scrape())
        return



class Stock:

    """
        Class for pulling recent stock values
    """
    def __init__(self):


        self.start = int(time.mktime((datetime.datetime.now()- datetime.timedelta(days=1)).timetuple()))
        self.end = int(time.time())


    def set_start(self, date):
        """

            Args: 
            
                date (list): [year (int), month (int), day (int), hour (int), minute (int), seconds (int)]
        """

        self.start = self.create_unix_stamp(date[0], date[1], date[2], date[3], date[4], date[5])

    def set_end(self, current=True, date=None):
        """
            Args:

                current (bool): if True, end is current date and time; if False must set desired end date and time 
                date (list): [year (int), month (int), day (int), hour (int), minute (int), seconds (int)]
        """

        if current:
            self.end = int(time.time())
        else:
            self.end = self.create_unix_stamp(date[0], date[1], date[2], date[3], date[4], date[5])


    # Create unix timestamp
    def create_unix_stamp(self, year, month, day, hour, minute, second):
        """
            Args:

                year (int): year
                month (int): month
                day (int): day
                hour (int): hour
                minute (int): minute
                second (int): second

            Method for creating unix time stamp from list 
        """
        dt = datetime.datetime(year, month, day, hour, minute, second)
        return int(time.mktime(dt.timetuple()))

    def convert(self, df):
        """

            Args:

                df (pd.DataFrame): dataframe to be converted


            Method for converting dataframe to dictionary
        """
        prices = {}
        prices['_id'] = 0
        prices['open'] = list(df.o)
        prices['high'] = list(df.h)
        prices['low'] = list(df.l) 
        prices['close'] = list(df.c) 
        prices['volume'] = list(df.v) 
        prices['timestamp'] = list(df.t) 
        prices['status'] = list(df.s) 
        return prices


    def lag(self, feature, df):
            df[feature+"_t1"] = [df.loc[df.timestamp.dt.day==i.day-1,['timestamp', feature]][feature].mean() for i in tqdm(df.timestamp)]


    def pull_data(self, stock_name):
        """
            Args:

                stock_name (str): Name of stock for which to pull data

            Method for scraping stock data
        """

        self.api_key = get_keys("Finnhub")
        self.finnhub_client = finnhub.Client(api_key=self.api_key)
        res = self.finnhub_client.stock_candles(stock_name, '1', self.start, self.end)

        df = pd.DataFrame(res)
        
        df['t'] = list(map(lambda x: datetime.datetime.fromtimestamp(int(str(x))).strftime('%Y-%m-%d %H:%M:%S'), df.t))

        #prices = self.convert(df)
        df.rename(columns = {'o': 'open', 
                            'h': 'high', 
                            'l': 'low', 
                            'c': 'close', 
                            'v': 'volume', 
                            't': 'timestamp', 
                            's': 'status'},
                inplace=True)

        # Engineer feature for high/low percentage
        df['highlow_percent'] = df.low/df.high
        # convert timestamp to datetime
        df.timestamp = pd.to_datetime(df.timestamp)
        # Create feature with lagged close


        self.lag('highlow_percent', df)
        #df['close_t1'] = [df.loc[df.timestamp.dt.day==i.day-1,['timestamp', 'close']].close.mean() for i in tqdm(df.timestamp, "Gathering stock prices: ")]

        return df




if __name__=='__main__':
    db = Database()
    db.use_database('DB1')
    # db.initialize_tables()
    
    # db.drop_table('COMMENTS')
    # db.drop_table("POSTS")
    # db.drop_table("STOCKS")
    print(db.query('show tables;'))

    # scrapewsb = ScrapeWSB('GME', 10, 10)
    # df = scrapewsb.scrape()
    # scrapewsb.convert(df)
    # print("DONE")

    # print(db.query('''SELECT * FROM POSTS ;'''))
    #print(db.query('''SELECT STOCK_ID FROM COMMENTS ;'''), '\n \n \n \n')
    print(db.query('''SELECT * FROM STOCKS ;'''))
        



