"""
FastAPI Backend for Code Maintenance Agent Demo
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent_orchestrator import CodeMaintenanceAgent
from agent.log_analyzer import LogAnalyzer
from agent.mock_data import generate_mock_logs

app = FastAPI(title="Autonomous Code Maintenance Agent API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = CodeMaintenanceAgent()
log_analyzer = LogAnalyzer()


class AnalyzeRequest(BaseModel):
    log_count: Optional[int] = 1000


class IssueProcessRequest(BaseModel):
    issue: Dict


@app.get("/")
async def root():
    return {
        "message": "Autonomous Code Maintenance Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_logs": "/api/generate-logs",
            "analyze_logs": "/api/analyze-logs",
            "process_issue": "/api/process-issue"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "ready"}


@app.post("/api/generate-logs")
async def generate_logs(request: AnalyzeRequest):
    """Generate mock production logs"""
    try:
        logs = generate_mock_logs(count=request.log_count)
        return {
            "success": True,
            "log_count": len(logs),
            "logs": logs[:50],  # Return first 50 for preview
            "message": f"Generated {len(logs)} log entries"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-logs")
async def analyze_logs(request: AnalyzeRequest):
    """Analyze logs and identify issues"""
    try:
        # Generate logs
        logs = generate_mock_logs(count=request.log_count)
        
        # Analyze
        issues = await log_analyzer.analyze_logs(logs)
        
        return {
            "success": True,
            "log_count": len(logs),
            "issues_found": len(issues),
            "issues": issues
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/process-issue")
async def process_issue(request: IssueProcessRequest):
    """Process a single issue and generate fix"""
    try:
        result = await agent.process_issue(request.issue)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/run-full-cycle")
async def run_full_cycle(request: AnalyzeRequest):
    """Run complete agent cycle: analyze logs → generate fixes → create PRs"""
    try:
        # Generate logs
        logs = generate_mock_logs(count=request.log_count)
        
        # Analyze logs
        issues = await log_analyzer.analyze_logs(logs)
        
        # Process each issue
        results = []
        for issue in issues:
            result = await agent.process_issue(issue)
            results.append(result)
        
        # Summary
        prs_generated = sum(1 for r in results if r['pr_generated'])
        
        return {
            "success": True,
            "summary": {
                "logs_analyzed": len(logs),
                "issues_found": len(issues),
                "prs_generated": prs_generated,
                "skipped": len(issues) - prs_generated
            },
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
