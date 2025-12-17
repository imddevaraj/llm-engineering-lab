import time


class Metrics:
    def __init__(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def latency_ms(self):
        return round((self.end_time - self.start_time) * 1000, 2)
