# 🔄 System Architecture & Flow

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client                              │
│                 (Browser, curl, test script)                │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTP POST /comment
                             │ {"comment": "This is amazing!"}
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Railway/Render                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              FastAPI Application                      │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Request Validation (Pydantic)                  │  │  │
│  │  │  - Checks comment is non-empty                  │  │  │
│  │  │  - Validates JSON structure                     │  │  │
│  │  └─────────────────────┬───────────────────────────┘  │  │
│  │                        │                              │  │
│  │                        ▼                              │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  OpenAI API Call                                │  │  │
│  │  │  - Model: gpt-4o-mini                           │  │  │
│  │  │  - Structured Output Schema                     │  │  │
│  │  │  - Strict validation: true                      │  │  │
│  │  └─────────────────────┬───────────────────────────┘  │  │
│  │                        │                              │  │
│  │                        ▼                              │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Response Formatting (JSONResponse)             │  │  │
│  │  │  - Content-Type: application/json               │  │  │
│  │  │  - Schema-validated output                      │  │  │
│  │  └─────────────────────┬───────────────────────────┘  │  │
│  └────────────────────────┼───────────────────────────────┘  │
└────────────────────────────┼──────────────────────────────────┘
                             │
                             │ {"sentiment": "positive", "rating": 5}
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                         Client                              │
│                  (Receives JSON response)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Request Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. Client sends POST request                                       │
│     POST /comment                                                   │
│     Headers: Content-Type: application/json                        │
│     Body: {"comment": "This product is amazing!"}                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. FastAPI receives request                                        │
│     - Route: @app.post("/comment")                                  │
│     - Handler: analyze_comment()                                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. Pydantic validates input                                        │
│     - CommentIn model                                               │
│     - Checks: comment is string, non-empty                          │
│     - Result: ✓ Valid or ✗ 400 Bad Request                         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. Get OpenAI client                                               │
│     - Loads OPENAI_API_KEY from environment                         │
│     - Creates OpenAI client                                         │
│     - Check: ✓ Key exists or ✗ 500 Server Error                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  5. Call OpenAI API                                                 │
│     Model: gpt-4o-mini                                              │
│     Messages:                                                       │
│       - System: "You are a sentiment analyzer..."                   │
│       - User: "Comment: This product is amazing!"                   │
│     Response Format: STRUCTURED_SCHEMA                              │
│       {                                                             │
│         "type": "json_schema",                                      │
│         "json_schema": {                                            │
│           "strict": True,                                           │
│           "schema": {                                               │
│             "sentiment": enum["positive","negative","neutral"],     │
│             "rating": integer(1-5)                                  │
│           }                                                         │
│         }                                                           │
│       }                                                             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  6. OpenAI processes with constrained decoding                      │
│     - Analyzes sentiment from comment                               │
│     - Generates tokens only valid per schema                        │
│     - Validates output against schema                               │
│     - Returns: {"sentiment": "positive", "rating": 5}               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  7. Parse and validate response                                     │
│     - json.loads() - Parse JSON string                              │
│     - SentimentOut(**data) - Validate with Pydantic                 │
│     - Check: ✓ Valid or ✗ 502 Bad Gateway                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  8. Return JSON response                                            │
│     Status: 200 OK                                                  │
│     Headers: Content-Type: application/json                        │
│     Body: {"sentiment": "positive", "rating": 5}                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
│                                                              │
│  ┌────────────────┐      ┌────────────────────────────────┐ │
│  │  CommentIn     │─────▶│  analyze_comment()             │ │
│  │  (Pydantic)    │      │                                │ │
│  │                │      │  1. Validate input             │ │
│  │  - comment: str│      │  2. Get OpenAI client          │ │
│  │  - min_length=1│      │  3. Call API with schema       │ │
│  └────────────────┘      │  4. Parse response             │ │
│                          │  5. Return JSON                │ │
│                          └─────────┬──────────────────────┘ │
│                                    │                        │
│  ┌────────────────┐                │                        │
│  │  SentimentOut  │◀───────────────┘                        │
│  │  (Pydantic)    │                                         │
│  │                │                                         │
│  │  - sentiment:  │                                         │
│  │    Literal[...]│                                         │
│  │  - rating:     │                                         │
│  │    int (1-5)   │                                         │
│  └────────────────┘                                         │
└──────────────────────────────────────────────────────────────┘
                             │
                             │ API Call
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                      OpenAI API                              │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  GPT-4o-mini Model                                     │ │
│  │                                                        │ │
│  │  Input:                                                │ │
│  │  - System prompt                                       │ │
│  │  - User comment                                        │ │
│  │  - JSON Schema (strict)                                │ │
│  │                                                        │ │
│  │  Processing:                                           │ │
│  │  1. Understand comment sentiment                      │ │
│  │  2. Determine intensity (1-5)                          │ │
│  │  3. Generate ONLY valid JSON per schema                │ │
│  │  4. Validate before returning                          │ │
│  │                                                        │ │
│  │  Output:                                               │ │
│  │  {"sentiment": "positive", "rating": 5}                │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔐 Environment & Configuration

