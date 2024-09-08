from dotenv import dotenv_values
import praw


def reddit_commenter(input_list):
    """
    Comments given text on a given subreddit post.

    Parameters:
    input_list (list): A list containing the id of the post and the text of the comment.
        - The first element is the id of the post.
        - The second element is the text to comment.

        Example format: ["23322", "What a beautiful cat!"]

    Returns:
    (str): The formatted comment or an error message if something goes wrong.
    """
    CONFIG = dotenv_values("config/.env")
    id_comment = input_list[0]
    comment = input_list[1]

    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id=CONFIG["CLIENT_ID"],
        client_secret=CONFIG["CLIENT_SECRET"],
        user_agent="Commenter",
        username=CONFIG["USERNAME"],
        password=CONFIG["PASSWORD"]
    )

    try:
        post = reddit.submission(id=id_comment)
        replied = post.reply(comment)
        return replied

    except Exception as e:
        return f"An unexpected error occurred: {e}"
