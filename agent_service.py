import json

def get_agent_prompt(agent_name):
    try:
        with open('agents.json', 'r', encoding='utf-8') as file:
            agents_data = json.load(file)
        
        if agent_name in agents_data:
            return agents_data[agent_name]["system_prompt"]
        else:
            return "Error: Agent not found!"
            
    except FileNotFoundError:
        return "Error: agents.json file is missing!"