#!/usr/bin/env python3
"""
Quick demo runner for Autonomous Code Maintenance Agent
"""
import asyncio
import sys
import os
from pathlib import Path

# Add agent directory to path
sys.path.insert(0, str(Path(__file__).parent / "agent"))

from agent.main import AgentRunner


async def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     🤖 AUTONOMOUS CODE MAINTENANCE AGENT - DEMO                 ║
║                                                                  ║
║     Built for GrabHack 2.0: Shaping the Future                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

This demo will:
1. Generate 1000 mock production logs
2. Analyze logs to identify recurring issues
3. Perform root cause analysis
4. Generate code fixes
5. Create Pull Request proposals

Press CTRL+C to stop at any time.
""")
    
    input("Press ENTER to start the demo...")
    print()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  No API key found. Running in DEMO mode with mock responses.")
        print("   To use real LLM: Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        print()
    
    # Run the agent
    runner = AgentRunner()
    results = await runner.run_full_cycle()
    
    print("\n" + "=" * 80)
    print("✨ DEMO COMPLETE!")
    print("=" * 80)
    print(f"\nResults saved to: {runner.output_dir.absolute()}")
    print("\nNext steps:")
    print("1. Review reasoning logs in the 'output' directory")
    print("2. Try the web interface: cd frontend && npm run dev")
    print("3. Explore the code in the 'agent' directory")
    print("\nThank you for trying the Autonomous Code Maintenance Agent!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nPlease check:")
        print("1. Python dependencies are installed: pip install -r requirements.txt")
        print("2. You're in the correct directory")
        print("3. Python version is 3.9 or higher")
        sys.exit(1)
