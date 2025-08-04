from langchain_experimental.agents import create_csv_agent

from entities.ollama_entities import Llama3

model = Llama3().create()

agent = create_csv_agent(model, "xyz.csv", verbose=True, allow_dangerous_code=True,
                         handle_parsing_errors=True)
agent.run("How many rows?")
agent.run("What is the highest price?")
