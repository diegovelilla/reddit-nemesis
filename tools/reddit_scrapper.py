from dotenv import dotenv_values
import praw
import json


def reddit_scrapper(input_list):
    """
    Scrapes given subreddit's today's top posts for a number of posts.

    Parameters:
    input_list (list): A list containing the name of the subreddit and the number of tweets to scrape.
        - The first element is the name of the subreddit.
        - The second element is the number of posts to scrape.

        Example format: ["cats", "5"]

    Returns:
    (str): The formatted weather or an error message if something goes wrong.
    """
    CONFIG = dotenv_values("config/.env")
    subreddit_name = input_list[0]
    num_posts = int(input_list[1])

    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id=CONFIG["CLIENT_ID"],
        client_secret=CONFIG["CLIENT_SECRET"],
        user_agent="Scrapper"
    )

    try:
        # Get the subreddit
        user = reddit.redditor("TARGET_USERNAME")

        subreddit = reddit.subreddit(subreddit_name)
        top_posts = subreddit.top(limit=num_posts, time_filter="day")

        result = []
        for post in top_posts:
            if not post.stickied:
                body = post.selftext.replace("\n", " ")
                post_data = {
                    "Title": post.title,
                    "Body": body,
                    "id": post.id
                }
                result.append(post_data)
        return json.dumps(result, indent=4, ensure_ascii=False)

    except Exception as e:
        return f"An unexpected error occurred: {e}"
