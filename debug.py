import os  
from src import guardrail  
from langchain_groq import ChatGroq  
from src import config  
llm = ChatGroq(model=config.GROQ_GUARDRAIL_MODEL, api_key=config.GROQ_API_KEY, temperature=0, max_tokens=20)  
print(repr(llm.invoke(guardrail.prompt_template.format(user_query='What is the expense ratio of HDFC Mid-Cap Fund?')).content))  
