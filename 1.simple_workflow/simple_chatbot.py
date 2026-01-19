from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class ChatState(TypedDict):
    chat_history: Annotated[list[BaseMessage], add_messages]

model = ChatOpenAI()

def chat_response(state: ChatState):
    chat_history = state["chat_history"]
    response = model.invoke(chat_history)
    return {"chat_history": [response]}

checkpoint = MemorySaver()

# Define the workflow graph
graph = StateGraph(ChatState)

# Add nodes to your graph
graph.add_node("Chat Response", chat_response)

# add edges to your graph
graph.add_edge(START, "Chat Response")
graph.add_edge("Chat Response", END)    

# compile the graph
workflow = graph.compile(checkpointer=checkpoint)

print("Chat History:")

config = {'configurable': {'thread_id': '1'}}
while True:
    user_messages = input("You: ")
    if user_messages.lower() in ['exit', 'quit']:
        break
    final_state = workflow.invoke({'chat_history': [HumanMessage(content=user_messages)]}, config=config)
    print('AI: ', final_state['chat_history'][-1].content)
