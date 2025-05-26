from src.agent import Agent
from src.tools import basic_calculator, reverse_string, get_bangkok_weather
from src.llm import OllamaModel
from src.config import DEFAULT_MODEL, DEFAULT_STOP_TOKEN

if __name__ == "__main__":
    tools = [basic_calculator, reverse_string, get_bangkok_weather]
    model_service = OllamaModel
    model_name = DEFAULT_MODEL
    stop = DEFAULT_STOP_TOKEN

    agent = Agent(tools, model_service, model_name, stop)

    while True:
        prompt = input("Ask me anything: ")
        if prompt.lower() == "exit":
            break

        agent.work(prompt)