```
┌─────────────────────────────────────────────────────────────┐
│                    Deployment Environment                   │
│                    (Railway / Render)                       │
│                                                             │
│  Environment Variables:                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  OPENAI_API_KEY = sk-...                            │   │
│  │  PORT = 8000 (auto-set by platform)                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Runtime:                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Python 3.11                                         │   │
│  │  Uvicorn ASGI server                                 │   │
│  │  FastAPI framework                                   │   │
│  │  OpenAI SDK                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Configuration Files:                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Procfile: web: uvicorn main:app --host 0.0.0.0     │   │
│  │  runtime.txt: python-3.11                            │   │
│  │  requirements.txt: [dependencies]                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Data Flow

```
INPUT                     PROCESSING                  OUTPUT
─────                     ──────────                  ──────

┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│             │          │             │          │             │
│  "This is   │   ───▶   │   GPT-4o    │   ───▶   │  sentiment: │
│   amazing!" │          │    mini     │          │  "positive" │
│             │          │             │          │             │
└─────────────┘          └─────────────┘          │  rating: 5  │
                                                   │             │
                         ┌─────────────┐          └─────────────┘
                         │ Structured  │
                         │   Schema    │
                         │  ┌───────┐  │
                         │  │"enum" │  │
                         │  │ 1-5   │  │
                         │  └───────┘  │
                         └─────────────┘
                          Enforces Format
```

---

## 🧪 Testing Flow

```
┌────────────────────────────────────────────────────────────┐
│                    Test Script                             │
│                 (test_endpoint.py)                         │
│                                                            │
│  Test Cases:                                               │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 1. "This product is amazing!"                        │ │
│  │    Expected: positive, 4-5                           │ │
│  │                                                      │ │
│  │ 2. "Worst purchase ever"                             │ │
│  │    Expected: negative, 1-2                           │ │
│  │                                                      │ │
│  │ 3. "The product arrived on time"                     │ │
│  │    Expected: neutral, 3                              │ │
│  │                                                      │ │
│  │ 4. "I love it! Best investment!"                     │ │
│  │    Expected: positive, 5                             │ │
│  │                                                      │ │
│  │ 5. "It's okay, nothing special"                      │ │
│  │    Expected: neutral, 2-4                            │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Send POST requests to /comment                      │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Validate responses:                                 │ │
│  │  - HTTP 200 OK                                       │ │
│  │  - JSON structure                                    │ │
│  │  - Valid sentiment enum                              │ │
│  │  - Rating in range 1-5                               │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Results: Pass if 3+ out of 5 correct                │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 Error Handling Flow

```
┌─────────────────────────────────────────────────────────┐
│  Request arrives                                        │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ Input Validation     │
       └──────────┬───────────┘
                  │
        ┌─────────┴─────────┐
        │ Valid?            │
        └─────────┬─────────┘
                  │
        ┌─────────┴─────────┐
     No │                   │ Yes
        ▼                   ▼
┌───────────────┐   ┌──────────────────┐
│ Return 400    │   │ Get OpenAI Key   │
│ Bad Request   │   └────────┬─────────┘
└───────────────┘            │
                   ┌─────────┴─────────┐
                   │ Key exists?       │
                   └─────────┬─────────┘
                             │
                   ┌─────────┴─────────┐
                No │                   │ Yes
                   ▼                   ▼
           ┌───────────────┐   ┌──────────────────┐
           │ Return 500    │   │ Call OpenAI API  │
           │ Server Error  │   └────────┬─────────┘
           └───────────────┘            │
                              ┌─────────┴─────────┐
                              │ API Success?      │
                              └─────────┬─────────┘
                                        │
                              ┌─────────┴─────────┐
                           No │                   │ Yes
                              ▼                   ▼
                      ┌───────────────┐   ┌──────────────────┐
                      │ Return 502    │   │ Parse JSON       │
                      │ Bad Gateway   │   └────────┬─────────┘
                      └───────────────┘            │
                                         ┌─────────┴─────────┐
                                         │ Valid JSON?       │
                                         └─────────┬─────────┘
                                                   │
                                         ┌─────────┴─────────┐
                                      No │                   │ Yes
                                         ▼                   ▼
                                 ┌───────────────┐   ┌──────────────────┐
                                 │ Return 502    │   │ Return 200 OK    │
                                 │ Bad Gateway   │   │ with JSON        │
                                 └───────────────┘   └──────────────────┘
```

