import praw
from praw.models import MoreComments
import pandas as pd


# Create "reddit" object
reddit = praw.Reddit(client_id='pjzGSwuoF7dgxA', client_secret='PIW3cZ1TiX9i5VVhr-wjdQvWT8ik1w', user_agent='WebScraping')

#Blank list for hottest posts and their attributes
posts = []

# obtain most recent posts from wallstreetbets with regard to GME
queried_posts = reddit.subreddit('wallstreetbets').search("GME", 'hot', 'day')

print("TOP 10 GME POSTS ON /rwallstreetbets: \n \n")

# Loop through 10 GME posts and print title
count=1
for post in queried_posts:
    print("Post #{}:   {}\n".format(count, post.title))
    count+=1

    # append post attributes to list
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])

# Create Dataframe for top 10 hottest posts
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])


id = posts.id[0]
submission = reddit.submission(id = id)

print("\n \n \n \n \n \n")
# remove all "More Comments"
#submission.comments.replace_more(limit=0)
for top_level_comment in submission.comments:
    print(top_level_comment.body)
