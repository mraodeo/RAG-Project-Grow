import sys
import os
# Add project root to python path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.pipeline import process_query

st.set_page_config(page_title="MF FAQ Assistant", page_icon="🏦", layout="centered")

# Inject custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.warning("⚠️ Facts-only. No investment advice.")
st.title("🏦 Mutual Fund FAQ Assistant")
st.markdown("Welcome! Ask me any factual question about HDFC mutual fund schemes.")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Example questions as buttons
st.markdown("### Try these examples:")
examples = [
    "What is the expense ratio of HDFC Large Cap Fund?",
    "What is the exit load for HDFC ELSS Tax Saver Fund?",
    "Minimum SIP amount for HDFC Small Cap Fund?",
]

# Create columns for buttons
cols = st.columns(len(examples))
for i, q in enumerate(examples):
    with cols[i]:
        if st.button(q):
            st.session_state.pending_query = q

# Chat history display
st.markdown("---")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask a question about HDFC mutual fund schemes...")
query = user_input or st.session_state.pop("pending_query", None)

if query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Process and display response
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            response = process_query(query)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
