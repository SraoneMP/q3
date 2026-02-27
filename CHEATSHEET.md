# 📋 Quick Cheatsheet - FastAPI Sentiment Analysis

## 🚀 Quick Start (Local)

```bash
# 1. Setup
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-your-key" > .env

# 2. Run
uvicorn main:app --reload --port 8000

# 3. Test
curl -X POST http://localhost:8000/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "This is amazing!"}'
```

## 🌐 Deploy to Railway (2 minutes)

### Web UI (Easiest):
1. Go to https://railway.app → Login
2. New Project → Deploy from GitHub
3. Add variable: `OPENAI_API_KEY=your_key`
4. Generate Domain → Done!

### CLI (Alternative):
```bash
npm install -g @railway/cli
railway login
railway init
railway variables set OPENAI_API_KEY=your_key
railway up
railway domain
```

## 🧪 Testing

```bash
# Run automated tests
python test_endpoint.py

# Test production
python test_endpoint.py https://your-app.railway.app

# Manual test
curl -X POST https://your-app.railway.app/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "Great product!"}'
```

## 📖 Key Concepts

### Structured Output Schema
```python
STRUCTURED_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "sentiment_response",
        "schema": {
            "type": "object",
            "properties": {
                "sentiment": {
                    "type": "string",
                    "enum": ["positive", "negative", "neutral"]
                },
                "rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5
                }
            },
            "required": ["sentiment", "rating"]
        },
        "strict": True  # ← Must be True!
    }
}
```

### API Call
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Must support structured outputs
    messages=[...],
    response_format=STRUCTURED_SCHEMA  # ← Key parameter
)
```

## ❓ Quick Answers

**Q: Normal vs Structured Output?**
- Normal: Free-form text, needs parsing
- Structured: Validated JSON, production-ready

**Q: Which models support it?**
- ✅ gpt-4o, gpt-4o-mini (2024+)
- ❌ gpt-4, gpt-3.5-turbo (old models)
- Reason: Constrained decoding capability

**Q: Streaming vs Structured?**
- Streaming: Incremental tokens
- Structured: Complete validated JSON
- Can't combine: Need full JSON to validate

**Q: How to enforce schema?**
- Use `response_format` parameter
- Set `strict: True`
- Define complete JSON schema

**Q: Why structured for production?**
- ✅ 99.99% reliability vs 85-95%
- ✅ No parsing logic needed
- ✅ Direct database insertion
- ✅ Type safety guaranteed

## 📂 Files Created

```
├── main.py              # FastAPI app with structured outputs ✅
├── requirements.txt     # Dependencies ✅
├── test_endpoint.py     # Testing script ✅
├── deploy.py           # Deployment helper ✅
├── run_local.bat       # Windows run script ✅
├── .env.example        # Environment template ✅
├── Procfile           # Railway/Heroku config ✅
├── runtime.txt        # Python version ✅
├── railway.json       # Railway settings ✅
├── README.md          # Full documentation ✅
├── DEPLOYMENT.md      # Deployment guide ✅
├── RAILWAY_GUIDE.md   # Railway-specific guide ✅
└── ANSWERS.md         # Detailed Q&A ✅
```

## 🔧 Troubleshooting

### Local Issues
```bash
# Port already in use
uvicorn main:app --port 8001

# Missing .env
cp .env.example .env
# Edit .env and add your key

# Import errors
pip install -r requirements.txt
```

### Railway Issues
```bash
# Check logs
railway logs

# Verify variables
railway variables

# Restart
railway restart

# Re-deploy
railway up
```

### API Issues
```bash
# Test with verbose output
curl -v -X POST http://localhost:8000/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "test"}'

# Check API docs
# http://localhost:8000/docs
```

## 📊 Expected Results

### Test Case Examples

| Input | Expected Sentiment | Expected Rating |
|-------|-------------------|-----------------|
| "Amazing product!" | positive | 4-5 |
| "Terrible, waste of money" | negative | 1-2 |
| "Package arrived" | neutral | 3 |
| "Love it!" | positive | 5 |
| "Disappointed" | negative | 1-2 |

### API Response Format
```json
{
  "sentiment": "positive",
  "rating": 5
}
```

## 🔗 Important URLs

**After deployment, you'll have:**
- API endpoint: `https://your-app.railway.app/comment`
- Interactive docs: `https://your-app.railway.app/docs`
- Alternative docs: `https://your-app.railway.app/redoc`

**Resources:**
- Railway Dashboard: https://railway.app/dashboard
- OpenAI API Keys: https://platform.openai.com/api-keys
- OpenAI Docs: https://platform.openai.com/docs/guides/structured-outputs

## ✅ Submission Checklist

- [ ] Code is working locally
- [ ] Deployed to Railway/Render
- [ ] Public URL is accessible
- [ ] `/docs` endpoint shows API documentation
- [ ] POST `/comment` returns correct JSON structure
- [ ] Tested with 5 different comments
- [ ] At least 3/5 tests pass
- [ ] Both sentiment and rating are correct
- [ ] Submitted URL in assignment

## 💡 Pro Tips

1. **Test locally first** - Don't deploy broken code
2. **Check logs** - Railway logs show errors clearly
3. **Use /docs** - Interactive API documentation
4. **Monitor costs** - Should be < $1 for assignment
5. **Save your URL** - You'll need it for submission

## 🎯 Success Criteria

Your API passes when:
- ✅ Returns HTTP 200 OK
- ✅ Content-Type: application/json
- ✅ Has "sentiment" field (valid enum value)
- ✅ Has "rating" field (1-5 integer)
- ✅ 3+ out of 5 test cases correct
- ✅ Consistent response format

---

**Need more details? Check:**
- [README.md](README.md) - Complete documentation
- [RAILWAY_GUIDE.md](RAILWAY_GUIDE.md) - Step-by-step Railway deployment
- [ANSWERS.md](ANSWERS.md) - Detailed answers to all questions
- [DEPLOYMENT.md](DEPLOYMENT.md) - All deployment options
