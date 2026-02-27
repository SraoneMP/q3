# 📅 GitHub Actions Daily Commit - DevSync

## ✅ Assignment Implementation Complete

This repository contains a scheduled GitHub Action that automatically commits daily updates as part of DevSync Solutions' workflow automation.

---

## 📋 Assignment Requirements Met

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| ✅ Cron schedule (specific time, no wildcards) | Done | `30 10 * * *` (10:30 AM UTC) |
| ✅ Step with email 21f3000245@ds.study.iitm.ac.in | Done | Multiple steps include email |
| ✅ Creates commit in each run | Done | Commits daily activity logs |
| ✅ Located in .github/workflows/ | Done | `.github/workflows/daily-commit.yml` |
| ✅ Manual trigger capability | Done | `workflow_dispatch` enabled |

---

## 🔄 Workflow Details

### Schedule
- **Cron**: `30 10 * * *`
- **Time**: 10:30 AM UTC daily (4:00 PM IST)
- **Frequency**: Once per day

### What It Does
1. Checks out the repository
2. Configures Git with email: `21f3000245@ds.study.iitm.ac.in`
3. Creates/updates activity logs in `.devsync/logs/`
4. Generates date-specific status files
5. Commits all changes with proper attribution
6. Pushes to the repository

### Files Created/Updated
- `.devsync/logs/activity.log` - Cumulative activity log
- `.devsync/status_YYYY-MM-DD.txt` - Daily status report
- `.devsync/last_sync.txt` - Last sync timestamp
- `.last_run.txt` - Simple last run indicator

---

## 🧪 Testing the Workflow

### Method 1: Manual Trigger (Recommended)
1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Daily Automated Commit - DevSync**
4. Click **Run workflow** dropdown
5. Click **Run workflow** button
6. Wait 30-60 seconds for completion

### Method 2: Using GitHub CLI
```bash
gh workflow run daily-commit.yml
```

### Method 3: Using API
```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/USER/REPO/actions/workflows/daily-commit.yml/dispatches \
  -d '{"ref":"main"}'
```

---

## 📖 Understanding Cron Syntax

### The Pattern: `30 10 * * *`

```
┌───────────── minute (0 - 59)          → 30
│ ┌───────────── hour (0 - 23)          → 10 (10 AM UTC)
│ │ ┌───────────── day of month (1-31)  → * (every day)
│ │ │ ┌───────────── month (1 - 12)     → * (every month)
│ │ │ │ ┌───────────── day of week (0-6) → * (every day of week)
│ │ │ │ │
* * * * *
```

### Common Examples
| Cron | Description |
|------|-------------|
| `0 0 * * *` | Every day at midnight UTC |
| `30 10 * * *` | Every day at 10:30 AM UTC (our implementation) |
| `0 */6 * * *` | Every 6 hours |
| `0 9 * * 1` | Every Monday at 9 AM |
| `15 14 1 * *` | 1st day of every month at 2:15 PM |

---

## ❓ Questions Answered

### 1. What is cron syntax and how do I read '0 * * * *'?

**Cron syntax** is a time-based job scheduler format used in Unix-like systems.

**Reading `0 * * * *`:**
- `0` = minute (at the start of the hour)
- `*` = hour (every hour)
- `*` = day of month (every day)
- `*` = month (every month)
- `*` = day of week (every day of week)

**Result**: Runs every hour, on the hour (00:00, 01:00, 02:00, etc.)

### 2. Why use GitHub Actions for scheduling instead of cron on a server?

**Advantages of GitHub Actions:**
- ✅ **No server maintenance** - GitHub manages infrastructure
- ✅ **Free for public repos** - 2,000 minutes/month for private
- ✅ **Version controlled** - Workflow is in your repo
- ✅ **Built-in secrets management** - Secure token handling
- ✅ **Integrated with Git** - Direct repo access
- ✅ **Scalable** - Automatic resource allocation
- ✅ **Cross-platform** - Works on Ubuntu, Windows, macOS
- ✅ **No setup** - No need to provision servers

