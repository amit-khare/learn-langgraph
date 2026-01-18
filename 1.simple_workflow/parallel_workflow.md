# Parallel Workflow

## What the code does:

This demonstrates **parallel execution** - where multiple nodes run simultaneously and independently.

1. **State Definition** (`BatsState`): Defines the workflow's data structure for cricket batting statistics:
   - `runs`: Total runs scored (int)
   - `balls`: Total balls faced (int)
   - `fours`: Number of 4-run boundaries (int)
   - `sixes`: Number of 6-run boundaries (int)
   - `sr`: Strike rate (float) - calculated field
   - `ballsperrun`: Balls per run (float) - calculated field
   - `bountrate`: Boundary rate (float) - calculated field

2. **Node Functions** (all run in parallel):
   - **`calculate_strike_rate`**: 
     - Calculates: (runs / balls) × 100
     - Returns only the `sr` field to avoid conflicts
   
   - **`calculate_balls_per_run`**:
     - Calculates: balls / runs
     - Returns only the `ballsperrun` field to avoid conflicts
   
   - **`calculate_bountrate`**:
     - Calculates: ((fours + sixes) / balls) × 100
     - Returns only the `bountrate` field to avoid conflicts

3. **Workflow Graph**:
   ```
   START → Calculate Strike Rate → END
       ↘ Calculate Balls Per Run ↗
       ↘ Calculate Bounce Rate ↗
   ```
   - Three nodes execute in parallel from START
   - All converge to END when complete
   - No dependencies between calculations

4. **Execution**:
   - Initializes state with sample data (150 runs, 120 balls, 10 fours, 5 sixes)
   - All three calculations run simultaneously
   - Outputs:
     - Strike Rate: 125.0
     - Balls Per Run: 0.8
     - Boundary Rate: 12.5

5. **Visualization**:
   - Displays ASCII representation showing parallel execution paths
   - Three branches from START converging to END

## Key Points:
- Demonstrates **parallel execution** where multiple nodes run simultaneously
- Each node returns **only the fields it modifies** to avoid update conflicts
- All nodes read from the same initial state independently
- LangGraph automatically waits for all parallel nodes to complete before moving to END
- Much faster than sequential execution when calculations are independent
- Pattern: `return {"field": value}` instead of `return state` to avoid conflicts
- Useful when tasks don't depend on each other's results

## Important Pattern:
**Partial State Returns** - Each node returns only what it modifies:
```python
def calculate_strike_rate(state: BatsState) -> BatsState:
    sr = (state["runs"] / state["balls"]) * 100
    return {"sr": round(sr, 2)}  # Only return what changed
```

This prevents the `InvalidUpdateError` when multiple nodes run in parallel.
