from src import guardrail

TEST_CASES = [
    {
        "query": "What is the expense ratio of HDFC Mid-Cap Fund?",
        "expected": "FACTUAL"
    },
    {
        "query": "Exit load for HDFC ELSS Tax Saver",
        "expected": "FACTUAL"
    },
    {
        "query": "Should I invest in HDFC Small Cap Fund?",
        "expected": "ADVISORY"
    },
    {
        "query": "Which is better: HDFC Mid Cap or SBI Mid Cap?",
        "expected": "ADVISORY"
    },
    {
        "query": "Can you check my PAN ABCDE1234F for investment?",
        "expected": "PII_DETECTED"
    },
    {
        "query": "My phone number is 9876543210. How do I invest?",
        "expected": "PII_DETECTED"
    },
    {
        "query": "Who won the cricket match yesterday?",
        "expected": "OUT_OF_SCOPE"
    }
]

def run_tests():
    print("Running Guardrail Tests...\n")
    passed = 0
    
    for i, test in enumerate(TEST_CASES):
        query = test["query"]
        expected = test["expected"]
        
        result = guardrail.classify(query)
        
        if result == expected:
            print(f"✅ Test {i+1} PASSED")
            passed += 1
        else:
            print(f"❌ Test {i+1} FAILED")
            print(f"   Query: {query}")
            print(f"   Expected: {expected}, Got: {result}")
            
    print(f"\nResults: {passed}/{len(TEST_CASES)} passed.")

if __name__ == "__main__":
    run_tests()
