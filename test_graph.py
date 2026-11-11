from langgraph.graph import StateGraph, START
from langchain_core.messages import HumanMessage

from state import AgentState
from nodes import developer_node, tester_node
from router import tester_router

workflow = StateGraph(AgentState)

workflow.add_node("developer_node", developer_node)
workflow.add_node("tester_node", tester_node)

workflow.add_edge(START, "developer_node")
workflow.add_edge("developer_node", "tester_node")

workflow.add_conditional_edges(
    "tester_node", 
    tester_router
)

app = workflow.compile()

if __name__ == "__main__":
    print("🚀 Starting the system...")
    
    initial_state = {"messages": [HumanMessage(content="Please write a calculator app")]}
    
    app.invoke(initial_state, {"recursion_limit": 4})