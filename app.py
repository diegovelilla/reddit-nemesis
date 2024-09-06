from models.llama_3_1_70B import llama_3_1_70B
from tools.reddit_scrapper import reddit_scrapper
from tools.reddit_commenter import reddit_commenter
import json


def prepare_system_prompts():
    with open("prompts/planner.md", "r") as file:
        system_prompt_planner = file.read()
    with open("prompts/researcher.md", "r") as file:
        system_prompt_researcher = file.read()
    with open("prompts/writer.md", "r") as file:
        system_prompt_writer = file.read()
    return system_prompt_planner, system_prompt_researcher, system_prompt_writer


def chain_of_action(model, system_prompt_sentiment_analyzer, system_prompt_writer):
    # Scrape reddit posts for questions
    reddit_scrape = reddit_scrapper(["unpopularopinion", "1"])
    print(f"Somebody in reddit has this question:\n{reddit_scrape}")
    post = json.loads(reddit_scrape)
    post_id = post["id"]

    # Give post to sentiment analyzer
    plan_prompt = f"""
    {{
    "post": "{reddit_scrape}"
    }}    
    """

    analysis = model.answer(
        system_prompt=system_prompt_sentiment_analyzer, prompt=plan_prompt)
    analysis = json.loads(analysis)
    print("\nFor this question I decided to search:")
    print(analysis["defending_points"])
    print(analysis["argument1"])
    print(analysis["argument2"])
    print(analysis["argument3"])
    print(analysis["offend"])

    # Use the writer to write the comment
    write_prompt = f"""
    {{
    "post": {reddit_scrape},
    "defending_points": {analysis["defending_points"]},
    "argument1": {analysis["argument1"]},
    "argument2": {analysis["argument2"]},
    "argument3": {analysis["argument3"]},
    "offend": {analysis["offend"]}
    }}   
    """
    writer = model.answer(
        system_prompt=system_prompt_writer, prompt=write_prompt)
    print(writer)
    writer = json.loads(writer)
    print(f"""\n\n{writer["answer"]}""")
    """
    # Use the reddit_poster tool
    reddit_commenter(post_id, writer["answer"]])
    """


if __name__ == "__main__":

    model = llama_3_1_70B()
    system_prompt_sentiment_analyzer = ""
    system_prompt_writer = ""
    with open("prompts/sentiment_analizer.md", "r") as file:
        system_prompt_sentiment_analyzer = file.read()
    with open("prompts/writer.md", "r") as file:
        system_prompt_writer = file.read()

    chain_of_action(model, system_prompt_sentiment_analyzer=system_prompt_sentiment_analyzer,
                    system_prompt_writer=system_prompt_writer)