---

## 📊 Performance Metrics

```
┌────────────────────────────────────────────────────────────┐
│  Typical Request Timeline                                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  0ms     ├─ Client sends request                          │
│          │                                                 │
│  5ms     ├─ FastAPI receives                              │
│          │                                                 │
│  10ms    ├─ Input validation                              │
│          │                                                 │
│  15ms    ├─ OpenAI API call starts                        │
│          │                                                 │
│  1200ms  ├─ OpenAI processes (avg)                        │
│          │  - Sentiment analysis                          │
│          │  - Schema validation                           │
│          │  - JSON generation                             │
│          │                                                 │
│  1220ms  ├─ Response received                             │
│          │                                                 │
│  1225ms  ├─ JSON parsing                                  │
│          │                                                 │
│  1230ms  ├─ Pydantic validation                           │
│          │                                                 │
│  1235ms  ├─ Client receives response                      │
│          │                                                 │
├────────────────────────────────────────────────────────────┤
│  Total: ~1.2 seconds                                       │
└────────────────────────────────────────────────────────────┘

Breakdown:
- Overhead: ~35ms (FastAPI + validation)
- OpenAI API: ~1200ms (network + processing)
- Total: ~1235ms per request
```

---

## 🔒 Security Architecture

```
┌────────────────────────────────────────────────────────────┐
│  Security Layers                                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. HTTPS (Railway/Render provides SSL)                   │
│     ├─ Encrypted in transit                               │
│     └─ TLS 1.3                                            │
│                                                            │
│  2. API Key Protection                                     │
│     ├─ Stored in environment variables                    │
│     ├─ Never in code or logs                              │
│     └─ Loaded at runtime only                             │
│                                                            │
│  3. Input Validation                                       │
│     ├─ Pydantic models                                    │
│     ├─ Type checking                                      │
│     └─ Length validation                                  │
│                                                            │
│  4. Output Validation                                      │
│     ├─ OpenAI schema enforcement                          │
│     ├─ JSON structure validation                          │
│     └─ Type safety                                        │
│                                                            │
│  5. Error Handling                                         │
│     ├─ No sensitive data in errors                        │
│     ├─ Generic error messages                             │
│     └─ Detailed logs server-side only                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 Success Criteria Diagram

```
┌────────────────────────────────────────────────────────────┐
│                  Request Testing                           │
└────────────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  Send 5 test     │
              │  comments        │
              └────────┬─────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌──────────────────┐        ┌──────────────────┐
│ Check Response   │        │ Check Response   │
│ Structure        │        │ Accuracy         │
└────────┬─────────┘        └────────┬─────────┘
         │                           │
         ▼                           ▼
┌──────────────────┐        ┌──────────────────┐
│ ✓ HTTP 200       │        │ ✓ Sentiment OK   │
│ ✓ JSON format    │        │ ✓ Rating 1-5     │
│ ✓ Has fields     │        │ ✓ Matches expect │
└────────┬─────────┘        └────────┬─────────┘
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  Score: X / 5    │
              └────────┬─────────┘
                       │
              ┌────────┴────────┐
              │                 │
        X < 3 ▼                 ▼ X ≥ 3
       ┌──────────┐      ┌──────────┐
       │   FAIL   │      │   PASS   │
       │   ❌      │      │   ✅      │
       └──────────┘      └──────────┘
```

---

This visual guide shows exactly how all components work together to create a production-ready sentiment analysis API! 🎉
