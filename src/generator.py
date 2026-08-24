from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from src import config

# Define the strict system prompt
SYSTEM_PROMPT = """You are a facts-only mutual fund FAQ assistant.

STRICT RULES:
1. Answer ONLY using the provided context. Do NOT use any outside knowledge.
2. Keep your response to a MAXIMUM of 3 sentences.
3. If the context does not contain the answer, respond exactly with:
   "I don't have this information in my current sources."
4. NEVER provide investment advice, opinions, or recommendations.
5. NEVER compare fund performance or calculate returns.
6. Do NOT include any source links or date footers in your answer.

CONTEXT:
{context}

USER QUESTION:
{question}
"""

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=SYSTEM_PROMPT
)

def generate_answer(query: str, retrieved_docs: list[dict]) -> str:
    """
    Generates an answer using the Groq API and the retrieved context.
    """
    if not retrieved_docs:
        return "I don't have this information in my current sources."

    # Combine the content of all retrieved chunks
    # We include the scheme name from metadata for explicit context in the prompt
    context_parts = []
    for doc in retrieved_docs:
        scheme_name = doc["metadata"].get("scheme_name", "Unknown Scheme")
        context_parts.append(f"[Source: {scheme_name}]\n{doc['content']}")
        
    context_str = "\n\n---\n\n".join(context_parts)
    
    # Initialize the LLM
    try:
        llm = ChatGroq(
            model=config.GROQ_GENERATION_MODEL,
            api_key=config.GROQ_API_KEY,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.LLM_MAX_TOKENS,
        )
    except Exception as e:
        print(f"Error initializing ChatGroq: {e}")
        return "System error: Unable to connect to language model."

    # Format the prompt
    prompt_val = prompt_template.format(context=context_str, question=query)
    
    # Generate the response
    try:
        response = llm.invoke(prompt_val)
        return response.content.strip()
    except Exception as e:
        print(f"Error generating answer from Groq: {e}")
        return "System error: Failed to generate response."

if __name__ == "__main__":
    # Quick test
    test_docs = [{
        "content": "The HDFC Mid Cap Fund Direct Growth has an expense ratio of 0.75%.",
        "metadata": {"scheme_name": "HDFC Mid Cap Fund Direct Growth"}
    }]
    print(generate_answer("What is the expense ratio?", test_docs))
