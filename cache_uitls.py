import time

class SimpleCache:
    def __init__(self):
        self.store = {}
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.store:
            self.hits += 1
            return self.store[key]
        self.misses += 1
        return None

    def set(self, key, value):
        self.store[key] = value

    def stats(self):
        return {"hits": self.hits, "misses": self.misses}
