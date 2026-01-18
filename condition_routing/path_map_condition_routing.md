# Path Map Condition Routing

## What the code does:

This demonstrates **conditional routing with path mapping and looping** - where the workflow uses explicit path mappings to control routing decisions and creates a loop that executes a limited number of times based on iteration count.

## Workflow Structure:

1. **State Definition** (`ConditionState`): Defines the workflow's data structure:
   - `value`: Numeric value to evaluate (int)
   - `status`: Current status ("big" or "small")
   - `iteration`: Current iteration counter (int)
   - `max_iterations`: Maximum number of iterations allowed (int)
   - `result`: Final result message (string)

2. **Initial Routing Function**:
   - **`decide_next`**:
     - Examines the input value
     - Returns "big" if value > 10
     - Returns "small" if value ≤ 10
     - Determines which path the workflow takes initially

3. **Processing Nodes**:
   - **`big_node`**: 
     - Sets result to "Value is big"
     - Direct path to END (no looping)
   
   - **`small_node`**:
     - Sets result to "Value is small"
     - Continues to pass_through node (enters loop)
   
   - **`pass_through`**:
     - Increments the iteration counter
     - Tracks how many times the loop has executed
     - Continues to loop check

4. **Loop Control Function**:
   - **`check_iteration`**:
     - Compares current iteration vs max_iterations
     - Returns routing decision:
       - `"continue_small"` if iteration < max_iterations (loop again)
       - `"end"` if iteration >= max_iterations (exit loop)

5. **Workflow Graph**:
   ```
   START → decide_next
             ↓       ↓
           big    small
            ↓        ↓
           END   pass_through
                     ↓
               check_iteration
                 ↓         ↓
              small       END
              (loop)    (exit)
   ```
   - Initial conditional routing from START
   - Big path: direct to END
   - Small path: enters iteration loop
   - Loop continues until max_iterations reached

6. **Execution Example**:
   - Input: value=5 (≤10), max_iterations=3
   - Path taken: START → small → pass_through → check_iteration
   - Loop iterations:
     - Iteration 1: small → pass_through (iteration=1) → check_iteration → continue_small
     - Iteration 2: small → pass_through (iteration=2) → check_iteration → continue_small
     - Iteration 3: small → pass_through (iteration=3) → check_iteration → end
   - Final output: "Value is small", iterations=3

7. **Visualization**:
   - Shows branching from START with two paths
   - Demonstrates loop structure with conditional exit
   - pass_through node feeds back to small node

## Key Concepts:

### Path Mapping:
```python
graph.add_conditional_edges(START, decide_next, {"big": "big", "small": "small"})
```
- Explicitly maps return values to node names
- `decide_next` returns "big" or "small"
- Dictionary maps these strings to corresponding nodes
- More explicit than relying on node name matching alone

### Conditional Looping:
```python
graph.add_conditional_edges("pass_through", check_iteration, {"continue_small": "small", "end": END})
```
- Creates a loop by routing back to earlier node
- Loop condition: `iteration < max_iterations`
- Loop body: small → pass_through
- Loop exit: routes to END when max iterations reached

### Iteration Counter Pattern:
```python
def pass_through(state: ConditionState):
    iteration = state['iteration'] + 1
    return {"iteration": iteration}
```
- Maintains loop counter in state
- Increments on each iteration
- Prevents infinite loops
- Enables controlled repetition

### Multiple Conditional Edges:
- **First conditional edge** (from START): Routes based on value
- **Second conditional edge** (from pass_through): Routes based on iteration count
- Each conditional edge serves different purpose in workflow

### Literal Type for Type Safety:
```python
def check_iteration(state: ConditionState) -> Literal["continue_small", "end"]:
```
- Return type constrains possible routing targets
- Ensures only valid routing decisions
- Catches routing errors at type-check time

## Workflow Patterns Demonstrated:

1. **Branching**: Different paths based on initial conditions
2. **Looping**: Controlled repetition with exit condition
3. **State Evolution**: Iteration counter tracks progress
4. **Path Mapping**: Explicit routing configuration
5. **Multiple Conditionals**: Different routing logic at different points

## Use Cases:

### Retry Logic:
- Attempt operation multiple times before failing
- Track retry count in iteration counter
- Exit after max retries

### Batch Processing:
- Process items in batches
- Loop until all batches processed
- Track progress with iteration counter

### Gradual Refinement:
- Iteratively improve a result
- Check quality after each iteration
- Continue until quality threshold or max iterations

### Polling Pattern:
- Check status repeatedly
- Wait between checks (in real implementation)
- Exit when condition met or timeout

### Progressive Disclosure:
- Reveal information step by step
- User advances through iterations
- Track current step with counter

## Example Scenarios:

**Scenario 1: Big Value (No Loop)**
- Input: value=15
- Path: START → decide_next → big → END
- Iterations: 0
- Result: "Value is big"

**Scenario 2: Small Value (Loop 3 Times)**
- Input: value=5, max_iterations=3
- Path: START → decide_next → small → loop 3x → END
- Iterations: 3
- Result: "Value is small"

**Scenario 3: Small Value (Loop 5 Times)**
- Input: value=8, max_iterations=5
- Path: START → decide_next → small → loop 5x → END
- Iterations: 5
- Result: "Value is small"

## Advanced Features:

### Controlled Loops:
- Unlike infinite loops, this has explicit exit condition
- Prevents runaway execution
- Guarantees termination

### State-Based Routing:
- Routing decisions based on state values
- Different parts of state influence different routing decisions
- `value` influences initial routing
- `iteration` influences loop continuation

### Path Map Flexibility:
- Can map to node names or special targets like END
- Clear declaration of routing possibilities
- Easy to modify routing behavior

## Important Notes:

1. **Iteration Counter Must Be Initialized**: Start at 0 to count correctly
2. **Path Map Keys Must Match Return Values**: String returned by router must match dictionary keys
3. **Loop Prevention**: Always have exit condition to prevent infinite loops
4. **State Accumulation**: Each iteration can accumulate state changes
5. **END is a Special Target**: Can be used directly in path mapping

## Requirements:
- Understanding of conditional edges with path mapping
- Literal types for routing decisions
- Loop control patterns
- State management across iterations

## Comparison with Other Patterns:

**vs. Simple Conditional Routing**:
- Adds explicit path mapping
- Enables looping behavior
- More complex state management

**vs. Infinite Loops**:
- Has built-in termination condition
- Safer and more predictable
- Suitable for production use

**vs. Recursive Patterns**:
- Uses iteration counter instead of recursion
- Easier to understand and debug
- Better for bounded repetition
