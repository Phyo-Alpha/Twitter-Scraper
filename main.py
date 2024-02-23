from fastapi import FastAPI, Body
from datetime import datetime

from tweety import Twitter

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello from deep purple webscraper and AI"}


@app.get("/tweets/{username}")
async def get_tweets(username: str):
    user_tweets = {}

    app = Twitter("session")
    app.sign_in("edwardAIbot1", "35571559")
    target_username = username

    user_info = app.get_user_info(target_username)
    all_tweets = app.get_tweets(target_username, pages=1)

    user_tweets["name"] = user_info.name
    user_tweets["username"] = user_info.username
    user_tweets["tweets"] = []
    for tweet in all_tweets:
        try:
            date = tweet.created_on.strftime("%Y/%m/%d")
            user_tweet = {
                "tweet-id": tweet.id,
                "tweet": tweet.text,
                "date": date,
                "likes": tweet.likes,
                "views": tweet.views,
                "reply_count": tweet.reply_counts,
                "replies": [],
            }
            stop = False
            for thread in tweet.get_comments(pages=1, wait_time=2):
                if stop:
                    break
                for reply in thread.tweets:
                    user_comment = {
                        "author": reply.author.username,
                        "comment": reply.text,
                    }
                    user_tweet.get("replies").append(user_comment)

                    if len(user_tweet.get("replies")) >= 2:
                        stop = True
                        break
            user_tweets.get("tweets").append(user_tweet)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

    return user_tweets


@app.get("/getUserInfo/{username}")
async def get_user_info(username: str):
    app = Twitter("session")
    app.sign_in("edwardAIbot1", "35571559")
    user_info = app.get_user_info(username)

    return user_info
