import praw
from praw.models import MoreComments
import pandas as pd

class GetData:
	def __init__(self):

		# Create "reddit" object
		self.reddit = praw.Reddit(client_id='pjzGSwuoF7dgxA', client_secret='PIW3cZ1TiX9i5VVhr-wjdQvWT8ik1w', user_agent='WebScraping')
	def scrape(self, )
		#Blank list for hottest posts and their attributes
		posts = []

		# obtain most recent posts from wallstreetbets with regard to GME
		queried_posts = reddit.subreddit('wallstreetbets').search("GME", 'hot', 'day')



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
	        submission = reddit.submission(id = id)
	        comments = []
	        for top_level_comment in submission.comments:
	            comments.append(top_level_comment.body)
	        
	        stock["post_{}".format(i)] = {"id": df.iloc[i].id, "title": df.iloc[i].title, "score": df.iloc[i].score,
	                                      "num_comments": df.iloc[i].num_comments, "url": df.iloc[i].url, 
	                                      "created": df.iloc[i].created, "comments": comments}
	    return stock


