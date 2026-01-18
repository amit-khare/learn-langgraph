from langgraph.graph import StateGraph, START, END
from typing import TypedDict


# Define states

class BMIState(TypedDict):
    weight: float  # in kilograms
    height: float  # in meters
    bmi: float     # Body Mass Index
    category: str  # BMI Category

def calculate_bmi(state: BMIState) -> BMIState:
    weight = state["weight"]
    height = state["height"]
    bmi = weight / (height ** 2)
    state["bmi"] = round(bmi, 2)
    return state

def categorize_bmi(state: BMIState) -> BMIState:
    bmi = state["bmi"]
    if bmi < 18.5:
        state["category"] = "Underweight"
    elif 18.5 <= bmi < 24.9:
        state["category"] = "Normal weight"
    elif 25 <= bmi < 29.9:
        state["category"] = "Overweight"
    else:
        state["category"] = "Obesity"
    return state

# Define the workflow graph
graph = StateGraph(BMIState)

# Add nodes to your graph
graph.add_node("Calculate BMI", calculate_bmi)
graph.add_node("Categorize BMI", categorize_bmi)

# add edges to your graph
graph.add_edge(START, "Calculate BMI")
graph.add_edge("Calculate BMI", "Categorize BMI")
graph.add_edge("Categorize BMI", END)   
# compile the graph
workflow   = graph.compile()

# execute the workflow with sample data
initial_state: BMIState = {
        "weight": 70.0,  # kg
        "height": 1.75,  # meters
        "bmi": 0.0       # placeholder
    }
final_state = workflow.invoke(initial_state)

print(f"Calculated BMI: {final_state['bmi']}") # Output: Calculated BMI: 22.86
print(final_state)

# Visualize the workflow
try:
    from IPython.display import Image, display
    display(Image(workflow.get_graph().draw_mermaid_png()))
except Exception:
    # If not in Jupyter, print ASCII representation
    print("\nWorkflow Graph:")
    print(workflow.get_graph().draw_ascii())
  

