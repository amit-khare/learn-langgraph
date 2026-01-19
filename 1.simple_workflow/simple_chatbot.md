# Simple Chatbot

## What the code does:

This demonstrates **a stateful chatbot with conversation memory** - where the chatbot maintains conversation history across multiple turns using LangGraph's checkpointing mechanism.

## Workflow Structure:

1. **State Definition** (`ChatState`): Defines the conversation state:
   - `chat_history`: **Annotated list of messages** with `add_messages` reducer
   - Automatically handles message accumulation across conversation turns
   - Preserves both user and AI messages in chronological order

2. **Message Reducer** (`add_messages`):
   - Special LangGraph reducer for message handling
   - Automatically appends new messages to existing history
   - Prevents duplicate messages
   - Maintains proper message order

3. **Chat Response Node**:
   - **`chat_response`**:
     - Receives the entire chat history from state
     - Sends full history to ChatOpenAI for context-aware responses
     - Returns the AI response as a single-item list
     - `add_messages` reducer automatically appends it to history

4. **Memory Checkpointing** (`MemorySaver`):
   - Persists conversation state in memory
   - Associates conversation with a unique `thread_id`
   - Retrieves previous messages when continuing conversation
   - Enables multi-turn conversations with context

5. **Workflow Graph**:
   ```
   START → Chat Response → END
   ```
   - Simple linear workflow for each turn
   - Each invocation adds one user message and one AI response
   - State is preserved between invocations via checkpointer

6. **Interactive Loop**:
   - Prompts user for input
   - Creates HumanMessage with user's text
   - Invokes workflow with message and thread config
   - Displays AI's response
   - Repeats until user types 'exit' or 'quit'

## Key Components:

### Annotated Message List:
```python
chat_history: Annotated[list[BaseMessage], add_messages]
```
- `Annotated` type tells LangGraph how to handle updates
- `add_messages` is a special reducer for message lists
- Automatically merges new messages with existing history
- Smarter than simple list concatenation (handles duplicates, ordering)

### Thread Configuration:
```python
config = {'configurable': {'thread_id': '1'}}
```
- `thread_id` identifies this conversation thread
- Same thread_id retrieves same conversation history
- Different thread_ids create separate conversations
- Required when using checkpointers

### Checkpointer Compilation:
```python
workflow = graph.compile(checkpointer=checkpoint)
```
- Compiles workflow with memory persistence
- Every workflow invocation saves state automatically
- State retrieved automatically on next invocation
- No manual state management needed

### Message Types:
```python
HumanMessage(content=user_messages)  # User input
response  # AIMessage from ChatOpenAI
```
- LangChain message types provide structure
- Each message knows its role (human, AI, system)
- Enables proper conversation formatting for LLM

## How It Works:

### First Turn:
1. User enters: "Hello"
2. HumanMessage created and added to state
3. Workflow invokes with initial state
4. `chat_response` sends history to LLM
5. LLM responds: "Hi! How can I help you?"
6. Response added to chat_history via `add_messages`
7. State saved to checkpoint with thread_id='1'
8. AI response displayed to user

### Second Turn:
1. User enters: "What's the weather?"
2. HumanMessage created
3. Workflow invoked with same thread_id
4. Checkpointer retrieves previous history (Hello + AI response)
5. New message added to existing history
6. Full history sent to LLM (context-aware!)
7. LLM responds based on full conversation
8. Updated state saved to checkpoint
9. AI response displayed

### Conversation Flow:
```
Turn 1: [HumanMessage("Hello")] → [HumanMessage("Hello"), AIMessage("Hi!")]
Turn 2: [HumanMessage("What's the weather?")] → [previous + HumanMessage + AIMessage]
Turn 3: [HumanMessage("Thanks")] → [all previous + HumanMessage + AIMessage]
```

## Advanced Features:

### Automatic State Management:
- No manual history tracking needed
- Checkpointer handles persistence automatically
- `add_messages` handles message merging
- Just pass new messages, framework handles rest

### Context-Aware Responses:
- LLM sees entire conversation history
- Can reference previous messages
- Maintains conversation coherence
- Natural multi-turn dialogue

### Thread Isolation:
- Different thread_ids = different conversations
- Can maintain multiple conversations simultaneously
- Thread-safe state management
- Perfect for multi-user applications

