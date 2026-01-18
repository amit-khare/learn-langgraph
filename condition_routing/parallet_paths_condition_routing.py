from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add


# Define a simple state for parallel path routing
class ParallelState(TypedDict):
    value: int
    results: Annotated[list[str], add]  # Collect results from parallel nodes

def decide_parallel(state: ParallelState):
    # Return a list to execute multiple nodes in parallel
    return ["big", "small"]

def big_node(state: ParallelState):
    return {"results": [f"Big processed value: {state['value']}"]}

def small_node(state: ParallelState):
    return {"results": [f"Small processed value: {state['value']}"]}

# Define the workflow graph
graph = StateGraph(ParallelState)

# Add nodes to your graph
graph.add_node("big", big_node)
graph.add_node("small", small_node)

# add edges to your graph
# When decide_parallel returns a list, both nodes execute in parallel
graph.add_conditional_edges(START, decide_parallel)
graph.add_edge("big", END)
graph.add_edge("small", END)

workflow = graph.compile()

# execute the workflow with sample data
initial_state: ParallelState = {
    "value": 42,
    "results": []
}

final_state = workflow.invoke(initial_state)
print("Parallel Execution Results:")
for result in final_state['results']:
    print(f"  - {result}")

# Visualize the workflow
try:
    from IPython.display import Image, display
    display(Image(workflow.get_graph().draw_mermaid_png()))
except Exception:
    # If not in Jupyter, print ASCII representation
    print("\nWorkflow Graph:")
    print(workflow.get_graph().draw_ascii())
