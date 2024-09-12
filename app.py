from models.llama_3_1_70B import llama_3_1_70B
from tools.reddit_scrapper import reddit_scrapper
from tools.reddit_commenter import reddit_commenter
from termcolor import colored
import json


def prepare_system_prompts():
    with open("prompts/sentiment_analyzer.md", "r") as file:
        system_prompt_sentiment_analyzer = file.read()
    with open("prompts/writer.md", "r") as file:
        system_prompt_writer = file.read()
    return system_prompt_sentiment_analyzer, system_prompt_writer


def chain_of_action(model, system_prompt_sentiment_analyzer, system_prompt_writer):
    # If you want to try it out with your own text, comment the block of code below
    # (from reddit_scrape =, to post_id =) and uncomment this:

    post = "life is getting more and more expensive"

    try:
        """
        # Scrape reddit posts for questions
        reddit_scrape = reddit_scrapper(["unpopularopinion", "1"])
        post = json.loads(reddit_scrape)
        print(type(post))
        print(colored("Somebody in reddit has this question:", "magenta"))
        print(f"Title: {post["Title"]}\nBody: {post["Body"]}")
        post_id = post["id"]
        """

        # Give post to sentiment analyzer
        plan_prompt = f"""
        {{
        "post": "{post}"
        }}
        """

        analysis = model.answer(
            system_prompt=system_prompt_sentiment_analyzer, prompt=plan_prompt, json=True)
        print(analysis)
        analysis = json.loads(analysis)
        print(colored("\nWhat I've extracted from this post:",
                      "magenta") + "\nDefending points: ")
        for point in analysis["defending_points"]:
            print(point)
        print(
            "\n- - - - - - - - - -\n\n" + colored("My counterarguments:", "magenta") + f"""\n{analysis["argument1"]}\n\n{analysis["argument2"]}\n\n{analysis["argument3"]}\nRage-baiter: {analysis["offend"]}""")

        # Use the writer to write the comment
        write_prompt = f"""
        {{
        "post": {post},
        "defending_points": {analysis["defending_points"]},
        "argument1": {analysis["argument1"]},
        "argument2": {analysis["argument2"]},
        "argument3": {analysis["argument3"]},
        "offend": {analysis["offend"]}
        }}
        """
        writer = model.answer(
            system_prompt=system_prompt_writer, prompt=write_prompt, json=False)
        print(writer)
        print("My answer:")
        print(colored(f"""\n\n{writer}""", "cyan"))

        # Use the reddit_commenter tool. Uncomment next line to actually write a comment under the post
        # reddit_commenter(post_id, writer)

    except Exception as e:
        print(colored("There was an error parsing the JSON object, probably, the model outputted a wrongly formatted JSON object. Try to run the program again :)", "green"))
        print(e)


if __name__ == "__main__":

    model = llama_3_1_70B()
    system_prompt_sentiment_analyzer, system_prompt_writer = prepare_system_prompts()
    chain_of_action(model, system_prompt_sentiment_analyzer=system_prompt_sentiment_analyzer,
                    system_prompt_writer=system_prompt_writer)
