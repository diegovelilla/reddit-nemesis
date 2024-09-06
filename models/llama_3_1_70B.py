from groq import Groq
from dotenv import dotenv_values
import json

CONFIG = dotenv_values("./config/.env")


class llama_3_1_70B:

    def __init__(self):
        """
        Initializes the llama-3.1-70B with the given parameters.
        """
        self.client = Groq(api_key=CONFIG["GROQ_API_KEY"])
        self.model_name = "llama-3.1-70b-versatile"

    def answer(self, system_prompt, prompt):
        """
        Generates a response from the model based on the provided prompt.

        Parameters:
        system_prompt (str): The system_prompt that will change how the agent works.
        prompt (str): The user query to generate a response for.

        Returns:
        str: The response from the model as a string formatted as a list.
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{system_prompt}"
                },
                {
                    "role": "user",
                    "content": f"{prompt}"
                }
            ],
            model=self.model_name
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    model = llama_3_1_70B()
    system_prompt_sentiment_analyzer = ""
    system_prompt_writer = ""
    with open("prompts/sentiment_analizer.md", "r") as file:
        system_prompt_sentiment_analyzer = file.read()
    with open("prompts/writer.md", "r") as file:
        system_prompt_writer = file.read()

    prompt = """hello (no hate)"""
    analyze = model.answer(
        system_prompt=system_prompt_sentiment_analyzer, prompt=prompt)

    response = model.answer(system_prompt=system_prompt_writer, prompt=analyze)
    response = json.loads(response)
    print(response["answer"])
