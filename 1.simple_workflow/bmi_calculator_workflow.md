# BMI Calculator Workflow

## What the code does:

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

## Key Points:
- Demonstrates basic LangGraph state management
- Single-node workflow for mathematical calculation
- Includes workflow visualization using `draw_ascii()`
- Requires `grandalf` package for graph visualization
