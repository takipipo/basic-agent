from agent import Agent
from tools import basic_calculator, reverse_string
from llm import OllamaModel

if __name__ == "__main__":
    tools = [basic_calculator, reverse_string]
    model_service = OllamaModel
    model_name = "mistral"
    stop = "<|eot_id|>"

    agent = Agent(tools, model_service, model_name, stop)

    while True:
        prompt = input("Ask me anything: ")
        if prompt.lower() == "exit":
            break

        agent.work(prompt)