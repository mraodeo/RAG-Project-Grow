from datetime import datetime


def format_response(raw_answer: str, metadata: dict) -> str:
    """
    Appends citations and footer to the raw LLM answer.
    """
    if not raw_answer or raw_answer.strip() == "I don't have this information in my current sources.":
        return raw_answer
        
    source_url = metadata.get("source_url", "Unknown Source")
    last_updated_str = metadata.get("last_updated", "Unknown Date")
    
    # Try to format the date nicely if it's an ISO string
    try:
        if last_updated_str and last_updated_str != "Unknown Date":
            dt = datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
            last_updated_str = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        pass # Keep original string if parsing fails
        
    formatted = f"{raw_answer.strip()}\n\n"
    formatted += f"Source: {source_url}\n"
    formatted += f"Last updated from sources: {last_updated_str}"
    
    return formatted
