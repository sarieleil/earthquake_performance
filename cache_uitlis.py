class SimpleCache:
    def __init__(self):
        self.store = {}
        self.hits = 0
        self.misses = 0

    def set(self, key, value):
        self.store[key] = value

    def get(self, key):
        if key in self.store:
            self.hits += 1
            return self.store[key]
        self.misses += 1
        return None

    def __contains__(self, key):
        return key in self.store
