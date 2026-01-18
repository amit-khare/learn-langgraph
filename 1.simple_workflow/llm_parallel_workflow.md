# LLM Parallel Workflow

## What the code does:

This demonstrates **parallel LLM execution with structured outputs and list aggregation** - where multiple LLM calls run simultaneously to evaluate different aspects of an essay, and their results are combined.

1. **Structured Output Schema** (`FeedbackSchema`): Uses Pydantic to enforce LLM response structure:
   - `feedback`: Detailed textual feedback (string)
   - `score`: Numeric score out of 10 (int, constrained between 0-10)

2. **State Definition** (`EssayEvalution`): Manages the essay evaluation workflow:
   - `essay`: The essay text to evaluate
   - `clarity_of_thought_feedback`: Feedback on clarity (string)
   - `depth_of_analysis_feedback`: Feedback on analytical depth (string)
   - `language_feedback`: Feedback on language quality (string)
   - `individual_scores`: **Annotated list** to collect scores from parallel evaluators
   - `avg_score`: Final average score (float)
   - `final_feedback`: Comprehensive summary feedback (string)

3. **Parallel Evaluation Nodes** (all run simultaneously):
   - **`evaluate_clarity_of_thought`**: 
     - Analyzes essay clarity and organization
     - Returns clarity feedback and score as a single-item list
   
   - **`evaluate_depth_of_analysis`**:
     - Evaluates depth and complexity of analysis
     - Returns depth feedback and score as a single-item list
   
   - **`evaluate_language`**:
     - Assesses grammar, vocabulary, and writing style
     - Returns language feedback and score as a single-item list

4. **Aggregation Node**:
   - **`finalize_evaluation`**:
     - Runs **after** all parallel evaluations complete
     - Uses LLM to synthesize all feedbacks into comprehensive summary
     - Calculates final average score from collected scores
     - Returns final feedback and average score

5. **Workflow Graph**:
   ```
   START → Evaluate Clarity of Thought ↘
       ↘ Evaluate Depth of Analysis → Finalize Evaluation → END
       ↘ Evaluate Language           ↗
   ```
   - Three evaluation nodes run in parallel
   - All converge to the finalization node
   - Finalization waits for all evaluations before proceeding

6. **Execution**:
   - Initializes state with an essay about "pieces"
   - Three LLM calls execute in parallel (3x faster than sequential)
   - Each returns specific feedback and a score
   - Finalization combines all feedback into comprehensive evaluation
   - Outputs individual scores and final synthesized feedback

7. **Visualization**:
   - Shows parallel execution with convergence pattern
   - Three branches from START merging into Finalize Evaluation

## Key Points:

### Advanced Pattern: `Annotated` with Reducers
```python
individual_scores: Annotated[list[int], operator.add]
```
- **Why needed**: Multiple parallel nodes return scores simultaneously
- **What it does**: `operator.add` combines lists by concatenating them
- **Result**: `[6] + [5] + [7]` → `[6, 5, 7]`
- **Without it**: Would throw `InvalidUpdateError` because LangGraph doesn't know how to merge concurrent updates

### Structured Outputs
```python
structure_model = model.with_structured_output(FeedbackSchema)
```
- Forces LLM responses to match Pydantic schema
- Guarantees `feedback` (string) and `score` (0-10 int) fields
- Eliminates parsing errors and ensures consistent data structure

### Partial Returns Pattern
```python
return {"clarity_of_thought_feedback": response.feedback, "individual_scores": [response.score]}
```
- Each node returns **only the fields it updates**
- Prevents conflicts when parallel nodes run simultaneously
- List items are wrapped in brackets to create single-item lists

### Convergence Pattern
- Multiple parallel nodes → Single aggregation node
- LangGraph automatically waits for all parallel nodes to complete
- Aggregation node sees combined results from all parallel executions
- Useful for map-reduce style operations

## Use Cases:
- Multi-criteria evaluation (essays, code reviews, product reviews)
- Parallel data processing with aggregation
- Concurrent API calls with result combination
- Fan-out/fan-in workflow patterns

## Requirements:
- `OPENAI_API_KEY` environment variable
- Pydantic for schema validation
- Understanding of `Annotated` types and reducer functions
