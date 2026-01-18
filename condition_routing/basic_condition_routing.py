from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal



# Define a simple state for condition routing
class ConditionState(TypedDict):
    value: int
    result: str

def pass_through(state: ConditionState) -> ConditionState:
    return state

def decide_next(state: ConditionState) -> Literal["big", "small"]:
    if state["value"] > 10:
        return "big"
    return "small"

def big_node(state: ConditionState) -> ConditionState:
    return {"result": "Value is big"}

def small_node(state: ConditionState) -> ConditionState:
    return {"result": "Value is small"}

# Define the workflow graph
graph = StateGraph(ConditionState)

# Add nodes to your graph
graph.add_node("big", big_node)
graph.add_node("small", small_node)
graph.add_node("pass_through", pass_through)

graph.add_conditional_edges(START, decide_next)
graph.add_edge("big", END)
graph.add_edge("small", "pass_through")
graph.add_edge("pass_through", END)

workflow = graph.compile()

# execute the workflow with sample data
initial_state: ConditionState = {
        "value": 15,        
        "result": ""
    }
final_state = workflow.invoke(initial_state)
print(f"Final Result: {final_state['result']}") # Output: Final Result: Value is big

# Visualize the workflow
try:
    from IPython.display import Image, display
    display(Image(workflow.get_graph().draw_mermaid_png()))
except Exception:
    # If not in Jupyter, print ASCII representation
    print("\nWorkflow Graph:")
    print(workflow.get_graph().draw_ascii())
