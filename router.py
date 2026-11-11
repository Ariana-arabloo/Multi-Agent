from langgraph.graph import END
from state import AgentState

def tester_router(state: AgentState) -> str:
    last_message = state["messages"][-1].content
    
    if "Critical" in last_message:
        print("Router: Bug found, routing back to Developer 🔄")
        return "developer_node"
    
    print("Router: Code approved, finishing process ✅")
    return END