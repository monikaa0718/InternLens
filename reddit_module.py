import praw
from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT
)

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

SUBREDDITS = [
    "internships",
    "csMajors",
    "cscareerquestions"
]


def get_top_comments(submission, limit=5):
    comments = []

    try:
        submission.comments.replace_more(limit=0)

        for comment in submission.comments[:limit]:
            comments.append(comment.body)

    except Exception:
        pass

    return comments


def search_reddit(company_name, limit=5):
    query = f"{company_name} internship"
    results = []

    for sub in SUBREDDITS:
        subreddit = reddit.subreddit(sub)

        for submission in subreddit.search(query, limit=limit):
            comments = get_top_comments(submission)

            results.append({
                "platform": "reddit",
                "title": submission.title,
                "body": (submission.selftext or "") + " " + " ".join(comments),
                "url": f"https://www.reddit.com{submission.permalink}",
                "author": sub,
                "date_posted": str(submission.created_utc),
                "raw_score": submission.score
            })

    for submission in reddit.subreddit("all").search(query, limit=limit):
        comments = get_top_comments(submission)

        results.append({
            "platform": "reddit",
            "title": submission.title,
            "body": (submission.selftext or "") + " " + " ".join(comments),
            "url": f"https://www.reddit.com{submission.permalink}",
            "author": str(submission.subreddit),
            "date_posted": str(submission.created_utc),
            "raw_score": submission.score
        })

    return results