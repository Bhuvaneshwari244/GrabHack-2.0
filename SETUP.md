# Setup Instructions

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- OpenAI API key OR Anthropic API key (for LLM functionality)

## Quick Start (5 minutes)

### 1. Clone and Setup

```bash
# Navigate to project directory
cd autonomous-code-maintenance-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
# Option 1: OpenAI
OPENAI_API_KEY=sk-your-key-here

# Option 2: Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Note**: The agent works in DEMO mode without API keys, using mock responses.

### 3. Run the Agent (CLI)

```bash
# Run the agent
python agent/main.py

# Or analyze specific log file
python agent/main.py --analyze-logs logs/production.log
```

### 4. Run the Web Demo

**Terminal 1 - Backend**:
```bash
cd backend
python main.py
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:5173
```

Open browser to `http://localhost:5173`

## Detailed Setup

### Python Environment

1. **Create virtual environment**:
```bash
python -m venv venv
```

2. **Activate**:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Verify installation**:
```bash
python -c "import langchain; import langgraph; print('✓ Dependencies installed')"
```

### API Configuration

#### Option 1: OpenAI (Recommended)

1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env`:
```bash
OPENAI_API_KEY=sk-proj-...
```

#### Option 2: Anthropic

1. Get API key from https://console.anthropic.com/
2. Add to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

#### Option 3: Demo Mode (No API Key)

The agent works without API keys using mock responses for demonstration.

### Frontend Setup

1. **Install Node.js dependencies**:
```bash
cd frontend
npm install
```

2. **Start development server**:
```bash
npm run dev
```

3. **Build for production**:
```bash
npm run build
```

## Project Structure

```
autonomous-code-maintenance-agent/
├── agent/                      # Core agent code
│   ├── main.py                # Entry point
│   ├── agent_orchestrator.py # LangGraph orchestration
│   ├── log_analyzer.py        # Log analysis
│   ├── code_analyzer.py       # Code analysis
│   ├── fix_generator.py       # Fix generation
│   ├── pr_creator.py          # PR creation
│   └── mock_data.py           # Mock data generator
├── backend/                    # FastAPI backend
│   └── main.py                # API server
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── App.css            # Styles
│   │   └── main.jsx           # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── output/                     # Generated outputs
│   ├── reasoning_log_*.json   # Reasoning logs
│   └── reasoning_log_*.txt    # Human-readable logs
├── README.md                   # Main documentation
├── ARCHITECTURE.md             # Architecture details
├── SAMPLE_REASONING_LOG.md     # Example reasoning log
├── SETUP.md                    # This file
├── requirements.txt            # Python dependencies
└── .env.example               # Environment template
```

## Running the Agent

### CLI Mode

**Basic usage**:
```bash
python agent/main.py
```

**With custom log file**:
```bash
python agent/main.py --analyze-logs path/to/logs.log
```

**Generate mock logs**:
```bash
python agent/mock_data.py
```

### Web Interface

1. **Start backend**:
```bash
cd backend
python main.py
```

2. **Start frontend** (new terminal):
```bash
cd frontend
npm run dev
```

3. **Open browser**:
```
http://localhost:5173
```

4. **Click "Run Agent Cycle"** to see the agent in action

### API Endpoints

**Backend API** (http://localhost:8000):

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/generate-logs` - Generate mock logs
- `POST /api/analyze-logs` - Analyze logs for issues
- `POST /api/process-issue` - Process single issue
- `POST /api/run-full-cycle` - Run complete agent cycle

**Example API call**:
```bash
curl -X POST http://localhost:8000/api/run-full-cycle \
  -H "Content-Type: application/json" \
  -d '{"log_count": 1000}'
```

## Configuration

### Agent Configuration

Edit `.env`:

```bash
# Confidence threshold (0.0 - 1.0)
CONFIDENCE_THRESHOLD=0.80

# Maximum lines changed per PR
MAX_LINES_PER_PR=50

# Enable automatic PR creation (requires GitHub token)
ENABLE_AUTO_PR=false
```

### GitHub Integration (Optional)

To enable actual PR creation:

1. Generate GitHub personal access token
2. Add to `.env`:
```bash
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=your-org/your-repo
```

3. Enable auto PR:
```bash
ENABLE_AUTO_PR=true
```

## Troubleshooting

### Issue: Import errors

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: API key not working

**Solution**:
```bash
# Verify .env file exists
ls -la .env

# Check API key format
cat .env | grep API_KEY

# Test API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### Issue: Frontend not connecting to backend

**Solution**:
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check frontend proxy configuration
cat frontend/vite.config.js

# Restart both servers
```

### Issue: Port already in use

**Solution**:
```bash
# Backend (port 8000)
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows

# Frontend (port 5173)
lsof -ti:5173 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5173   # Windows
```

## Testing

### Run Agent Tests

```bash
# Test log analysis
python -m pytest tests/test_log_analyzer.py

# Test code analysis
python -m pytest tests/test_code_analyzer.py

# Test full pipeline
python -m pytest tests/test_integration.py
```

### Manual Testing

1. **Generate logs**:
```bash
python agent/mock_data.py
```

2. **Run agent**:
```bash
python agent/main.py
```

3. **Check output**:
```bash
ls -la output/
cat output/reasoning_log_*.txt
```

## Demo Mode

For quick demonstration without API keys:

1. **Skip API key setup** - Agent uses mock responses
2. **Run agent**:
```bash
python agent/main.py
```
3. **View results** in `output/` directory

Mock mode provides realistic outputs for demonstration purposes.

## Production Deployment

### Backend Deployment

```bash
# Install production dependencies
pip install gunicorn

# Run with gunicorn
gunicorn backend.main:app --workers 4 --bind 0.0.0.0:8000
```

### Frontend Deployment

```bash
# Build for production
cd frontend
npm run build

# Serve static files
npm install -g serve
serve -s dist -p 5173
```

### Docker Deployment (Optional)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "agent/main.py"]
```

```bash
# Build and run
docker build -t code-maintenance-agent .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY code-maintenance-agent
```

## Next Steps

1. ✅ Complete setup
2. ✅ Run demo in CLI mode
3. ✅ Try web interface
4. ✅ Review reasoning logs in `output/`
5. ✅ Customize configuration in `.env`
6. ✅ Integrate with your codebase

## Support

For issues or questions:
- Check `README.md` for overview
- Review `ARCHITECTURE.md` for technical details
- See `SAMPLE_REASONING_LOG.md` for example output

## License

MIT License - See LICENSE file for details
