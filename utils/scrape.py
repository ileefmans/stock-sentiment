import praw
from praw.models import MoreComments
import pandas as pd

class GetData:
    def __init__(self, stock_name, sort_type="hot", time_filter="day"):

        self.stock_name = stock_name
        self.sort_type=sort_type
        self.time_filter = time_filter

        # Create "reddit" object
        self.reddit = praw.Reddit(client_id='pjzGSwuoF7dgxA', client_secret='PIW3cZ1TiX9i5VVhr-wjdQvWT8ik1w', user_agent='WebScraping')
    
    def scrape(self):
        #Blank list for hottest posts and their attributes
        posts = []

        # obtain most recent posts from wallstreetbets with regard to GME
        queried_posts = self.reddit.subreddit('wallstreetbets').search(self.stock_name, 
                                                                self.sort_type, 
                                                                self.time_filter,
                                                                limit=10)



        # Loop through 10 GME posts and print title
        for post in queried_posts:
            # append post attributes to list
            posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, 
                        post.selftext, post.created])

        # Create Dataframe for top 10 hottest posts
        posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

        return posts

    def convert(self, df):
        stock = {}
        
        for i in range(len(df)):
            ID = df.id[i]
            submission = self.reddit.submission(id = ID)
            submission.comments.replace_more(limit=0)
            comments = []

            count = 0
            for top_level_comment in submission.comments:
                if count<10:
                    comments.append(top_level_comment.body)
                count+=1
            
            stock["post_{}".format(i)] = {"id": df.iloc[i].id, "title": df.iloc[i].title, "score": int(df.iloc[i].score),
                                          "num_comments": int(df.iloc[i].num_comments), "url": df.iloc[i].url, 
                                          "created": float(df.iloc[i].created), "comments": comments}
        return stock

    def process(self):
        return self.convert(self.scrape())



# if __name__ == "__main__":
#   getdata = GetData
        



