from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

class BlogState(TypedDict):
    topic: str
    outline: str
    content: str

def generate_outline(state: BlogState) -> BlogState:
    topic = state["topic"]
    prompt = f"Generate a detailed outline for a blog post about: {topic}"
    response = model.invoke(prompt)
    state["outline"] = response.content
    return state


def generate_content(state: BlogState) -> BlogState:
    outline = state["outline"]
    prompt = f"Write a detailed blog post based on the following outline:\n{outline}"
    response = model.invoke(prompt)
    state["content"] = response.content
    return state

graph = StateGraph(BlogState)

# Add nodes to the graph
graph.add_node("Generate Outline", generate_outline)
graph.add_node("Generate Content", generate_content)    

# Add edges to the graph
graph.add_edge(START, "Generate Outline")
graph.add_edge("Generate Outline", "Generate Content")
graph.add_edge("Generate Content", END) 

# Compile the graph into a workflow
workflow = graph.compile()

# Execute the workflow with sample data
initial_state: BlogState = {
    "topic": "The Future of Artificial Intelligence",
    "outline": "",
    "content": ""
}

final_state = workflow.invoke(initial_state)

print("Blog Outline:")
print(final_state["outline"])
print("\nBlog Content:")
print(final_state["content"])   



# Visualize the workflow
try:
    from IPython.display import Image, display
    display(Image(workflow.get_graph().draw_mermaid_png()))
except Exception:
    # If not in Jupyter, print ASCII representation
    print("\nWorkflow Graph:")
    print(workflow.get_graph().draw_ascii())