**Traditional Cron Disadvantages:**
- ❌ Requires server maintenance
- ❌ Server costs
- ❌ Manual security updates
- ❌ Single point of failure
- ❌ Requires SSH access management

### 3. What are the limitations of GitHub Actions scheduled workflows?

**Time Limitations:**
- ⚠️ **Shortest interval**: Every 5 minutes (not every minute)
- ⚠️ **Delay**: May run up to 15-30 minutes late during high load
- ⚠️ **No exact guarantee**: Schedule is "best effort"

**Resource Limitations:**
- 📊 **Free tier**: 2,000 minutes/month for private repos
- 📊 **Public repos**: Unlimited minutes
- 📊 **Job timeout**: 6 hours max per job
- 📊 **Workflow timeout**: 72 hours max

**Repository Limitations:**
- 🔒 **Inactive repos**: Disabled after 60 days of no repo activity
- 🔒 **Requires push access**: Workflow needs write permissions
- 🔒 **Branch restrictions**: Runs from default branch only

**Other Limitations:**
- ⛔ Cannot run more frequently than cron allows
- ⛔ Timezone is always UTC
- ⛔ Requires internet connectivity

### 4. How do I test a scheduled workflow without waiting for the cron time?

**Method 1: workflow_dispatch (Built into our workflow)**
```yaml
on:
  schedule:
    - cron: '30 10 * * *'
  workflow_dispatch:  # ← This enables manual trigger
```

**Testing Steps:**
1. Go to GitHub repo → **Actions** tab
2. Select your workflow
3. Click **Run workflow** button
4. Select branch and click **Run workflow**

**Method 2: GitHub CLI**
```bash
gh workflow run daily-commit.yml
gh run watch  # Watch it run
```

**Method 3: Git Push Trigger (Temporary)**
```yaml
on:
  push:  # Add temporarily for testing
  schedule:
    - cron: '30 10 * * *'
```

**Method 4: API Request**
```bash
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/USER/REPO/actions/workflows/daily-commit.yml/dispatches \
  -d '{"ref":"main"}'
```

### 5. What happens to scheduled workflows if my repository becomes inactive?

**GitHub's Inactivity Policy:**
- ⏰ After **60 days** of no repo activity, scheduled workflows are **automatically disabled**
- 📧 GitHub sends a warning email before disabling
- 🔄 To re-enable: Make any commit or manually trigger a workflow

**What counts as activity:**
- Any git push
- Creating/closing issues
- Pull request activity
- Manual workflow runs
- Repository setting changes

**Prevention:**
- ✅ Our workflow commits daily = keeps repo active
- ✅ Each commit resets the 60-day timer
- ✅ Self-sustaining workflow

### 6. How do I make my scheduled workflow commit changes back to the repo?

**Our Implementation (already done):**

```yaml
steps:
  - name: Checkout with write permissions
    uses: actions/checkout@v4
    with:
      token: ${{ secrets.GITHUB_TOKEN }}  # ← Built-in token
  
  - name: Configure Git
    run: |
      git config user.name "DevSync Bot"
      git config user.email "21f3000245@ds.study.iitm.ac.in"
  
  - name: Make changes
    run: |
      echo "Content" > file.txt
  
  - name: Commit and push
    run: |
      git add .
      git commit -m "Automated commit"
      git push
```

**Key Requirements:**
1. **Permissions**: Add `contents: write` to job
2. **Token**: Use `${{ secrets.GITHUB_TOKEN }}`
3. **Git config**: Set user.name and user.email
4. **Push**: Use `git push` (authenticated automatically)

**Alternative: Create PR instead of direct push:**
```yaml
- name: Create Pull Request
  uses: peter-evans/create-pull-request@v5
  with:
    commit-message: Automated update
    branch: automated-updates
```

### 7. What is the difference between Cron jobs and Systemd timers in Linux?

