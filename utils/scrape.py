import praw
from praw.models import MoreComments
import pandas as pd
import finnhub
import yaml
import datetime
import time

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

        with open("IDs.yml") as file:
            self.IDs = yaml.load(file, Loader=yaml.FullLoader)
        self.client_id = self.IDs['Reddit']['client_id']
        self.client_secret = IDs['Reddit']['client_secret']

        self.stock_name = stock_name
        self.num_posts = num_posts
        self.num_comments = num_comments
        self.sort_type=sort_type
        self.time_filter = time_filter

        # Create "reddit" object
        self.reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent='WebScraping')
    
    def scrape(self):
        #Blank list for hottest posts and their attributes
        posts = []

        # obtain most recent posts from wallstreetbets with regard to GME
        queried_posts = self.reddit.subreddit('wallstreetbets').search(self.stock_name, 
                                                                self.sort_type, 
                                                                self.time_filter,
                                                                limit=self.num_posts)



        # Loop through 10 GME posts and print title
        for post in queried_posts:
            # append post attributes to list
            posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, 
                        post.selftext, post.created])

        # Create Dataframe for top 10 hottest posts
        posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

        return posts

    def convert(self, df):
        # Initialize dictionary
        stock = {}
        
        # Loop through all top posts
        for i in range(len(df)):

            # Extract ID
            ID = df.id[i]
            # Create submission object to extract comments for each post
            submission = self.reddit.submission(id = ID)
            submission.comments.replace_more(limit=0)

            # Initialize list for commments
            comments = []
            count = 0
            # Loop through comments
            for top_level_comment in submission.comments:
                # append comments to list
                if count<self.num_comments:
                    comments.append(top_level_comment.body)
                else:
                    break
                count+=1
            
            # add meta data for each post along with all commments to dictionary
            stock["post_{}".format(i)] = {"id": df.iloc[i].id, "title": df.iloc[i].title, "score": int(df.iloc[i].score),
                                          "num_comments": int(df.iloc[i].num_comments), "url": df.iloc[i].url, 
                                          "created": float(df.iloc[i].created), "comments": comments}
        return stock

    def process(self):
        return self.convert(self.scrape())



class Stock:
    def __init__(self):


        # Extract IDs from yaml file
        with open("IDs.yml") as file:
            self.IDs = yaml.load(file, Loader=yaml.FullLoader)
        self.api_key = self.IDs["Finnhub"]["api_key"]

        # Set up client
        self.finnhub_client = finnhub.Client(api_key=self.api_key)
        self.start = int(time.mktime((datetime.datetime.now()- datetime.timedelta(days=1)).timetuple()))
        self.end = int(time.time())


    def set_start(self, date):
        self.start = self.create_unix_stamp(date[0], date[1], date[2], date[3], date[4], date[5])

    def set_end(self, current=True, date=None):
        if current:
            self.end = int(time.time())
        else:
            self.end = self.create_unix_stamp(date[0], date[1], date[2], date[3], date[4], date[5])


    # Create unix timestamp
    def create_unix_stamp(self, year, month, day, hour, minute, second):
        dt = datetime.datetime(year, month, day, hour, minute, second)
        return int(time.mktime(dt.timetuple()))


    def pull_data(self):

        res = self.finnhub_client.stock_candles('AAPL', '1', self.start, self.end)
        df = pd.DataFrame(res)
        df['t'] = list(map(lambda x: datetime.datetime.fromtimestamp(int(str(x))).strftime('%Y-%m-%d %H:%M:%S'), df.t))

        print(df)
        



