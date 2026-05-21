"""
Code Analyzer - Finds issue locations and performs root cause analysis
"""
from typing import Dict, Optional
from langchain_core.prompts import ChatPromptTemplate


class CodeAnalyzer:
    """Analyzes code to find issues and determine root causes"""
    
    def __init__(self, llm):
        self.llm = llm
        
    async def find_issue_location(self, issue: Dict) -> Dict:
        """Find the exact code location of the issue"""
        
        # In a real system, this would use AST parsing and code search
        # For demo, we'll generate realistic mock data
        
        location_map = {
            'NullPointerException': {
                'file': 'src/services/UserService.java',
                'line': 156,
                'method': 'getProfile',
                'context': 'Accessing user.preferences without null check',
                'code_snippet': '''
public Profile getProfile(String userId) {
    User user = userRepo.findById(userId);
    return new Profile(user.name, user.preferences.theme);  // Issue here
}
'''
            },
            'IndexOutOfBounds': {
                'file': 'src/utils/ListProcessor.py',
                'line': 89,
                'method': 'process_batch',
                'context': 'Accessing list index without bounds check',
                'code_snippet': '''
def process_batch(items, batch_size):
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        result = batch[batch_size]  # Issue: should be batch[0] or batch[-1]
        yield result
'''
            },
            'TimeoutException': {
                'file': 'src/api/PaymentGateway.ts',
                'line': 234,
                'method': 'processPayment',
                'context': 'API call without timeout configuration',
                'code_snippet': '''
async processPayment(orderId: string): Promise<PaymentResult> {
    const response = await fetch(PAYMENT_API_URL, {
        method: 'POST',
        body: JSON.stringify({ orderId })
        // Missing: timeout configuration
    });
    return response.json();
}
'''
            }
        }
        
        error_type = issue['error_type']
        return location_map.get(error_type, {
            'file': 'src/unknown/Unknown.java',
            'line': 0,
            'method': 'unknown',
            'context': 'Unable to locate exact issue',
            'code_snippet': '// Code not found'
        })
    
    async def analyze_root_cause(self, issue: Dict, code_location: Dict) -> Dict:
        """Analyze root cause using LLM reasoning"""
        
        if self.llm:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert code analyzer. Analyze the given error and code to determine the root cause.
                
Provide:
1. Root cause description
2. Issue type (null_check, bounds_check, timeout, etc.)
3. Impact assessment
4. Confidence score (0-1)
"""),
                ("user", """Error: {error_type}
Occurrences: {count}
Location: {file}:{line}
Method: {method}
Context: {context}

Code:
{code_snippet}

Analyze the root cause.""")
            ])
            
            response = await self.llm.ainvoke(
                prompt.format_messages(
                    error_type=issue['error_type'],
                    count=issue['count'],
                    file=code_location['file'],
                    line=code_location['line'],
                    method=code_location['method'],
                    context=code_location['context'],
                    code_snippet=code_location['code_snippet']
                )
            )
            
            # Parse LLM response (simplified)
            return {
                'description': response.content[:200],
                'type': self._infer_issue_type(issue['error_type']),
                'impact': f"Affects {issue['count']} requests/day",
                'confidence': 0.92
            }
        else:
            # Mock response for demo
            return self._mock_root_cause_analysis(issue, code_location)
    
    def _mock_root_cause_analysis(self, issue: Dict, code_location: Dict) -> Dict:
        """Generate mock root cause analysis for demo"""
        
        analysis_map = {
            'NullPointerException': {
                'description': 'Missing null check on user.preferences before accessing theme property. When user preferences are not set, this causes NullPointerException.',
                'type': 'null_check',
                'impact': f"Affects {issue['count']} requests/day (0.02% of traffic)",
                'confidence': 0.95
            },
            'IndexOutOfBounds': {
                'description': 'Incorrect index access in batch processing. Using batch_size as index instead of valid array index.',
                'type': 'bounds_check',
                'impact': f"Affects {issue['count']} batch operations/day",
                'confidence': 0.88
            },
            'TimeoutException': {
                'description': 'Missing timeout configuration in payment API call. Long-running requests cause timeout exceptions.',
                'type': 'timeout_config',
                'impact': f"Affects {issue['count']} payment transactions/day",
                'confidence': 0.90
            }
        }
        
        return analysis_map.get(issue['error_type'], {
            'description': 'Unknown root cause',
            'type': 'unknown',
            'impact': 'Unknown impact',
            'confidence': 0.50
        })
    
    def _infer_issue_type(self, error_type: str) -> str:
        """Infer issue type from error"""
        type_map = {
            'NullPointerException': 'null_check',
            'IndexOutOfBounds': 'bounds_check',
            'TimeoutException': 'timeout_config',
            'DatabaseError': 'db_connection',
            'APIError': 'api_error'
        }
        return type_map.get(error_type, 'unknown')
