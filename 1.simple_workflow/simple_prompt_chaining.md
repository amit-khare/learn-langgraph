# Simple Prompt Chaining

## What the code does:

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

## Key Points:
- Demonstrates **sequential processing** where outputs chain to inputs
- Each node enriches the state progressively
- Shows how to break complex LLM tasks into smaller steps
- Output of first LLM call influences the second LLM call
- Requires `OPENAI_API_KEY` environment variable (loaded from `.env` file)
- Uses state to pass data between nodes automatically
