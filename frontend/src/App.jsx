import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [selectedResult, setSelectedResult] = useState(null)

  const runAgent = async () => {
    setLoading(true)
    setResults(null)
    setSelectedResult(null)

    try {
      const response = await axios.post('/api/run-full-cycle', {
        log_count: 1000
      })
      setResults(response.data)
    } catch (error) {
      console.error('Error running agent:', error)
      alert('Error running agent. Check console for details.')
    } finally {
      setLoading(false)
    }
  }

  const viewDetails = (result) => {
    setSelectedResult(result)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🤖 Autonomous Code Maintenance Agent</h1>
        <p>AI-powered system that monitors logs, identifies bugs, and generates Pull Requests</p>
      </header>

      <div className="container">
        <div className="control-panel">
          <button 
            onClick={runAgent} 
            disabled={loading}
            className="run-button"
          >
            {loading ? '⏳ Running Agent...' : '▶️ Run Agent Cycle'}
          </button>
          <p className="help-text">
            This will analyze 1000 mock production logs, identify issues, and generate fixes
          </p>
        </div>

        {results && (
          <div className="results-section">
            <div className="summary-card">
              <h2>📊 Execution Summary</h2>
              <div className="summary-grid">
                <div className="stat">
                  <div className="stat-value">{results.summary.logs_analyzed}</div>
                  <div className="stat-label">Logs Analyzed</div>
                </div>
                <div className="stat">
                  <div className="stat-value">{results.summary.issues_found}</div>
                  <div className="stat-label">Issues Found</div>
                </div>
                <div className="stat success">
                  <div className="stat-value">{results.summary.prs_generated}</div>
                  <div className="stat-label">PRs Generated</div>
                </div>
                <div className="stat">
                  <div className="stat-value">{results.summary.skipped}</div>
                  <div className="stat-label">Skipped</div>
                </div>
              </div>
            </div>

            <div className="results-list">
              <h2>🔧 Generated Fixes</h2>
              {results.results.map((result, idx) => (
                <div 
                  key={idx} 
                  className={`result-card ${result.pr_generated ? 'success' : 'skipped'}`}
                  onClick={() => viewDetails(result)}
                >
                  <div className="result-header">
                    <span className="result-icon">
                      {result.pr_generated ? '✅' : '⚠️'}
                    </span>
                    <div className="result-info">
                      <h3>{result.issue_type}</h3>
                      <p className="confidence">
                        Confidence: {(result.confidence * 100).toFixed(0)}%
                      </p>
                    </div>
                  </div>
                  {result.pr_generated && (
                    <div className="pr-info">
                      <p><strong>PR:</strong> {result.pr_title}</p>
                      <p><strong>Branch:</strong> {result.branch_name}</p>
                    </div>
                  )}
                  {!result.pr_generated && (
                    <p className="skip-reason">{result.reason}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedResult && (
          <div className="modal-overlay" onClick={() => setSelectedResult(null)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>🧠 Agent Reasoning Log</h2>
                <button onClick={() => setSelectedResult(null)} className="close-btn">×</button>
              </div>
              <div className="modal-content">
                <div className="reasoning-steps">
                  {selectedResult.reasoning_steps.map((step, idx) => (
                    <div key={idx} className="reasoning-step">
                      <h3>Step {idx + 1}: {step.action}</h3>
                      <p>{step.description}</p>
                      {step.details && (
                        <ul>
                          {step.details.map((detail, i) => (
                            <li key={i}>{detail}</li>
                          ))}
                        </ul>
                      )}
                      <p className="step-result"><strong>Result:</strong> {step.result}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <footer className="footer">
        <p>Built for GrabHack 2.0: Shaping the Future</p>
      </footer>
    </div>
  )
}

export default App
