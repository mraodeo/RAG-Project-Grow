"""
Groq API connectivity verification script.
Run this after setting up your .env to confirm the API key works.

Usage:
    python scripts/verify_groq.py
"""

import sys
import os

# Add project root to path so we can import src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import GROQ_API_KEY, GROQ_GENERATION_MODEL, GROQ_GUARDRAIL_MODEL


def verify_groq():
    """Test Groq API connectivity with both models."""
    try:
        from groq import Groq
    except ImportError:
        print("❌ 'groq' package not installed. Run: pip install langchain-groq")
        return False

    if not GROQ_API_KEY or GROQ_API_KEY == "gsk_your_groq_api_key_here":
        print("❌ GROQ_API_KEY is not configured. Update your .env file.")
        return False

    client = Groq(api_key=GROQ_API_KEY)

    # Test 1: Generation model
    print(f"\n🔄 Testing generation model: {GROQ_GENERATION_MODEL}...")
    try:
        response = client.chat.completions.create(
            model=GROQ_GENERATION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Groq generation model is connected!' in one sentence.",
                }
            ],
            max_tokens=50,
            temperature=0,
        )
        print(f"✅ {GROQ_GENERATION_MODEL}: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ {GROQ_GENERATION_MODEL} failed: {e}")
        return False

    # Test 2: Guardrail model
    print(f"\n🔄 Testing guardrail model: {GROQ_GUARDRAIL_MODEL}...")
    try:
        response = client.chat.completions.create(
            model=GROQ_GUARDRAIL_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Groq guardrail model is connected!' in one sentence.",
                }
            ],
            max_tokens=50,
            temperature=0,
        )
        print(f"✅ {GROQ_GUARDRAIL_MODEL}: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ {GROQ_GUARDRAIL_MODEL} failed: {e}")
        return False

    print("\n🎉 All Groq models are connected and working!")
    return True


if __name__ == "__main__":
    success = verify_groq()
    sys.exit(0 if success else 1)
