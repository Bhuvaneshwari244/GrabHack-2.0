"""
Mock Data Generator - Creates realistic production logs and codebase
"""
import random
from datetime import datetime, timedelta
from typing import List


def generate_mock_logs(count: int = 1000) -> List[str]:
    """Generate realistic mock production logs"""
    
    log_templates = [
        # NullPointerException logs
        "[{timestamp}] ERROR [UserService] NullPointerException at com.grab.user.UserService.getProfile(UserService.java:156)",
        "[{timestamp}] ERROR [UserService] java.lang.NullPointerException at com.grab.user.UserService.getProfile(UserService.java:156)",
        
        # IndexOutOfBounds logs
        "[{timestamp}] ERROR [ListProcessor] IndexOutOfBoundsException at com.grab.utils.ListProcessor.process_batch(ListProcessor.py:89)",
        
        # Timeout logs
        "[{timestamp}] WARN [PaymentGateway] TimeoutException in processPayment after 30s",
        "[{timestamp}] ERROR [PaymentGateway] Request timeout in processPayment",
        
        # Database errors
        "[{timestamp}] ERROR [OrderService] SQLException in getOrderHistory: Connection timeout",
        
        # API errors
        "[{timestamp}] WARN [ExternalAPI] HTTP 503 Service Unavailable endpoint: /api/v1/partners",
        "[{timestamp}] ERROR [ExternalAPI] HTTP 500 Internal Server Error endpoint: /api/v1/bookings",
        
        # Normal logs (noise)
        "[{timestamp}] INFO [Application] Request processed successfully",
        "[{timestamp}] INFO [Application] User login successful",
        "[{timestamp}] DEBUG [Cache] Cache hit for key: user_profile_12345",
        "[{timestamp}] INFO [Metrics] Response time: 45ms",
    ]
    
    logs = []
    base_time = datetime.now() - timedelta(hours=24)
    
    # Generate logs with realistic distribution
    error_weights = [
        0.05,  # NullPointer (5%)
        0.05,  # NullPointer variant
        0.02,  # IndexOutOfBounds (2%)
        0.03,  # Timeout (3%)
        0.02,  # Timeout variant
        0.01,  # Database error (1%)
        0.02,  # API 503 (2%)
        0.01,  # API 500 (1%)
        0.30,  # Normal INFO (30%)
        0.25,  # Normal INFO (25%)
        0.15,  # Normal DEBUG (15%)
        0.09,  # Normal Metrics (9%)
    ]
    
    for i in range(count):
        template = random.choices(log_templates, weights=error_weights)[0]
        timestamp = base_time + timedelta(seconds=i * 86.4)  # Spread over 24 hours
        log_line = template.format(timestamp=timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        logs.append(log_line)
    
    return logs


def generate_mock_codebase() -> dict:
    """Generate mock codebase structure"""
    
    return {
        'src/services/UserService.java': '''
package com.grab.user;

public class UserService {
    private UserRepository userRepo;
    
    public Profile getProfile(String userId) {
        User user = userRepo.findById(userId);
        // BUG: Missing null check on user.preferences
        return new Profile(user.name, user.preferences.theme);
    }
}
''',
        'src/utils/ListProcessor.py': '''
def process_batch(items, batch_size):
    """Process items in batches"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        # BUG: Incorrect index access
        result = batch[batch_size]
        yield result
''',
        'src/api/PaymentGateway.ts': '''
async function processPayment(orderId: string): Promise<PaymentResult> {
    // BUG: Missing timeout configuration
    const response = await fetch(PAYMENT_API_URL, {
        method: 'POST',
        body: JSON.stringify({ orderId })
    });
    return response.json();
}
'''
    }


def save_mock_logs(filename: str = "mock_production.log"):
    """Save mock logs to file"""
    logs = generate_mock_logs(1000)
    with open(filename, 'w') as f:
        f.write('\n'.join(logs))
    print(f"Generated {len(logs)} log entries in {filename}")


if __name__ == "__main__":
    save_mock_logs()
