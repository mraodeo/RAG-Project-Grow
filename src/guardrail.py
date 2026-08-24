import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from src import config

# ---------------------------------------------------------
# PII Regex Patterns
# ---------------------------------------------------------
PII_PATTERNS = [
    # PAN Card (e.g., ABCDE1234F)
    r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b',
    # Aadhaar (e.g., 1234 5678 9012 or 123456789012)
    r'\b[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\b',
    # Phone number (India specific +91 or just 10 digits starting with 6-9)
    r'\b(?:\+91[\s-]?)?[6-9][0-9]{9}\b',
    # Email
    r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
]

# Account numbers / OTPs need context so we'll do a simpler broad pass
OTP_ACCOUNT_PATTERNS = [
    r'\b(otp|verification code|account|folio)\s*[:#-]?\s*[0-9]{4,18}\b'
]

# ---------------------------------------------------------
# Intent Classification Setup
# ---------------------------------------------------------
GUARDRAIL_PROMPT = """
You are an intent classification engine. Classify the user query into exactly one of the three categories below.
Respond with ONLY the category name. Do not explain.

Categories:
1. FACTUAL: Questions asking for specific facts about mutual funds (e.g. expense ratio, NAV, AUM, exit load, fund manager, riskometer).
2. ADVISORY: Questions asking for investment advice, opinions, recommendations, "should I invest", predictions, or comparing funds.
3. OUT_OF_SCOPE: General knowledge, greetings, or questions completely unrelated to mutual funds.

Examples:
Query: "What is the NAV of HDFC Mid Cap?" -> FACTUAL
Query: "Should I put my money in the Small Cap fund?" -> ADVISORY
Query: "Which fund will give me better returns?" -> ADVISORY
Query: "Who won the game?" -> OUT_OF_SCOPE
Query: "Hi there" -> OUT_OF_SCOPE

Query: "{user_query}" ->
"""

prompt_template = PromptTemplate(
    input_variables=["user_query"],
    template=GUARDRAIL_PROMPT
)

# ---------------------------------------------------------
# Refusal Templates
# ---------------------------------------------------------
REFUSAL_RESPONSES = {
    "ADVISORY": (
        "I can only provide factual information about mutual fund schemes. "
        "I'm unable to offer investment advice or recommendations.\n\n"
        "For investment guidance, please consult a SEBI-registered advisor or visit:\n"
        "https://www.amfiindia.com/investor-corner/knowledge-center.html"
    ),
    "PII_DETECTED": (
        "For your safety, I cannot process queries containing personal information "
        "such as PAN, Aadhaar, phone numbers, or account details.\n\n"
        "Please rephrase your question with only scheme-related details."
    ),
    "OUT_OF_SCOPE": (
        "I can only answer questions about mutual fund schemes covered in my knowledge base. "
        "Please try asking about one of the supported schemes:\n"
        "• HDFC Mid-Cap Fund\n• HDFC Small Cap Fund\n• HDFC Gold ETF FoF\n"
        "• HDFC Large Cap Fund\n• HDFC ELSS Tax Saver Fund"
    ),
}

def contains_pii(query: str) -> bool:
    """Returns True if the query contains PII patterns."""
    text_to_check = query.upper()
    for pattern in PII_PATTERNS + OTP_ACCOUNT_PATTERNS:
        if re.search(pattern, text_to_check, re.IGNORECASE):
            return True
    return False

def classify(query: str) -> str:
    """
    Classifies the user query.
    Returns: "FACTUAL", "ADVISORY", "OUT_OF_SCOPE", or "PII_DETECTED".
    """
    if contains_pii(query):
        return "PII_DETECTED"
        
    try:
        llm = ChatGroq(
            model=config.GROQ_GUARDRAIL_MODEL,
            api_key=config.GROQ_API_KEY,
            temperature=0,
            max_tokens=1024,
        )
        prompt_val = prompt_template.format(user_query=query)
        response = llm.invoke(prompt_val)
        
        # Remove <think>...</think> blocks if present
        content = response.content.strip()
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
        
        category = content.strip().upper()
        
        # Ensure the output is exactly one of our allowed categories
        for allowed in ["FACTUAL", "ADVISORY", "OUT_OF_SCOPE"]:
            if allowed in category:
                return allowed
                
        # Default fallback
        return "OUT_OF_SCOPE"
    except Exception as e:
        print(f"Error in guardrail classifier: {e}")
        # Fail safe
        return "FACTUAL"

def get_refusal_response(intent: str) -> str:
    """Returns the canned refusal response for a given intent."""
    return REFUSAL_RESPONSES.get(intent, "I cannot process this request.")
