# Simple LLM Workflow

## What the code does:

1. **State Definition** (`LLMState`): Defines the workflow's data structure with two fields:
   - `question`: The input question to ask the LLM
   - `answer`: The LLM's response

2. **Node Function** (`get_llm_response`): 
   - Takes the current state
   - Sends the question to ChatOpenAI using `model.invoke()`
   - Extracts the text response from `response.content`
   - Updates the state with the answer

3. **Workflow Graph**:
   - **START** → **Get LLM Response** → **END**
   - Simple linear workflow with one processing node

4. **Execution**:
   - Initializes state with a question
   - Runs the workflow which calls OpenAI's API
   - Returns the final state with the answer

## Key Points:
- Uses `model.invoke(question)` to call ChatOpenAI (not `predict()`)
- Accesses `response.content` to get the actual text from the message object
- Demonstrates basic LangGraph workflow with LLM integration
- Requires `OPENAI_API_KEY` environment variable (loaded from `.env` file)
