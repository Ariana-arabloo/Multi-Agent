from langchain_core.messages import AIMessage, SystemMessage
from state import AgentState
from agent_service import get_agent_prompt

def developer_node(state: AgentState):
    print("--- DEVELOPER AGENT WORKING ---")
    system_prompt = get_agent_prompt("developer_agent")
    messages_to_send = [SystemMessage(content=system_prompt)] + state["messages"]
    
    return {"messages": [AIMessage(content="Code has been written.")]}

def tester_node(state: AgentState):
    print("--- TESTER AGENT WORKING ---")
    system_prompt = get_agent_prompt("security_tester_agent")
    messages_to_send = [SystemMessage(content=system_prompt)] + state["messages"]
    
    return {"messages": [AIMessage(content="Critical: I found a bug!")]}