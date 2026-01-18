from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

# Create state definitions
class LLMState(TypedDict):
    question: str
    answer: str

# Define a function to get LLM response
def get_llm_response(state: LLMState) -> LLMState:
    question = state["question"]
    response = model.invoke(question)
    state["answer"] = response.content
    return state

# Create a graph
graph = StateGraph(LLMState)

# Add nodes to the graph
graph.add_node("Get LLM Response", get_llm_response)

# Add edges to the graph
graph.add_edge(START, "Get LLM Response")
graph.add_edge("Get LLM Response", END) 

# Compile the graph into a workflow
workflow = graph.compile()

# Execute the workflow with sample data
initial_state: LLMState = {
    "question": "What is the capital of France?",
    "answer": ""
}

final_state = workflow.invoke(initial_state)

print(f"Question: {final_state['question']}")
print(f"Answer: {final_state['answer']}")