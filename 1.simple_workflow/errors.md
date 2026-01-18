# Common LangGraph Errors and Solutions

## 1. InvalidUpdateError: Multiple Values Per Step

### Error Message:
```
langgraph.errors.InvalidUpdateError: At key 'runs': Can receive only one value per step. 
Use an Annotated key to handle multiple values.
For troubleshooting, visit: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE
```

### What Causes This?
This error occurs when multiple nodes in a **parallel workflow** try to update the **same state field** simultaneously. LangGraph doesn't know how to merge these concurrent updates.

### Example Problem:
```python
# Two nodes running in parallel both trying to update 'runs'
graph.add_edge(START, "Node A")  # Node A updates 'runs'
graph.add_edge(START, "Node B")  # Node B also updates 'runs'
```

### Solution: Use `Annotated` with a Reducer

You need to tell LangGraph **how to combine** multiple updates using the `Annotated` type with a reducer function.

**Import Required:**
```python
from typing import Annotated
from operator import add
```

**Fix the State Definition:**
```python
class MyState(TypedDict):
    # For fields updated by parallel nodes, use Annotated with a reducer
    runs: Annotated[int, add]  # Will add values together
    name: str  # Regular field (not updated concurrently)
```

### Common Reducer Functions:

1. **`add`** - Adds numbers together
   ```python
   from operator import add
   value: Annotated[int, add]
   ```

2. **Custom reducer** - For lists or custom logic
   ```python
   def merge_lists(existing, new):
       return existing + new
   
   items: Annotated[list, merge_lists]
   ```

3. **Replace (default)** - Overwrites with latest value
   ```python
   # No Annotated needed - this is default behavior
   name: str
   ```

### When Do You Need This?

✅ **Use `Annotated`** when:
- Multiple nodes run **in parallel**
- They update the **same field**
- You want to **combine** their results

❌ **Don't need `Annotated`** when:
- Nodes run **sequentially** (one after another)
- Each field is updated by **only one node**
- You want the **latest value** to replace the old one

### Complete Fixed Example:

```python
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

class BatsState(TypedDict):
    # Fields updated by parallel nodes need Annotated
    runs: Annotated[int, add]
    balls: Annotated[int, add]
    # Fields updated by only one node don't need it
    sr: float
    ballsperrun: float

def calculate_strike_rate(state: BatsState) -> BatsState:
    state["sr"] = round((state["runs"] / state["balls"]) * 100, 2)
    return state

def calculate_balls_per_run(state: BatsState) -> BatsState:
    state["ballsperrun"] = round(state["balls"] / state["runs"], 2)
    return state

graph = StateGraph(BatsState)
graph.add_node("Calculate Strike Rate", calculate_strike_rate)
graph.add_node("Calculate Balls Per Run", calculate_balls_per_run)

# Parallel edges from START
graph.add_edge(START, "Calculate Strike Rate")
graph.add_edge(START, "Calculate Balls Per Run")

# Both converge to END
graph.add_edge("Calculate Strike Rate", END)
graph.add_edge("Calculate Balls Per Run", END)

workflow = graph.compile()
```

### Key Takeaway:

> **In parallel workflows, use `Annotated[type, reducer]` for any state field that multiple nodes might update simultaneously.**
