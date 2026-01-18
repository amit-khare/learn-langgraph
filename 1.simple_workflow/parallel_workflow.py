from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv


load_dotenv()

# Define states for parallel tasks
class BatsState(TypedDict):
    runs : int
    balls : int
    fours : int
    sixes : int
    sr: float
    ballsperrun: float
    bountrate: float

def calculate_bountrate(state: BatsState) -> BatsState:
    fours = state["fours"]
    sixes = state["sixes"]
    balls = state["balls"]
    bountrate = ((fours + sixes) / balls) * 100 if balls > 0 else 0
    state["bountrate"] = round(bountrate, 2)
    return {"bountrate": state["bountrate"]}

def calculate_strike_rate(state: BatsState) -> BatsState:
    runs = state["runs"]
    balls = state["balls"]
    sr = (runs / balls) * 100 if balls > 0 else 0
    state["sr"] = round(sr, 2)
    return {"sr": state["sr"]}

def calculate_balls_per_run(state: BatsState) -> BatsState:
    runs = state["runs"]
    balls = state["balls"]
    ballsperrun = (balls / runs) if runs > 0 else 0
    state["ballsperrun"] = round(ballsperrun, 2)
    return {"ballsperrun": state["ballsperrun"]}

# Define the workflow graph
graph = StateGraph(BatsState)

# Add nodes to your graph
graph.add_node("Calculate Strike Rate", calculate_strike_rate)
graph.add_node("Calculate Balls Per Run", calculate_balls_per_run)
graph.add_node("Calculate Bounce Rate", calculate_bountrate)
# add edges to your graph
graph.add_edge(START, "Calculate Strike Rate")
graph.add_edge(START, "Calculate Balls Per Run")
graph.add_edge(START, "Calculate Bounce Rate")
graph.add_edge("Calculate Strike Rate", END)
graph.add_edge("Calculate Balls Per Run", END)
graph.add_edge("Calculate Bounce Rate", END)

# compile the graph
workflow   = graph.compile()

# execute the workflow with sample data
initial_state: BatsState = {
        "runs": 150,
        "balls": 120,
        "fours": 10,
        "sixes": 5,
        "sr": 0.0,
        "ballsperrun": 0.0,
        "bountrate": 0.0    
    }

final_state = workflow.invoke(initial_state)

print(f"Calculated Strike Rate: {final_state['sr']}") # Output: Calculated Strike Rate: 125.0
print(f"Calculated Balls Per Run: {final_state['ballsperrun']}") # Output: Calculated Balls Per Run: 0.8
print(f"Calculated Bounce Rate: {final_state['bountrate']}") # Output: Calculated Bounce Rate: 12.5

# Visualize the workflow
try:
    from IPython.display import Image, display
    display(Image(workflow.get_graph().draw_mermaid_png()))
except Exception:
    # If not in Jupyter, print ASCII representation
    print("\nWorkflow Graph:")
    print(workflow.get_graph().draw_ascii()) 

    