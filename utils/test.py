import praw
from praw.models import MoreComments
import pandas as pd


# Create "reddit" object
reddit = praw.Reddit(client_id='pjzGSwuoF7dgxA', client_secret='PIW3cZ1TiX9i5VVhr-wjdQvWT8ik1w', user_agent='WebScraping')

#Blank list for hottest posts and their attributes
posts = []

# obtain top 10 hottest posts from wallstreetbets
hot_posts = reddit.subreddit('wallstreetbets').hot(limit=10)

print("TOP 10 HOTTEST POSTS ON /rwallstreetbets: \n \n")

# Loop through 10 hottest posts and print title
count=1
for post in hot_posts:
    print("Post #{}:   {}\n".format(count, post.title))
    count+=1

    # append post attributes to list
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])

# Create Dataframe for top 10 hottest posts
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
print(posts)


url = posts.url[0]
submission = reddit.submission(url = url)

print("\n \n \n \n \n \n")
# for top_level_comment in submission.comments:
#     print(top_level_comment.body)
print(len(submission.comments))
