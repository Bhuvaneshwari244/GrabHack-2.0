"""
Autonomous Code Maintenance Agent - Main Entry Point
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from agent_orchestrator import CodeMaintenanceAgent
from log_analyzer import LogAnalyzer
from mock_data import generate_mock_logs, generate_mock_codebase


class AgentRunner:
    """Main runner for the autonomous code maintenance agent"""
    
    def __init__(self):
        self.agent = CodeMaintenanceAgent()
        self.log_analyzer = LogAnalyzer()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    async def run_full_cycle(self, log_file: Optional[str] = None):
        """Run complete agent cycle: analyze logs → identify issues → generate PRs"""
        
        print("=" * 80)
        print("🤖 AUTONOMOUS CODE MAINTENANCE AGENT")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Step 1: Generate or load logs
        if log_file:
            print(f"📋 Loading logs from: {log_file}")
            with open(log_file, 'r') as f:
                logs = f.readlines()
        else:
            print("📋 Generating mock production logs...")
            logs = generate_mock_logs(count=1000)
            
        print(f"   Loaded {len(logs)} log entries\n")
        
        # Step 2: Analyze logs for patterns
        print("🔍 Step 1: Analyzing logs for error patterns...")
        issues = await self.log_analyzer.analyze_logs(logs)
        print(f"   Found {len(issues)} recurring issues\n")
        
        for idx, issue in enumerate(issues, 1):
            print(f"   Issue #{idx}: {issue['error_type']}")
            print(f"   ├─ Occurrences: {issue['count']}")
            print(f"   ├─ Severity: {issue['severity']}")
            print(f"   └─ Affected: {issue['location']}\n")
        
        # Step 3: Process each issue with the agent
        results = []
        for issue in issues:
            print(f"🧠 Processing: {issue['error_type']}")
            result = await self.agent.process_issue(issue)
            results.append(result)
            
            # Save reasoning log
            self._save_reasoning_log(result)
            
            if result['pr_generated']:
                print(f"   ✅ PR Generated: {result['pr_title']}")
                print(f"   📝 Branch: {result['branch_name']}")
                print(f"   🎯 Confidence: {result['confidence']:.0%}\n")
            else:
                print(f"   ⚠️  Skipped: {result['reason']}\n")
        
        # Step 4: Summary
        print("=" * 80)
        print("📊 EXECUTION SUMMARY")
        print("=" * 80)
        prs_generated = sum(1 for r in results if r['pr_generated'])
        print(f"Issues Analyzed: {len(issues)}")
        print(f"PRs Generated: {prs_generated}")
        print(f"Skipped: {len(issues) - prs_generated}")
        print(f"Output Directory: {self.output_dir.absolute()}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        return results
    
    def _save_reasoning_log(self, result: Dict):
        """Save detailed reasoning log to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reasoning_log_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Also save human-readable version
        txt_file = filepath.with_suffix('.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(self._format_reasoning_log(result))
    
    def _format_reasoning_log(self, result: Dict) -> str:
        """Format reasoning log in human-readable format"""
        log = []
        log.append("=" * 80)
        log.append("AGENT REASONING LOG")
        log.append("=" * 80)
        log.append(f"Timestamp: {result['timestamp']}")
        log.append(f"Issue: {result['issue_type']}\n")
        
        for idx, step in enumerate(result['reasoning_steps'], 1):
            log.append(f"Step {idx}: {step['action']}")
            log.append(f"|- {step['description']}")
            if 'details' in step:
                for detail in step['details']:
                    log.append(f"|- {detail}")
            log.append(f"'- Result: {step['result']}\n")
        
        log.append(f"Final Decision: {'PR Generated' if result['pr_generated'] else 'Skipped'}")
        log.append(f"Confidence: {result['confidence']:.0%}")
        
        if result['pr_generated']:
            log.append(f"\nPR Details:")
            log.append(f"|- Title: {result['pr_title']}")
            log.append(f"|- Branch: {result['branch_name']}")
            log.append(f"'- Files Changed: {len(result['files_changed'])}")
        
        log.append("=" * 80)
        return "\n".join(log)


async def main():
    """Main entry point"""
    runner = AgentRunner()
    
    # Run the agent
    results = await runner.run_full_cycle()
    
    print("\n✨ Agent execution complete! Check the 'output' directory for detailed logs.")


if __name__ == "__main__":
    asyncio.run(main())
