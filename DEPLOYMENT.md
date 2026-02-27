# Cloudflare Workers Deployment Guide

This FastAPI application uses OpenAI's structured outputs for sentiment analysis.

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key:**
   ```bash
   # Copy .env.example to .env
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run locally:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Test the endpoint:**
   ```bash
   curl -X POST http://localhost:8000/comment \
     -H "Content-Type: application/json" \
     -d '{"comment": "This product is amazing!"}'
   ```

## Deployment Options

### ⚡ Quick Deploy (Recommended)

Since Cloudflare Workers doesn't natively support Python/FastAPI, here are the best alternatives:

#### Option 1: Railway (Fastest - 2 minutes)

1. **Go to Railway:** https://railway.app
2. **Click "Start a New Project"** → "Deploy from GitHub repo"
3. **Connect this repository**
4. **Add Environment Variable:**
   - Variable: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
5. **Railway auto-detects Python and deploys!**
6. **Click "Generate Domain"** to get your URL

Your endpoint will be: `https://your-app.railway.app/comment`

#### Option 2: Render (Free Tier Available)

1. **Go to Render:** https://render.com
2. **New → Web Service**
3. **Connect your GitHub repository**
4. **Configure:**
   - **Name:** sentiment-api
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variable:**
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
6. **Create Web Service**

Your endpoint will be: `https://sentiment-api.onrender.com/comment`

#### Option 3: Deploy to Vercel (Serverless)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json`:**
   ```json
   {
     "builds": [{"src": "main.py", "use": "@vercel/python"}],
     "routes": [{"src": "/(.*)", "dest": "main.py"}]
   }
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

4. **Add environment variable:**
   ```bash
   vercel env add OPENAI_API_KEY production
   ```

### 🔧 Cloudflare Workers Alternative

Since you specifically mentioned Cloudflare, here's how to use it with a proxy approach:

1. **Deploy your FastAPI to Railway/Render first**
2. **Create a Cloudflare Worker as a proxy/cache layer:**

```javascript
// worker.js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Proxy to your Railway/Render deployment
    const backendUrl = 'https://your-app.railway.app';
    const backendRequest = new Request(backendUrl + url.pathname, {
      method: request.method,
      headers: request.headers,
      body: request.body,
    });
    
    return fetch(backendRequest);
  }
}
```

This gives you Cloudflare's global CDN + your Python backend!

## Testing

Test with curl:
```bash
# Positive sentiment
curl -X POST https://your-url.com/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "This product is amazing!"}'

# Expected: {"sentiment": "positive", "rating": 5}

# Negative sentiment
curl -X POST https://your-url.com/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "Worst purchase ever, completely disappointed"}'

# Expected: {"sentiment": "negative", "rating": 1}

# Neutral sentiment
curl -X POST https://your-url.com/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "The product arrived on time"}'

# Expected: {"sentiment": "neutral", "rating": 3}
```

## API Documentation

Once deployed, visit:
- `/docs` - Interactive Swagger UI
- `/redoc` - Alternative ReDoc documentation

## Structured Output Details

This implementation uses OpenAI's structured outputs feature:

1. **JSON Schema Definition:** The `STRUCTURED_SCHEMA` defines exact output format
2. **Model:** Uses `gpt-4o-mini` which supports structured outputs
3. **Validation:** Pydantic models ensure type safety
4. **Content-Type:** Returns `application/json` with strict schema

## Answer to Questions

**Q: What is the difference between a normal AI text response vs a structured output response?**

A: Normal text responses return free-form text that requires parsing. Structured outputs guarantee valid JSON matching a specific schema, eliminating parsing errors and ensuring consistency.

**Q: Which AI models support structured outputs?**

A: GPT-4o, GPT-4o-mini, and GPT-4o-2024-08-06 and later support structured outputs. Older models like GPT-3.5-turbo and GPT-4 (non-4o) do not have this feature because they lack the constrained decoding capability.

**Q: What is the difference between streaming responses and structured outputs?**

A: Streaming sends tokens incrementally as they're generated. Structured outputs return complete, schema-validated JSON at once. They're incompatible - structured outputs require the full response to validate against the schema.

**Q: How do I enforce a specific JSON schema in OpenAI's structured output?**

A: Use the `response_format` parameter with type `json_schema` and set `strict: True`. Define your schema with exact property types, enums, and required fields.

**Q: Why is structured output better than parsing text for production APIs?**

A: 
- **Guaranteed Format:** No parsing errors or malformed JSON
- **Type Safety:** Schema validation ensures correct data types
- **Consistency:** Every response matches the exact structure
- **No Regex/Parsing:** Eliminates fragile text parsing logic
- **Database Ready:** Can directly insert into DB without transformation
