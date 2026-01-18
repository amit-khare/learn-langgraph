
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import operator

load_dotenv()

# Define a schema for structured output
class FeedbackSchema(BaseModel):
    feedback : str = Field(description="detailed feedback on the essay")
    score: int = Field(description="score out of 10 for the essay", ge=0, le=10)

model = ChatOpenAI(model='gpt-4o-mini')

        
structure_model = model.with_structured_output(FeedbackSchema)


# Define states for parallel tasks
class EssayEvalution(TypedDict):
    eassy: str
    clarity_of_thought_feedback: str
    deptpth_of_analysis_feedback: str
    language_feedback: str
    individual_scores: Annotated[list[int], operator.add]
    avg_score: float
    final_feedback: str

def evaluate_clarity_of_thought(state: EssayEvalution) -> EssayEvalution:
    essay = state["eassy"]
    
    prompt = f"Provide detailed feedback on the clarity of thought in the following essay:\n\n{essay}\n\nYour response should be structured as JSON with 'feedback' and 'score' (out of 10)."
    response = structure_model.invoke(prompt)
    
    return {"clarity_of_thought_feedback": response.feedback, "individual_scores": [response.score]}

def evaluate_depth_of_analysis(state: EssayEvalution) -> EssayEvalution:
    essay = state["eassy"]
    
    prompt = f"Provide detailed feedback on the depth of analysis in the following essay:\n\n{essay}\n\nYour response should be structured as JSON with 'feedback' and 'score' (out of 10)."
    response = structure_model.invoke(prompt)
    
    return {"deptpth_of_analysis_feedback": response.feedback, "individual_scores": [response.score]}

def evaluate_language(state: EssayEvalution) -> EssayEvalution:
    essay = state["eassy"]

    prompt = f"Provide detailed feedback on the language used in the following essay:\n\n{essay}\n\nYour response should be structured as JSON with 'feedback' and 'score' (out of 10)."    
    response = structure_model.invoke(prompt)

    return {"language_feedback": response.feedback, "individual_scores": [response.score]  }

def finalize_evaluation(state: EssayEvalution):
    prompt = f"""Based on the following individual feedbacks and scores, provide a comprehensive final feedback summary for the essay.
    \nClarity of Thought Feedback: {state['clarity_of_thought_feedback']}
    \nDepth of Analysis Feedback: {state['deptpth_of_analysis_feedback']}
    \nLanguage Feedback: {state['language_feedback']}
    \nIndividual Scores: {state['individual_scores']}
    \nYour final feedback should include an overall average score out of 10 and a summary of strengths and areas for improvement."""    
    response = structure_model.invoke(prompt)
    return {"final_feedback": response.feedback, "avg_score": response.score}
   

# Define the workflow graph
graph = StateGraph(EssayEvalution)

# Add nodes to your graph
graph.add_node("Evaluate Clarity of Thought", evaluate_clarity_of_thought)
graph.add_node("Evaluate Depth of Analysis", evaluate_depth_of_analysis)
graph.add_node("Evaluate Language", evaluate_language)
graph.add_node("Finalize Evaluation", finalize_evaluation)

# add edges to your graph
graph.add_edge(START, "Evaluate Clarity of Thought")
graph.add_edge(START, "Evaluate Depth of Analysis")
graph.add_edge(START, "Evaluate Language")

graph.add_edge("Evaluate Clarity of Thought", "Finalize Evaluation")
graph.add_edge("Evaluate Depth of Analysis", "Finalize Evaluation")
graph.add_edge("Evaluate Language", "Finalize Evaluation")

graph.add_edge("Finalize Evaluation", END)

# compile the graph
workflow   = graph.compile()

# execute the workflow with sample data
essay = """A piece is a part of something big. When you break a chocolet, you get many pieces. Each piece may be small but it is still important. If one piece is missing, then the chocolet is not full. I like pieces because I can share them with my friends and family. 
In school, my teacher gives us a piece of paper to write on. That small piece helps me learn and do my homework. When we do puzzles, every piece has a special shape. If we lose one piece, the puzzle never gets finish. It makes me feel sad because the picture looks wrong.
My mom cuts pizza into pieces so everyone gets some. I like the biggest piece but my mom says sharing is good. When I give my sister a piece, she smiles and that makes me happy.
A piece can also be a piece of art or music. My brother plays a music piece on piano and it sounds nice. I think every piece matters, even if it is small. Small pieces make big things possible."""    


initial_state: EssayEvalution = {
        "eassy": essay       
    }


final_state = workflow.invoke(initial_state)

print("Essay Evaluation Results:")
print ("Individual Scores:", final_state['individual_scores'])
print(f"Average Score: {final_state['avg_score']}/10")
print("Final Feedback:")
print(final_state['final_feedback'])



# Visualize the workflow
try:    
    from IPython.display import Image, display
    display(Image(workflow.get_graph().draw_mermaid_png()))
except Exception:
    # If not in Jupyter, print ASCII representation
    print("\nWorkflow Graph:")
    print(workflow.get_graph().draw_ascii())    

