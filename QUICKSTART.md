# Quick Start Guide - 5 Minutes to Demo

## Fastest Path to Running Demo

### Option 1: CLI Demo (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run demo (works without API key)
python run_demo.py
```

That's it! The agent will:
- Generate 1000 mock logs
- Identify 3-5 recurring issues
- Generate fixes and PRs
- Save reasoning logs to `output/`

### Option 2: Web Demo (5 minutes)

**Terminal 1 - Backend**:
```bash
pip install -r requirements.txt
cd backend
python main.py
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm install
npm run dev
```

**Browser**: Open `http://localhost:5173` and click "Run Agent Cycle"

---

## What You'll See

### CLI Output
```
🤖 AUTONOMOUS CODE MAINTENANCE AGENT
Started at: 2026-04-12 10:23:45

📋 Generating mock production logs...
   Loaded 1000 log entries

🔍 Step 1: Analyzing logs for error patterns...
   Found 3 recurring issues

   Issue #1: NullPointerException
   ├─ Occurrences: 47
   ├─ Severity: HIGH
   └─ Affected: UserService.java:156

🧠 Processing: NullPointerException
   ✅ PR Generated: Fix NullPointerException in UserService.getProfile
   📝 Branch: auto-fix/nullpointer-20260412
   🎯 Confidence: 95%

📊 EXECUTION SUMMARY
Issues Analyzed: 3
PRs Generated: 2
Skipped: 1
```

### Web Interface
- Summary dashboard with statistics
- List of generated PRs
- Click any result to see detailed reasoning log
- Step-by-step agent thinking process

---

## Key Files to Review

After running the demo, check these files:

1. **`output/reasoning_log_*.txt`** - Human-readable reasoning
2. **`output/reasoning_log_*.json`** - Machine-readable data
3. **`README.md`** - Full documentation
4. **`SAMPLE_REASONING_LOG.md`** - Example output

---

## No API Key? No Problem!

The agent works in **DEMO mode** without API keys:
- Uses realistic mock responses
- Shows complete workflow
- Perfect for demonstration
- All features functional

To use real LLM (optional):
```bash
# Copy template
cp .env.example .env

# Add your key
echo "OPENAI_API_KEY=sk-your-key" >> .env
```

---

## Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows
```

### "npm: command not found"
Install Node.js from https://nodejs.org

---

## Next Steps

1. ✅ Run the demo
2. ✅ Review reasoning logs
3. ✅ Read `README.md` for details
4. ✅ Check `ARCHITECTURE.md` for technical depth
5. ✅ Prepare your presentation using `PRESENTATION_OUTLINE.md`

---

## For GrabHack Submission

You need:
1. **2-slide PPT** - See `PRESENTATION_OUTLINE.md`
2. **2-minute video** - Record demo + explanation
3. **Problem statement** - Already chosen (Engineering & Product Velocity)

Use `SUBMISSION_CHECKLIST.md` for complete submission guide.

---

**Ready? Let's go!**

```bash
python run_demo.py
```

🚀 Good luck with GrabHack 2.0!
