from src import retriever, generator, formatter, guardrail

def process_query(user_query: str) -> str:
    """
    Orchestrates the full query flow: guardrail → retriever → generator → formatter.
    """
    print(f"\n[Pipeline] Processing query: '{user_query}'")
    
    # Step 0: Guardrail
    print("[Pipeline] Running guardrail checks...")
    intent = guardrail.classify(user_query)
    
    if intent != "FACTUAL":
        print(f"[Pipeline] Guardrail triggered: {intent}")
        return guardrail.get_refusal_response(intent)
    
    # Step 1: Retrieve relevant chunks
    print("[Pipeline] Retrieving context...")
    results = retriever.retrieve(user_query)
    
    if not results:
        return "I don't have this information in my current sources."
        
    # Step 2: Generate answer via Groq
    print(f"[Pipeline] Generating answer using {len(results)} chunks...")
    raw_answer = generator.generate_answer(user_query, results)
    
    # Step 3: Format response with citation
    # We use the metadata of the top result for the primary citation
    top_metadata = results[0]["metadata"]
    formatted = formatter.format_response(raw_answer, top_metadata)
    
    return formatted

if __name__ == "__main__":
    # Test the full pipeline with guardrails
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Should I invest in the large cap fund?"
        
    answer = process_query(query)
    print("\n" + "="*50)
    print("FINAL ANSWER")
    print("="*50)
    print(answer)
