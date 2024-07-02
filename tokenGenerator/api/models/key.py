import time


class Key:
    def __init__(self, key_id):
        self.key_id = key_id
        self.created_at = time.time()
        self.blocked_at = None
        self.keep_alive = self.created_at

    def block(self):
        self.blocked_at = time.time()

    def unblock(self):
        self.blocked_at = None

    def refresh_keep_alive(self):
        self.keep_alive = time.time()

    def is_expired(self, ttl):
        return time.time() - self.keep_alive >= ttl

    def is_blocked(self):
        return self.blocked_at is not None
