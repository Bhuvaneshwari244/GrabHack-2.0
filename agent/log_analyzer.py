"""
Log Analyzer - Detects patterns and recurring issues in production logs
"""
import re
from collections import Counter, defaultdict
from typing import List, Dict
from datetime import datetime


class LogAnalyzer:
    """Analyzes production logs to identify recurring issues"""
    
    def __init__(self):
        self.error_patterns = {
            'NullPointerException': r'NullPointerException.*at\s+([\w\.]+)\(([\w\.]+):(\d+)\)',
            'IndexOutOfBounds': r'IndexOutOfBoundsException.*at\s+([\w\.]+)\(([\w\.]+):(\d+)\)',
            'TimeoutException': r'TimeoutException.*in\s+([\w\.]+)',
            'DatabaseError': r'SQLException.*in\s+([\w\.]+)',
            'APIError': r'HTTP\s+(\d+).*endpoint:\s+([\w\/]+)',
        }
        
    async def analyze_logs(self, logs: List[str]) -> List[Dict]:
        """Analyze logs and return prioritized list of issues"""
        
        # Extract errors from logs
        errors = self._extract_errors(logs)
        
        # Count occurrences
        error_counts = Counter(errors)
        
        # Group by type and location
        grouped_errors = self._group_errors(errors)
        
        # Prioritize issues
        issues = self._prioritize_issues(grouped_errors, error_counts)
        
        return issues[:5]  # Return top 5 issues
    
    def _extract_errors(self, logs: List[str]) -> List[tuple]:
        """Extract error information from log lines"""
        errors = []
        
        for log_line in logs:
            for error_type, pattern in self.error_patterns.items():
                match = re.search(pattern, log_line)
                if match:
                    errors.append((error_type, match.groups()))
        
        return errors
    
    def _group_errors(self, errors: List[tuple]) -> Dict:
        """Group errors by type and location"""
        grouped = defaultdict(list)
        
        for error_type, details in errors:
            key = (error_type, str(details))
            grouped[key].append(details)
        
        return grouped
    
    def _prioritize_issues(self, grouped_errors: Dict, error_counts: Counter) -> List[Dict]:
        """Prioritize issues based on frequency and severity"""
        issues = []
        
        severity_map = {
            'NullPointerException': 'HIGH',
            'IndexOutOfBounds': 'HIGH',
            'TimeoutException': 'MEDIUM',
            'DatabaseError': 'HIGH',
            'APIError': 'MEDIUM'
        }
        
        for (error_type, details_str), occurrences in grouped_errors.items():
            count = len(occurrences)
            
            # Parse location from first occurrence
            details = occurrences[0]
            if len(details) >= 2:
                location = f"{details[1]}:{details[2]}" if len(details) >= 3 else details[0]
            else:
                location = "Unknown"
            
            issues.append({
                'error_type': error_type,
                'count': count,
                'severity': severity_map.get(error_type, 'LOW'),
                'location': location,
                'sample_details': details,
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat()
            })
        
        # Sort by severity and count
        severity_order = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        issues.sort(
            key=lambda x: (severity_order[x['severity']], x['count']),
            reverse=True
        )
        
        return issues
