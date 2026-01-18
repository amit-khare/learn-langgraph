from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal



# Define a simple state for condition routing
class ConditionState(TypedDict):
    value: int
    status: Literal["big", "small"]
    iteration: int
    max_iterations: int
    result: str

def pass_through(state: ConditionState):
    iteration = state['iteration'] + 1
    return {"iteration": iteration}

def decide_next(state: ConditionState):
    if state["value"] > 10:
        return "big"
    return "small"

def big_node(state: ConditionState) -> ConditionState:
    return {"result": "Value is big"}

def small_node(state: ConditionState) -> ConditionState:
    return {"result": "Value is small"}

def check_iteration(state: ConditionState) -> Literal["continue_small", "end"]:
    if state['iteration'] < state['max_iterations']:
        return "continue_small"
    else:
        return "end"
    
# Define the workflow graph
graph = StateGraph(ConditionState)

# Add nodes to your graph
graph.add_node("big", big_node)
graph.add_node("small", small_node)
graph.add_node("pass_through", pass_through)

# add edges to your graph
graph.add_conditional_edges(START, decide_next, {"big": "big", "small": "small"})
graph.add_edge("big", END)
graph.add_edge("small", "pass_through")
graph.add_conditional_edges("pass_through", check_iteration, {"continue_small": "small", "end": END})

workflow = graph.compile()

# execute the workflow with sample data
initial_state: ConditionState = {
    "value": 5,        
    "status": "small",
    "iteration": 0,
    "max_iterations": 3,
    "result": ""
}
final_state = workflow.invoke(initial_state)
print(f"Final Result: {final_state['result']}") # Output: Final Result: Value is small

print(f"Iterations: {final_state['iteration']}") # Output: Iterations: 1

# Visualize the workflow
try:
    from IPython.display import Image, display
    display(Image(workflow.get_graph().draw_mermaid_png()))
except Exception:
    # If not in Jupyter, print ASCII representation
    print("\nWorkflow Graph:")
    print(workflow.get_graph().draw_ascii())