| Feature | Cron | Systemd Timers |
|---------|------|----------------|
| **Age** | Since 1970s | Since 2010 |
| **Syntax** | `* * * * *` format | Unit files (`.timer` + `.service`) |
| **Granularity** | Minute-level | Microsecond-level |
| **Logs** | Separate log files | Integrated with journalctl |
| **Dependencies** | None | Can depend on other services |
| **Missed runs** | Skip if system was off | Can catch up with `Persistent=true` |
| **Monitoring** | Manual | `systemctl status` |
| **Security** | Basic user isolation | Full systemd security features |

**Cron Example:**
```bash
# /etc/cron.d/myapp
30 10 * * * user /path/to/script.sh
```

**Systemd Timer Example:**
```ini
# /etc/systemd/system/myapp.timer
[Unit]
Description=Run myapp daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

**When to use each:**
- **Cron**: Simple periodic tasks, backward compatibility
- **Systemd**: Modern Linux, complex dependencies, better logging
- **GitHub Actions**: Cloud-based, Git-integrated, no server needed

---

## 🚀 Deployment Steps

### 1. Create GitHub Repository
```bash
# If not already created
gh repo create TDS-GAA3 --public --source=. --remote=origin
```

### 2. Initial Commit and Push
```bash
git add .
git commit -m "Initial commit: FastAPI + GitHub Actions automation"
git branch -M main
git push -u origin main
```

### 3. Verify Workflow
- Go to: `https://github.com/YOUR_USERNAME/TDS-GAA3/actions`
- You should see "Daily Automated Commit - DevSync"

### 4. Test Manual Trigger
- Click on the workflow
- Click "Run workflow"
- Wait for it to complete (~30 seconds)

### 5. Verify Commit
- Check the commit history
- You should see a new commit with message: "chore: Daily automated update..."

---

## 📊 Workflow Status

### Check Status
```bash
# Using GitHub CLI
gh run list --workflow=daily-commit.yml

# View latest run
gh run view

# Watch real-time
gh run watch
```

### Expected Behavior
- ✅ Workflow runs daily at 10:30 AM UTC
- ✅ Creates files in `.devsync/` directory
- ✅ Commits with email: 21f3000245@ds.study.iitm.ac.in
- ✅ Appears in Actions tab
- ✅ Shows green checkmark when successful

---

## 🔍 Troubleshooting

### Workflow not appearing in Actions?
- Ensure `.github/workflows/` directory exists
- Ensure YAML file is valid (check indentation)
- Push to main/master branch

### Workflow not creating commits?
- Check permissions: `contents: write` is set
- Verify GITHUB_TOKEN has push access
- Check workflow logs for errors

### Workflow disabled?
- Re-enable in Settings → Actions → General
- Or push any commit to reactive

### "Permission denied" error?
- Add `permissions: contents: write` to job
- Ensure branch protection rules allow Actions

---

## 📁 Repository Structure

```
TDS-GAA3/
├── .github/
│   └── workflows/
│       └── daily-commit.yml       ← Scheduled workflow
├── .devsync/                       ← Created by workflow
│   ├── logs/
│   │   └── activity.log
│   ├── status_2026-02-28.txt
│   └── last_sync.txt
├── .last_run.txt                  ← Created by workflow
├── main.py                        ← FastAPI app
├── requirements.txt
├── README.md
├── GITHUB_ACTIONS.md              ← This file
└── [other files...]
```

---

## 🎯 Success Criteria

✅ **Workflow file exists**: `.github/workflows/daily-commit.yml`
✅ **Cron uses specific time**: `30 10 * * *` (not wildcards like `* * * * *`)
✅ **Email in step name**: "21f3000245@ds.study.iitm.ac.in"
✅ **Creates commits**: Verified by git history
✅ **Manual trigger works**: workflow_dispatch enabled
✅ **Runs successfully**: Green checkmark in Actions

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Schedule Syntax](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [Crontab Guru](https://crontab.guru/) - Cron expression explainer
- [GitHub Actions Limits](https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration)

---

**🎉 Implementation Complete!**

Your scheduled GitHub Action is ready. Push this to GitHub and it will run automatically every day at 10:30 AM UTC!
