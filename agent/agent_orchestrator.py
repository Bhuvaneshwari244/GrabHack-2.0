"""
Agent Orchestrator using LangGraph for multi-step reasoning
"""
import os
from datetime import datetime
from typing import Dict, List, TypedDict, Annotated
from operator import add
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

try:
    from langchain_community.llms import Ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from langchain_huggingface import HuggingFaceEndpoint
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False

from agent.code_analyzer import CodeAnalyzer
from agent.fix_generator import FixGenerator
from agent.pr_creator import PRCreator


class AgentState(TypedDict):
    """State passed between agent nodes"""
    issue: Dict
    code_location: Dict
    root_cause: Dict
    fix_proposal: Dict
    validation_result: Dict
    pr_data: Dict
    reasoning_steps: Annotated[List[Dict], add]
    confidence: float
    should_create_pr: bool


class CodeMaintenanceAgent:
    """Main agent orchestrator using LangGraph"""
    
    def __init__(self):
        # Initialize LLM
        if os.getenv("OPENAI_API_KEY"):
            self.llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
            print("✅ Using OpenAI GPT-4")
        elif os.getenv("ANTHROPIC_API_KEY"):
            self.llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0)
            print("✅ Using Anthropic Claude")
        elif os.getenv("HUGGINGFACE_API_TOKEN") and HUGGINGFACE_AVAILABLE:
            model_name = os.getenv("HUGGINGFACE_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
            self.llm = HuggingFaceEndpoint(
                repo_id=model_name,
                huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN"),
                temperature=0.1,
                max_new_tokens=512
            )
            print(f"✅ Using Hugging Face ({model_name}) - FREE Online API")
        elif os.getenv("USE_OLLAMA") == "true" and OLLAMA_AVAILABLE:
            model_name = os.getenv("OLLAMA_MODEL", "llama3.1")
            self.llm = Ollama(model=model_name, base_url="http://localhost:11434")
            print(f"✅ Using Ollama ({model_name}) - FREE Local LLM")
        else:
            # Fallback to mock for demo
            self.llm = None
            print("⚠️  No API key found. Running in DEMO mode with mock responses.")
        
        # Initialize components
        self.code_analyzer = CodeAnalyzer(self.llm)
        self.fix_generator = FixGenerator(self.llm)
        self.pr_creator = PRCreator(self.llm)
        
        # Build agent graph
        self.graph = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """Build the agent workflow graph"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_code", self._analyze_code_node)
        workflow.add_node("determine_root_cause", self._root_cause_node)
        workflow.add_node("generate_fix", self._generate_fix_node)
        workflow.add_node("validate_fix", self._validate_fix_node)
        workflow.add_node("create_pr", self._create_pr_node)
        
        # Define edges
        workflow.set_entry_point("analyze_code")
        workflow.add_edge("analyze_code", "determine_root_cause")
        workflow.add_edge("determine_root_cause", "generate_fix")
        workflow.add_edge("generate_fix", "validate_fix")
        
        # Conditional edge: only create PR if validation passes
        workflow.add_conditional_edges(
            "validate_fix",
            self._should_create_pr,
            {
                True: "create_pr",
                False: END
            }
        )
        workflow.add_edge("create_pr", END)
        
        return workflow.compile()
    
    async def process_issue(self, issue: Dict) -> Dict:
        """Process a single issue through the agent pipeline"""
        
        # Initialize state
        initial_state = {
            "issue": issue,
            "code_location": {},
            "root_cause": {},
            "fix_proposal": {},
            "validation_result": {},
            "pr_data": {},
            "reasoning_steps": [],
            "confidence": 0.0,
            "should_create_pr": False
        }
        
        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        # Format output
        return {
            "timestamp": datetime.now().isoformat(),
            "issue_type": issue['error_type'],
            "reasoning_steps": final_state['reasoning_steps'],
            "confidence": final_state['confidence'],
            "pr_generated": final_state['should_create_pr'],
            "pr_title": final_state['pr_data'].get('title', ''),
            "branch_name": final_state['pr_data'].get('branch', ''),
            "files_changed": final_state['pr_data'].get('files', []),
            "reason": final_state.get('skip_reason', '')
        }
    
    async def _analyze_code_node(self, state: AgentState) -> AgentState:
        """Node: Analyze code to find issue location"""
        issue = state['issue']
        
        code_location = await self.code_analyzer.find_issue_location(issue)
        
        state['code_location'] = code_location
        state['reasoning_steps'].append({
            "action": "Code Location Identification",
            "description": f"Traced error to {code_location['file']}:{code_location['line']}",
            "details": [
                f"Method: {code_location['method']}",
                f"Context: {code_location['context']}"
            ],
            "result": "Location identified"
        })
        
        return state
    
    async def _root_cause_node(self, state: AgentState) -> AgentState:
        """Node: Determine root cause of the issue"""
        issue = state['issue']
        code_location = state['code_location']
        
        root_cause = await self.code_analyzer.analyze_root_cause(
            issue, 
            code_location
        )
        
        state['root_cause'] = root_cause
        state['confidence'] = root_cause['confidence']
        state['reasoning_steps'].append({
            "action": "Root Cause Analysis",
            "description": root_cause['description'],
            "details": [
                f"Issue Type: {root_cause['type']}",
                f"Impact: {root_cause['impact']}",
                f"Confidence: {root_cause['confidence']:.0%}"
            ],
            "result": "Root cause identified"
        })
        
        return state
    
    async def _generate_fix_node(self, state: AgentState) -> AgentState:
        """Node: Generate code fix"""
        root_cause = state['root_cause']
        code_location = state['code_location']
        
        fix_proposal = await self.fix_generator.generate_fix(
            root_cause,
            code_location
        )
        
        state['fix_proposal'] = fix_proposal
        state['reasoning_steps'].append({
            "action": "Solution Generation",
            "description": fix_proposal['strategy'],
            "details": [
                f"Lines changed: {fix_proposal['lines_changed']}",
                f"Backward compatible: {fix_proposal['backward_compatible']}"
            ],
            "result": "Fix generated"
        })
        
        return state
    
    async def _validate_fix_node(self, state: AgentState) -> AgentState:
        """Node: Validate the generated fix"""
        fix_proposal = state['fix_proposal']
        
        validation = await self.fix_generator.validate_fix(fix_proposal)
        
        state['validation_result'] = validation
        state['should_create_pr'] = (
            validation['passed'] and 
            state['confidence'] >= 0.80
        )
        
        state['reasoning_steps'].append({
            "action": "Fix Validation",
            "description": "Validated fix against safety criteria",
            "details": [
                f"Syntax valid: {validation['syntax_valid']}",
                f"Safety checks: {validation['safety_passed']}",
                f"Blast radius: {validation['blast_radius']}"
            ],
            "result": "Validation passed" if validation['passed'] else "Validation failed"
        })
        
        if not state['should_create_pr']:
            state['skip_reason'] = validation.get('reason', 'Confidence too low')
        
        return state
    
    async def _create_pr_node(self, state: AgentState) -> AgentState:
        """Node: Create Pull Request"""
        pr_data = await self.pr_creator.create_pr(
            issue=state['issue'],
            fix=state['fix_proposal'],
            reasoning=state['reasoning_steps']
        )
        
        state['pr_data'] = pr_data
        state['reasoning_steps'].append({
            "action": "PR Creation",
            "description": f"Created PR: {pr_data['title']}",
            "details": [
                f"Branch: {pr_data['branch']}",
                f"Files: {', '.join(pr_data['files'])}"
            ],
            "result": "PR created successfully"
        })
        
        return state
    
    def _should_create_pr(self, state: AgentState) -> bool:
        """Conditional edge: decide if PR should be created"""
        return state['should_create_pr']
