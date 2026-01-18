# Quadratic Equation Workflow

## What the code does:

This demonstrates **conditional branching** - where the workflow takes different paths based on the discriminant value of a quadratic equation.

### Mathematical Background:
For a quadratic equation: **ax² + bx + c = 0**
- **Discriminant (Δ)** = b² - 4ac
- If Δ > 0: Two distinct real roots
- If Δ = 0: One repeated root
- If Δ < 0: No real roots (complex roots)

## Workflow Structure:

1. **State Definition** (`QuadraticState`): Defines the workflow's data structure:
   - `a`: Coefficient of x² (int)
   - `b`: Coefficient of x (int)
   - `c`: Constant term (int)
   - `equation`: Formatted equation string
   - `discriminant`: Calculated discriminant value (float)
   - `result`: Final result message (string)

2. **Sequential Processing Nodes**:
   - **`show_equation`**: 
     - Formats the equation as "ax² + bx + c = 0"
     - Returns the formatted equation string
   
   - **`calculate_discriminant`**:
     - Calculates: b² - 4ac
     - Returns the discriminant value
     - This value determines which branch to take

3. **Conditional Branching Function**:
   - **`check_condition`**:
     - Examines the discriminant value
     - Returns one of three possible paths:
       - `"real_roots"` if discriminant > 0
       - `"repeated_roots"` if discriminant = 0
       - `"no_real_roots"` if discriminant < 0

4. **Conditional Path Nodes** (only one executes):
   - **`real_roots`**: 
     - Calculates two distinct roots using quadratic formula
     - Formula: x = (-b ± √Δ) / 2a
     - Returns both roots
   
   - **`repeated_roots`**:
     - Calculates the single repeated root
     - Formula: x = -b / 2a
     - Returns the repeated root
   
   - **`no_real_roots`**:
     - Returns message indicating no real roots exist
     - (Complex roots would require imaginary numbers)

5. **Workflow Graph**:
   ```
   START → Show Equation → Calculate Discriminant
                                    ↓
                        ┌───────────┼───────────┐
                        ↓           ↓           ↓
                  Real Roots  Repeated   No Real
                    (Δ>0)     Roots      Roots
                              (Δ=0)      (Δ<0)
                        ↓           ↓           ↓
                        └───────────┼───────────┘
                                    ↓
                                   END
   ```
   - Sequential processing until discriminant calculation
   - Conditional branching based on discriminant value
   - All paths converge to END

6. **Execution Example**:
   - Input: a=1, b=3, c=2 (equation: 1x² + 3x + 2 = 0)
   - Discriminant: 3² - 4(1)(2) = 9 - 8 = 1 (positive)
   - Branch taken: `real_roots`
   - Output: The roots are -1.0 and -2.0

7. **Visualization**:
   - Shows conditional branching pattern
   - Three possible paths from calculate_discriminant
   - Only one path executes per invocation

## Key Points:

### Conditional Edges:
```python
graph.add_conditional_edges('calculate_discriminant', check_condition)
```
- Creates dynamic routing based on function return value
- `check_condition` returns a string matching one of the node names
- LangGraph automatically routes to the corresponding node
- Type hint `Literal["real_roots", "repeated_roots", "no_real_roots"]` ensures valid routing

### Multiple Exit Points:
```python
graph.add_edge('real_roots', END)
graph.add_edge('repeated_roots', END)
graph.add_edge('no_real_roots', END)
```
- All three conditional branches lead to END
- Only one branch executes per workflow invocation
- Ensures workflow always completes regardless of path taken

### Partial State Returns:
- Each node returns only the fields it modifies
- Preserves state across the workflow
- Earlier nodes (equation, discriminant) remain accessible in later nodes

## Use Cases:
- Decision trees and classification logic
- Mathematical computation with different cases
- Rule-based routing (routing queries, data validation)
- Workflow branching based on computed values
- Error handling with different recovery paths

## Mathematical Example Results:

**Case 1: Two Real Roots (Δ > 0)**
- Input: a=1, b=3, c=2
- Discriminant: 1
- Output: Roots are -1.0 and -2.0

**Case 2: Repeated Root (Δ = 0)**
- Input: a=1, b=2, c=1
- Discriminant: 0
- Output: Only repeating root is -1.0

**Case 3: No Real Roots (Δ < 0)**
- Input: a=1, b=2, c=5
- Discriminant: -16
- Output: No real roots

## Requirements:
- Understanding of conditional edges in LangGraph
- `Literal` type hints for type safety
- Basic quadratic equation mathematics
