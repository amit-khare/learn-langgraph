# Review Reply Workflow

## What the code does:

This demonstrates **conditional workflow with sentiment analysis and structured LLM outputs** - where customer reviews are analyzed for sentiment, and different response strategies are applied based on whether the review is positive or negative.

## Workflow Structure:

1. **Structured Output Schemas**: Uses Pydantic to enforce LLM response formats:
   
   **`SentimentSchema`**:
   - `sentiment`: Either "positive" or "negative" (Literal type)
   - Ensures binary classification of review sentiment
   
   **`DiagnosisSchema`** (for negative reviews only):
   - `issue_type`: Category of the problem ("UX", "Performance", "Bug", "Support", "Other")
   - `tone`: Emotional state ("angry", "frustrated", "disappointed", "calm")
   - `urgency`: Priority level ("low", "medium", "high")
   - Provides detailed analysis for proper response crafting

2. **State Definition** (`ReviewState`): Manages the review response workflow:
   - `review`: The customer review text (string)
   - `sentiment`: Detected sentiment ("positive" or "negative")
   - `diagnosis`: Detailed analysis for negative reviews (dict)
   - `response`: Generated reply message (string)

3. **Sentiment Analysis Node**:
   - **`find_sentiment`**:
     - Analyzes the review to determine if it's positive or negative
     - Uses structured output to ensure consistent "positive"/"negative" classification
     - Returns the sentiment for conditional branching

4. **Conditional Router**:
   - **`check_sentiment`**:
     - Examines the detected sentiment
     - Routes to different paths:
       - `"positive_response"` if sentiment is positive
       - `"run_diagnosis"` if sentiment is negative

5. **Positive Path** (for happy customers):
   - **`positive_response`**:
     - Generates warm thank-you message
     - Acknowledges the positive feedback
     - Asks user to leave feedback on website
     - Directly goes to END

6. **Negative Path** (for unhappy customers):
   - **`run_diagnosis`**:
     - Deep analysis of the negative review
     - Extracts issue type, emotional tone, and urgency
     - Stores structured diagnosis data
     - Continues to response generation
   
   - **`negative_response`**:
     - Uses diagnosis information to craft empathetic response
     - Tailors message based on issue type, tone, and urgency
     - Provides helpful resolution message
     - Then goes to END

7. **Workflow Graph**:
   ```
   START → Find Sentiment
              ↓
        Check Sentiment
         ↙         ↘
   Positive      Negative
   Response      ↓
      ↓        Run Diagnosis
      ↓            ↓
      ↓      Negative Response
      ↓            ↓
      └────→ END ←┘
   ```
   - Single entry point analyzing sentiment
   - Conditional branching based on sentiment
   - Positive path: 1 step (quick acknowledgment)
   - Negative path: 2 steps (diagnosis + tailored response)

8. **Execution Example**:
   
   **Input Review**: "The app crashes every time I try to upload a photo. This is so frustrating!"
   
   **Processing**:
   - Sentiment detected: "negative"
   - Branch taken: run_diagnosis
   - Diagnosis results:
     - issue_type: "Bug"
     - tone: "frustrated"
     - urgency: "high"
   - Generated empathetic response addressing the bug with appropriate urgency

9. **Visualization**:
   - Shows branching logic with two distinct paths
   - Demonstrates how different customer experiences get different handling

## Key Points:

### Structured Output Models:
```python
sentiment_model = model.with_structured_output(SentimentSchema)
diagnosis_model = model.with_structured_output(DiagnosisSchema)
```
- Multiple specialized models for different tasks
- Each model enforces specific output structure
- Ensures predictable, parseable responses from LLM
- Uses Literal types for constrained choices

### Conditional Branching:
```python
def check_sentiment(state: ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    if state['sentiment'] == 'positive':
        return 'positive_response'
    else:
        return 'run_diagnosis'
```
- Routes workflow based on sentiment analysis
- Different customer experiences for positive vs negative reviews
- Type-safe routing with Literal type hints

### Sequential Processing in Negative Path:
```python
graph.add_edge('run_diagnosis', 'negative_response')
```
- Negative reviews go through two-step process
- First: diagnose the issue deeply
- Second: craft response using diagnosis
- More sophisticated handling for critical situations

### Asymmetric Workflow Paths:
- **Positive path**: Fast and simple (1 node)
- **Negative path**: Thorough and detailed (2 nodes)
- Reflects real-world customer service priorities
- More effort on problems, quick thanks for praise

### Context-Aware Response Generation:
```python
prompt = f"""You are a support assistant.
The user had a '{diagnosis['issue_type']}' issue, sounded '{diagnosis['tone']}', and marked urgency as '{diagnosis['urgency']}'.
Write an empathetic, helpful resolution message.
"""
```
- Uses structured diagnosis data to inform response
- Adjusts tone and urgency based on analysis
- Personalized support based on issue characteristics

## Use Cases:
- Customer review response automation
- Support ticket triage and routing
- Sentiment-based email routing
- Multi-tier customer service workflows
- Escalation systems based on urgency
- Review platform management
- Social media comment handling

## Real-World Applications:

### E-commerce Platform:
- Positive reviews: Thank customer, ask for website review
- Negative reviews: Diagnose issue, offer refund/replacement based on severity

### SaaS Product:
- Positive feedback: Request case study participation
- Negative feedback: Route to technical support with issue classification

### Mobile App:
- Happy users: Prompt for app store rating
- Frustrated users: Fast-track to dev team with bug details

## Example Scenarios:

**Scenario 1: Positive Review**
- Input: "Love this app! Best UI I've ever used."
- Path: find_sentiment → positive_response → END
- Output: Warm thank-you + website feedback request

**Scenario 2: Negative Review (Bug)**
- Input: "App crashes constantly. Can't do anything!"
- Path: find_sentiment → run_diagnosis → negative_response → END
- Diagnosis: Bug, angry tone, high urgency
- Output: Immediate apology + technical support escalation

**Scenario 3: Negative Review (Performance)**
- Input: "The app is quite slow on my device."
- Path: find_sentiment → run_diagnosis → negative_response → END
- Diagnosis: Performance, calm tone, medium urgency
- Output: Optimization tips + future update info

## Requirements:
- `OPENAI_API_KEY` environment variable
- Pydantic for schema validation
- Understanding of structured outputs
- Customer service domain knowledge

## Advanced Patterns Demonstrated:
1. **Multiple structured output models** for different purposes
2. **Asymmetric branching** with different path complexities
3. **Chained analysis** where one LLM call informs the next
4. **Context propagation** through state management
5. **Type-safe routing** with Literal type hints
6. **Domain-specific classification** (issue types, tones, urgency levels)
