import os

from langchain_experimental.agents import create_csv_agent

from entities.ollama_entities import Llama3
from utils.paths import DATA

model = Llama3().create()

agent = create_csv_agent(model, os.path.join(DATA, "restaurant_sales.csv"), verbose=True, allow_dangerous_code=True,
                         handle_parsing_errors=True)
agent.run("What is the most sold Product?")
agent.run("Which manager has the highest profit?")
