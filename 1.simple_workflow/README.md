# Simple Workflow Examples

## 1. BMI Calculator (`bmi_calculator.py`)

### What the code does:

1. **State Definition** (`BMIState`): Defines the workflow's data structure with three fields:
   - `weight`: Person's weight in kilograms (float)
   - `height`: Person's height in meters (float)
   - `bmi`: Calculated Body Mass Index (float)

2. **Node Function** (`calculate_bmi`):
   - Takes the current state containing weight and height
   - Applies the BMI formula: weight / (height²)
   - Rounds the result to 2 decimal places
   - Updates the state with the calculated BMI

3. **Workflow Graph**:
   - **START** → **Calculate BMI** → **END**
   - Simple linear workflow with one processing node

4. **Execution**:
   - Initializes state with sample data (70 kg, 1.75 m)
   - Runs the workflow to calculate BMI
   - Outputs: BMI = 22.86

5. **Visualization**:
   - Displays ASCII representation of the workflow graph
   - Shows the flow from start through calculation to end

### Key Points:
- Demonstrates basic LangGraph state management
- Single-node workflow for mathematical calculation
- Includes workflow visualization using `draw_ascii()`
- Requires `grandalf` package for graph visualization

---

## 2. Simple LLM Workflow (`simple_llm_workflow.py`)

### What the code does:

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

### Key Points:
- Uses `model.invoke(question)` to call ChatOpenAI (not `predict()`)
- Accesses `response.content` to get the actual text from the message object
- Demonstrates basic LangGraph workflow with LLM integration
- Requires `OPENAI_API_KEY` environment variable (loaded from `.env` file)

---

## 3. Simple Prompt Chaining (`simple_prompt_chaining.py`)

### What the code does:

This demonstrates **prompt chaining** - where the output of one LLM call becomes the input to the next.

1. **State Definition** (`BlogState`): Defines the workflow's data structure with three fields:
   - `topic`: Input topic for the blog post
   - `outline`: Generated outline (output of first node)
   - `content`: Final blog content (output of second node)

2. **Node Functions**:
   - **`generate_outline`**: 
     - Takes the topic from state
     - Prompts the LLM to create a detailed outline
     - Saves the outline back to state
   
   - **`generate_content`**:
     - Takes the outline from state
     - Prompts the LLM to write a full blog post based on the outline
     - Saves the content back to state

3. **Workflow Graph**:
   - **START** → **Generate Outline** → **Generate Content** → **END**
   - Sequential workflow where each node builds on the previous node's output

4. **Execution**:
   - Initializes state with a topic: "The Future of Artificial Intelligence"
   - First node generates an outline
   - Second node uses that outline to write the full blog post
   - Outputs both the outline and final content

5. **Visualization**:
   - Displays ASCII representation of the workflow graph
   - Shows the sequential flow through the two processing nodes

### Key Points:
- Demonstrates **sequential processing** where outputs chain to inputs
- Each node enriches the state progressively
- Shows how to break complex LLM tasks into smaller steps
- Output of first LLM call influences the second LLM call
- Requires `OPENAI_API_KEY` environment variable (loaded from `.env` file)
- Uses state to pass data between nodes automatically
