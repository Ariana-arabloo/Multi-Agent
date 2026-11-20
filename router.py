from langgraph.graph import END
from state import AgentState

def tester_router(state: AgentState):
    is_approved = state.get("is_approved", False)
    
    if is_approved:
        return "end_node"
        
    count = state.get("iteration_count", 0)
    
    if count >= 3:
        return "human_mediation"
    else:
        return "developer_node"