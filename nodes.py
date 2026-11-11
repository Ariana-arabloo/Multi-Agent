from langchain_core.messages import AIMessage
from state import AgentState

def developer_node(state: AgentState):
    print("--- DEVELOPER AGENT WORKING ---")
    return {"messages": [AIMessage(content="Code has been written.")]}

def tester_node(state: AgentState):
    print("--- TESTER AGENT WORKING ---")
    return {"messages": [AIMessage(content="Critical: I found a bug!")]}