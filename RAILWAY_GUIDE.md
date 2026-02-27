# 🚂 Railway Deployment Guide - 2 Minutes to Live API

## Prerequisites
- OpenAI API key (get from https://platform.openai.com/api-keys)
- GitHub account (optional but recommended)

## Option 1: Deploy via Railway Web UI (Easiest - No Code)

### Step 1: Prepare Your Code
1. Make sure all files are committed to Git
2. Push to GitHub (if you want automatic deployments)

### Step 2: Deploy on Railway

1. **Go to Railway**
   - Visit https://railway.app
   - Click "Login" and sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `TDS-GAA3`

3. **Configure Environment**
   - Railway will auto-detect Python
   - Click "Variables" tab
   - Click "New Variable"
   - Add:
     - **Variable**: `OPENAI_API_KEY`
     - **Value**: `sk-...` (your actual OpenAI key)

4. **Generate Public URL**
   - Click "Settings" tab
   - Scroll to "Networking"
   - Click "Generate Domain"
   - You'll get a URL like: `https://tds-gaa3-production.up.railway.app`

5. **Wait for Deployment**
   - Watch the "Deployments" tab
   - Should complete in 1-2 minutes
   - Look for "✓ Success" status

### Step 3: Test Your API

```bash
# Replace with your actual Railway URL
curl -X POST https://your-app.railway.app/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "This product is amazing!"}'

# Expected response:
# {"sentiment":"positive","rating":5}
```

### Step 4: View API Documentation

Visit your Railway URL:
- Main docs: `https://your-app.railway.app/docs`
- Alternative docs: `https://your-app.railway.app/redoc`

---

## Option 2: Deploy via Railway CLI (For Developers)

### Install Railway CLI

**Windows (PowerShell):**
```powershell
npm install -g @railway/cli
```

**Mac/Linux:**
```bash
npm install -g @railway/cli
# OR
brew install railway
```

### Deploy Steps

1. **Login to Railway**
   ```bash
   railway login
   ```

2. **Initialize Project**
   ```bash
   cd d:\Personal\TDS-GAA3
   railway init
   ```
   - Name your project (e.g., "sentiment-api")

3. **Set Environment Variable**
   ```bash
   railway variables set OPENAI_API_KEY=your_actual_key_here
   ```

4. **Deploy**
   ```bash
   railway up
   ```
   - This uploads your code and starts deployment
   - Wait for "✓ Build successful"

5. **Generate Domain**
   ```bash
   railway domain
   ```
   - Creates a public URL for your API

6. **Check Status**
   ```bash
   railway status
   ```

### View Logs

```bash
# Stream live logs
railway logs

# Filter for errors
railway logs | grep ERROR
```

---

## Troubleshooting

### Issue: "Build Failed"

**Check build logs:**
```bash
railway logs
```

**Common causes:**
1. Missing `requirements.txt` → Should already exist in project
2. Wrong Python version → Railway uses Python 3.11 by default
3. Missing dependencies → Check `requirements.txt` is complete

**Solution:**
```bash
# Verify files exist
ls requirements.txt main.py

# Re-deploy
railway up
```

### Issue: "Service Unavailable" or 502

**Causes:**
1. App crashed on startup
2. Wrong start command
3. Missing OPENAI_API_KEY

**Solution:**
```bash
# Check logs for errors
railway logs

# Verify environment variable
railway variables

# Should show OPENAI_API_KEY=sk-...
```

### Issue: "OPENAI_API_KEY not set"

**Check if variable exists:**
```bash
railway variables
```

**If missing:**
```bash
railway variables set OPENAI_API_KEY=your_key
```

**Restart service:**
```bash
railway restart
```

### Issue: Port binding error

Railway automatically sets `$PORT` environment variable. Your app should use:

```python
# In main.py (already configured correctly)
# Uvicorn will bind to $PORT automatically
```

**Check Procfile:**
```bash
cat Procfile
# Should show: web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Post-Deployment Checklist

- [ ] API responds at `/` endpoint
- [ ] `/docs` shows Swagger UI
- [ ] POST `/comment` returns correct JSON structure
- [ ] Test with positive comment
- [ ] Test with negative comment
- [ ] Test with neutral comment
- [ ] Monitor logs for errors
- [ ] Note URL for submission

---

## Cost Information

**Railway Pricing:**
- **Free Trial**: $5 credit (no credit card needed)
- **Usage**: ~$0.002 per hour
- **Estimated cost**: $1-2 for this assignment
- **Hobby Plan**: $5/month (500 hours included)

**This assignment should use < $1 of your free credit!**

---

## Monitoring & Logs

### View Logs in Dashboard
1. Go to https://railway.app/dashboard
2. Select your project
3. Click on service
4. Click "Logs" tab

### View Metrics
1. In project dashboard
2. Click "Metrics" tab
3. See:
   - CPU usage
   - Memory usage
   - Network traffic
   - Request count

---

## Environment Variables Management

### List all variables
```bash
railway variables
```

### Add new variable
```bash
railway variables set KEY=value
```

### Remove variable
```bash
railway variables delete KEY
```

### Update existing variable
```bash
railway variables set OPENAI_API_KEY=new_key
railway restart  # Restart to apply changes
```

---

## Updating Your Deployment

### Method 1: Push to GitHub (Auto-deploy)
```bash
git add .
git commit -m "Update API"
git push

# Railway auto-deploys from GitHub
```

### Method 2: Manual Upload
```bash
railway up
```

---

## Deleting Your Project

When done with assignment:

**Via CLI:**
```bash
railway delete
```

**Via Web:**
1. Go to project
2. Settings → Danger Zone
3. Delete Project

---

## Getting Your URL for Submission

### Via CLI:
```bash
railway status
```

### Via Web:
1. Open project in Railway dashboard
2. Look for "Deployments" section
3. Your URL is shown as "Domain"

### Format:
```
https://your-project-name-production.up.railway.app
```

**Your submission URL:**
```
https://your-project-name-production.up.railway.app/comment
```

---

## Testing Your Deployed API

### Use the test script:
```bash
python test_endpoint.py https://your-app.railway.app
```

### Manual tests:
```bash
# Positive
curl -X POST https://your-app.railway.app/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "Amazing product, love it!"}'

# Expected: {"sentiment":"positive","rating":5}

# Negative
curl -X POST https://your-app.railway.app/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "Terrible, waste of money"}'

# Expected: {"sentiment":"negative","rating":1}

# Neutral
curl -X POST https://your-app.railway.app/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "Package arrived on time"}'

# Expected: {"sentiment":"neutral","rating":3}
```

---

## Alternative: If Railway Doesn't Work

### Try Render (Free Tier)

1. Go to https://render.com
2. Sign up with GitHub
3. New → Web Service
4. Connect repository
5. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Add `OPENAI_API_KEY`
6. Create Web Service

URL format: `https://your-app.onrender.com`

---

## Success Criteria

Your API is working correctly when:

✅ Returns 200 OK status
✅ Content-Type is `application/json`
✅ Response has `sentiment` field (positive/negative/neutral)
✅ Response has `rating` field (1-5)
✅ 3+ out of 5 test cases pass
✅ No parsing errors in logs

---

## Quick Reference

```bash
# Deploy
railway up

# Generate URL
railway domain

# View logs
railway logs

# Check status
railway status

# Set API key
railway variables set OPENAI_API_KEY=sk-...

# Restart
railway restart

# Test
curl -X POST https://your-url.railway.app/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "test"}'
```

---

**🎉 You're done! Submit your Railway URL and you're all set!**
