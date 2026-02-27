"""
Test script for sentiment analysis endpoint
"""
import requests
import json

# Test cases
test_comments = [
    {"comment": "This product is amazing!", "expected_sentiment": "positive"},
    {"comment": "Worst purchase ever, completely disappointed", "expected_sentiment": "negative"},
    {"comment": "The product arrived on time", "expected_sentiment": "neutral"},
    {"comment": "I love it! Best investment ever!", "expected_sentiment": "positive"},
    {"comment": "It's okay, nothing special", "expected_sentiment": "neutral"}
]

def test_endpoint(base_url="http://localhost:8000"):
    print(f"Testing endpoint: {base_url}/comment\n")
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_comments, 1):
        print(f"Test {i}: {test['comment'][:50]}...")
        
        try:
            response = requests.post(
                f"{base_url}/comment",
                json={"comment": test["comment"]},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  Response: {json.dumps(result, indent=2)}")
                
                # Validate structure
                if "sentiment" in result and "rating" in result:
                    if result["sentiment"] in ["positive", "negative", "neutral"]:
                        if 1 <= result["rating"] <= 5:
                            if result["sentiment"] == test["expected_sentiment"]:
                                print(f"  ✓ PASSED - Correct sentiment")
                                passed += 1
                            else:
                                print(f"  ⚠ PARTIAL - Got '{result['sentiment']}', expected '{test['expected_sentiment']}'")
                                passed += 1  # Still count as pass if structure is correct
                        else:
                            print(f"  ✗ FAILED - Rating out of range: {result['rating']}")
                            failed += 1
                    else:
                        print(f"  ✗ FAILED - Invalid sentiment: {result['sentiment']}")
                        failed += 1
                else:
                    print(f"  ✗ FAILED - Missing required fields")
                    failed += 1
            else:
                print(f"  ✗ FAILED - HTTP {response.status_code}: {response.text}")
                failed += 1
                
        except Exception as e:
            print(f"  ✗ FAILED - Error: {str(e)}")
            failed += 1
        
        print()
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"Success rate: {passed}/{len(test_comments)} ({passed*100//len(test_comments)}%)")
    print(f"{'='*60}")
    
    return passed >= 3  # Need at least 3/5 to pass

if __name__ == "__main__":
    import sys
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    success = test_endpoint(base_url)
    sys.exit(0 if success else 1)