### Memory Persistence:
- `MemorySaver` keeps conversations in RAM
- Fast access for development/testing
- For production, use persistent checkpointers:
  - `SqliteSaver` - disk-based persistence
  - `PostgresSaver` - database persistence
  - Custom checkpointers for other backends

## Use Cases:

### Customer Support Chatbot:
- Track conversation across multiple messages
- Context-aware responses
- Thread per customer for conversation isolation

### Personal Assistant:
- Remember conversation context
- Multi-turn task completion
- Maintain user preferences across session

### Educational Tutor:
- Track learning progress in conversation
- Reference previous explanations
- Build on prior knowledge

### Interview Bot:
- Follow-up questions based on answers
- Maintain interview context
- Coherent conversation flow

## Example Conversation:

```
You: Hello
AI: Hi! How can I help you today?

You: What's the capital of France?
AI: The capital of France is Paris.

You: How many people live there?
AI: Paris has approximately 2.2 million people in the city proper, and about 12 million in the metropolitan area.

You: Thanks!
AI: You're welcome! Let me know if you have any other questions.

You: exit
```

Notice how the AI understands "there" refers to Paris from previous context!

## Important Patterns:

### Message Return Format:
```python
return {"chat_history": [response]}
```
- Return AI message as single-item list
- `add_messages` automatically appends to history
- Don't return full history (that would duplicate messages)

### Input Format:
```python
workflow.invoke({'chat_history': [HumanMessage(content=user_messages)]}, config=config)
```
- Pass user message as list
- Include thread config for state retrieval
- Framework merges with existing history

### Exit Condition:
```python
if user_messages.lower() in ['exit', 'quit']:
    break
```
- Simple exit mechanism
- Could add save/export functionality here
- Could display conversation summary

## Comparison with Other Approaches:

**vs. Stateless Chat:**
- Stateless: Each message independent, no context
- This: Full conversation context, coherent dialogue

**vs. Manual History Management:**
- Manual: Track messages in variables, pass to LLM
- This: Automatic persistence, reducer handles merging

**vs. Simple LLM Call:**
- Simple: One-off question/answer
- This: Multi-turn conversation with memory

## Extending the Chatbot:

### Add System Message:
```python
from langchain_core.messages import SystemMessage

initial_state = {
    'chat_history': [SystemMessage(content="You are a helpful assistant.")]
}
workflow.invoke(initial_state, config=config)
```

### Add Message Limit:
```python
def chat_response(state: ChatState):
    # Keep only last 10 messages
    recent_history = state["chat_history"][-10:]
    response = model.invoke(recent_history)
    return {"chat_history": [response]}
```

### Save Conversation:
```python
import json

def save_conversation(chat_history, filename):
    messages = [{"role": msg.type, "content": msg.content} for msg in chat_history]
    with open(filename, 'w') as f:
        json.dump(messages, f, indent=2)
```

### Multiple Threads:
```python
# Conversation 1
config1 = {'configurable': {'thread_id': 'user_123'}}

# Conversation 2  
config2 = {'configurable': {'thread_id': 'user_456'}}

# Each maintains separate history
```

## Requirements:
- `OPENAI_API_KEY` environment variable
- Understanding of message types (HumanMessage, AIMessage)
- Checkpointing concepts
- `add_messages` reducer behavior

## Common Patterns:

### Interactive Input Loop:
- Read user input continuously
- Exit condition check
- Response display
- Standard pattern for CLI chatbots

### Thread-Based State:
- One thread per conversation
- State automatically persisted
- State automatically retrieved
- Clean separation of conversations

### Message Accumulation:
- Each turn adds 2 messages (human + AI)
- History grows over time
- Consider message limit for long conversations
- Balance context vs. token costs

## Production Considerations:

1. **Message Limit**: Prevent unlimited history growth
2. **Persistent Storage**: Use SqliteSaver or PostgresSaver instead of MemorySaver
3. **Error Handling**: Handle API failures, network issues
4. **Rate Limiting**: Protect against spam/abuse
5. **User Authentication**: Secure thread access
6. **Conversation Export**: Allow users to save/export chats
7. **Timeout Handling**: Handle long LLM response times
8. **Cost Tracking**: Monitor token usage per conversation
