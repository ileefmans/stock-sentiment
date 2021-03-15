import praw
from praw.models import MoreComments
import pandas as pd

class ScrapeWSB:
    """
        Class to scrape r/wallstreetbets
    """
    def __init__(self, stock_name, num_posts, num_comments, sort_type="hot", time_filter="day"):
        """
            Args:

                stock_name (str):   Name of stock to be scraped
                num_posts (int):    Number of posts to be scraped
                num_comments (int): Number of comments to be scraped
                sort_type (str):    Way to sort top posts ("hot", etc) <--- FILL IN LATER
                time_filter(str):   Time period from which to scrape posts ("day", "week", "month")

        """

        self.stock_name = stock_name
        self.num_posts = num_posts
        self.num_comments = num_comments
        self.sort_type=sort_type
        self.time_filter = time_filter

        # Create "reddit" object
        self.reddit = praw.Reddit(client_id=temp, client_secret=temp, user_agent='WebScraping')
    
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


        



