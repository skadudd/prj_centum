import time
import threading
from typing import Dict, Optional
import logging

class RateLimiter:
    """
    Rate limiter for the OpenAI API that tracks requests and tokens per minute
    to stay within Tier 3 limits for o1-mini model.
    
    Tier 3 limits for o1-mini:
    - 5,000 RPM (Requests Per Minute)
    - 4,000,000 TPM (Tokens Per Minute)
    """
    
    def __init__(self, rpm_limit: int = 5000, tpm_limit: int = 4000000):
        self.rpm_limit = rpm_limit
        self.tpm_limit = tpm_limit
        
        # Tracking requests
        self.request_timestamps = []
        self.token_counts = []
        
        # Add a lock for thread safety
        self.lock = threading.Lock()
        
        # For logging rate limit information
        self.logger = logging.getLogger(__name__)
        
        # For tracking headers from responses
        self.last_rate_limit_headers: Dict[str, str] = {}
    
    def update_from_headers(self, headers: Dict[str, str]) -> None:
        """Update rate limit information from response headers"""
        rate_limit_headers = {
            'x-ratelimit-limit-requests': headers.get('x-ratelimit-limit-requests'),
            'x-ratelimit-limit-tokens': headers.get('x-ratelimit-limit-tokens'),
            'x-ratelimit-remaining-requests': headers.get('x-ratelimit-remaining-requests'),
            'x-ratelimit-remaining-tokens': headers.get('x-ratelimit-remaining-tokens'),
            'x-ratelimit-reset-requests': headers.get('x-ratelimit-reset-requests'),
            'x-ratelimit-reset-tokens': headers.get('x-ratelimit-reset-tokens')
        }
        
        # Filter out None values
        self.last_rate_limit_headers = {k: v for k, v in rate_limit_headers.items() if v is not None}
        
        # Log the current rate limit status
        if 'x-ratelimit-remaining-requests' in self.last_rate_limit_headers:
            self.logger.info(
                f"Rate limit status: {self.last_rate_limit_headers.get('x-ratelimit-remaining-requests')} "
                f"requests and {self.last_rate_limit_headers.get('x-ratelimit-remaining-tokens')} tokens remaining"
            )
    
    def _clean_old_entries(self) -> None:
        """Remove entries older than 1 minute"""
        current_time = time.time()
        one_minute_ago = current_time - 60
        
        # Clean request timestamps
        self.request_timestamps = [t for t in self.request_timestamps if t > one_minute_ago]
        
        # Clean token counts
        self.token_counts = [entry for entry in self.token_counts 
                           if entry['timestamp'] > one_minute_ago]
    
    def check_and_wait(self, estimated_tokens: int) -> float:
        """
        Check if we're within rate limits and wait if necessary.
        Returns the time spent waiting in seconds.
        """
        with self.lock:
            self._clean_old_entries()
            
            current_time = time.time()
            current_rpm = len(self.request_timestamps)
            current_tpm = sum(entry['count'] for entry in self.token_counts)
            
            # Determine how long to wait
            wait_time = 0
            
            # Check RPM limit
            if current_rpm >= self.rpm_limit:
                # Find the oldest timestamp within the last minute
                oldest_timestamp = min(self.request_timestamps)
                # Calculate how long until it's outside the 1-minute window
                rpm_wait = (oldest_timestamp + 60) - current_time
                wait_time = max(wait_time, rpm_wait)
            
            # Check TPM limit with the estimated tokens for the new request
            if current_tpm + estimated_tokens >= self.tpm_limit:
                # Find how long until enough tokens fall outside the window
                tokens_to_free = (current_tpm + estimated_tokens) - self.tpm_limit
                
                # Sort token entries by timestamp
                sorted_entries = sorted(self.token_counts, key=lambda x: x['timestamp'])
                
                tokens_freed = 0
                for entry in sorted_entries:
                    tokens_freed += entry['count']
                    if tokens_freed >= tokens_to_free:
                        # Calculate wait time based on this entry
                        tpm_wait = (entry['timestamp'] + 60) - current_time
                        wait_time = max(wait_time, tpm_wait)
                        break
            
            # Add jitter to prevent thundering herd
            if wait_time > 0:
                wait_time *= 1.1  # Add 10% buffer
            
            # Log if we need to wait
            if wait_time > 0:
                self.logger.warning(
                    f"Rate limit approaching: Current RPM={current_rpm}/{self.rpm_limit}, "
                    f"TPM={current_tpm}/{self.tpm_limit}. Waiting {wait_time:.2f}s"
                )
            
            return wait_time
    
    def record_request(self, token_count: int) -> None:
        """Record a request and its token usage"""
        with self.lock:
            current_time = time.time()
            self.request_timestamps.append(current_time)
            self.token_counts.append({
                'timestamp': current_time,
                'count': token_count
            })
    
    async def wait_if_needed(self, estimated_tokens: int) -> None:
        """Async wrapper to wait if rate limits are approaching"""
        import asyncio
        
        wait_time = self.check_and_wait(estimated_tokens)
        if wait_time > 0:
            await asyncio.sleep(wait_time)
    
    def get_current_usage(self) -> Dict[str, int]:
        """Get current usage stats"""
        with self.lock:
            self._clean_old_entries()
            return {
                'rpm': len(self.request_timestamps),
                'tpm': sum(entry['count'] for entry in self.token_counts)
            }
    
    def estimate_tokens(self, text: str) -> int:
        """Very rough token count estimation (4 chars per token)"""
        if text is None:
            return 0
        return len(text) // 4 + 1  # Simple estimation