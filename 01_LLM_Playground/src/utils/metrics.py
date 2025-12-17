import time
import tiktoken
import json
from datetime import datetime
from typing import Optional, Dict, Any

class Metrics:
    def __init__(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def latency_ms(self):
        return round((self.end_time - self.start_time) * 1000, 2)