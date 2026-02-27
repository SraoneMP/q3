#!/usr/bin/env python3
"""
Quick deployment helper for Railway
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    return True

def main():
    print("""
╔════════════════════════════════════════════════════════╗
║         FastAPI Sentiment API - Quick Deploy          ║
╚════════════════════════════════════════════════════════╝
    """)
    
    # Check if Railway CLI is installed
    print("🔍 Checking for Railway CLI...")
    result = subprocess.run("railway --version", shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("\n⚠️  Railway CLI not found!")
        print("\n📖 Installation options:")
        print("\n1. Install Railway CLI:")
        print("   npm install -g @railway/cli")
        print("\n2. Or deploy via Railway web UI:")
        print("   → Go to https://railway.app")
        print("   → Click 'Start a New Project'")
        print("   → Connect your GitHub repository")
        print("   → Add environment variable: OPENAI_API_KEY")
        print("   → Railway will auto-deploy!")
        sys.exit(1)
    
    print("✅ Railway CLI found!")
    
    # Check if logged in
    if not run_command("railway whoami", "Checking Railway login status"):
        print("\n🔐 Please login to Railway:")
        if not run_command("railway login", "Logging in to Railway"):
            sys.exit(1)
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️  OPENAI_API_KEY not found in environment!")
        api_key = input("\n🔑 Enter your OpenAI API key: ").strip()
        if not api_key:
            print("❌ API key is required!")
            sys.exit(1)
    
    # Initialize project
    print("\n🚀 Deploying to Railway...")
    
    # Link or create project
    run_command("railway init", "Initializing Railway project")
    
    # Set environment variable
    if not run_command(f'railway variables set OPENAI_API_KEY="{api_key}"', 
                      "Setting OPENAI_API_KEY"):
        print("⚠️  Failed to set API key, you can set it manually in Railway dashboard")
    
    # Deploy
    if not run_command("railway up", "Deploying application"):
        print("\n❌ Deployment failed!")
        sys.exit(1)
    
    # Get domain
    print("\n🌐 Generating public domain...")
    run_command("railway domain", "Setting up domain")
    
    print("""
    
╔════════════════════════════════════════════════════════╗
║              🎉 Deployment Successful! 🎉             ║
╚════════════════════════════════════════════════════════╝

📍 Your API is now live!

🔗 Find your URL in the Railway dashboard or run:
   railway status

📝 Test your endpoint:
   curl -X POST https://your-url.railway.app/comment \\
     -H "Content-Type: application/json" \\
     -d '{"comment": "This is amazing!"}'

📚 API Documentation:
   https://your-url.railway.app/docs

💡 Need help? Check DEPLOYMENT.md
    """)

if __name__ == "__main__":
    main()
