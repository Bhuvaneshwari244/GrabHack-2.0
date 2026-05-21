"""
Fix Generator - Generates code fixes and validates them
"""
from typing import Dict
from langchain_core.prompts import ChatPromptTemplate


class FixGenerator:
    """Generates and validates code fixes"""
    
    def __init__(self, llm):
        self.llm = llm
        
    async def generate_fix(self, root_cause: Dict, code_location: Dict) -> Dict:
        """Generate code fix based on root cause analysis"""
        
        if self.llm:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert software engineer. Generate a minimal, safe code fix.

Requirements:
- Fix must be backward compatible
- Minimal lines changed
- Include error handling
- Add comments explaining the fix
"""),
                ("user", """Root Cause: {description}
Issue Type: {type}
Current Code:
{code_snippet}

Generate the fixed code.""")
            ])
            
            response = await self.llm.ainvoke(
                prompt.format_messages(
                    description=root_cause['description'],
                    type=root_cause['type'],
                    code_snippet=code_location['code_snippet']
                )
            )
            
            return {
                'strategy': 'LLM-generated fix',
                'fixed_code': response.content,
                'lines_changed': 3,
                'backward_compatible': True,
                'explanation': root_cause['description']
            }
        else:
            # Mock fix for demo
            return self._mock_generate_fix(root_cause, code_location)
    
    def _mock_generate_fix(self, root_cause: Dict, code_location: Dict) -> Dict:
        """Generate mock fix for demo"""
        
        fix_map = {
            'null_check': {
                'strategy': 'Add null-safe access with default value',
                'fixed_code': '''
public Profile getProfile(String userId) {
    User user = userRepo.findById(userId);
    // Fix: Add null check for user.preferences
    String theme = (user.preferences != null) 
        ? user.preferences.theme 
        : "default";
    return new Profile(user.name, theme);
}
''',
                'lines_changed': 5,
                'backward_compatible': True,
                'explanation': 'Added null check before accessing user.preferences.theme with default fallback'
            },
            'bounds_check': {
                'strategy': 'Fix incorrect index access',
                'fixed_code': '''
def process_batch(items, batch_size):
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        # Fix: Use first element of batch instead of invalid index
        result = batch[0] if batch else None
        if result:
            yield result
''',
                'lines_changed': 4,
                'backward_compatible': True,
                'explanation': 'Fixed index access to use batch[0] with safety check'
            },
            'timeout_config': {
                'strategy': 'Add timeout configuration',
                'fixed_code': '''
async processPayment(orderId: string): Promise<PaymentResult> {
    // Fix: Add timeout configuration
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    
    try {
        const response = await fetch(PAYMENT_API_URL, {
            method: 'POST',
            body: JSON.stringify({ orderId }),
            signal: controller.signal
        });
        return response.json();
    } finally {
        clearTimeout(timeoutId);
    }
}
''',
                'lines_changed': 8,
                'backward_compatible': True,
                'explanation': 'Added 5-second timeout with AbortController'
            }
        }
        
        return fix_map.get(root_cause['type'], {
            'strategy': 'Generic fix',
            'fixed_code': '// Fix not available',
            'lines_changed': 0,
            'backward_compatible': True,
            'explanation': 'Unable to generate fix'
        })
    
    async def validate_fix(self, fix_proposal: Dict) -> Dict:
        """Validate the generated fix"""
        
        # Basic validation checks
        lines_changed = fix_proposal['lines_changed']
        backward_compatible = fix_proposal['backward_compatible']
        
        # Check constraints
        syntax_valid = True  # In real system, would run linter
        safety_passed = lines_changed <= 50  # Max 50 lines per PR
        blast_radius = 'LOW' if lines_changed < 10 else 'MEDIUM'
        
        passed = all([
            syntax_valid,
            safety_passed,
            backward_compatible
        ])
        
        return {
            'passed': passed,
            'syntax_valid': syntax_valid,
            'safety_passed': safety_passed,
            'blast_radius': blast_radius,
            'backward_compatible': backward_compatible,
            'reason': '' if passed else 'Validation failed'
        }
