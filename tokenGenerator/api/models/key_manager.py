import uuid
import threading
import random
from .key import Key
import time

# In seconds
DELETE_DURATION = 300
UNBLOCK_DURATION = 60


class KeyManager:
    def __init__(self):
        self.keys = {}  # key_id -> Key instance
        self.available_keys = set()
        self.blocked_keys = set()
        self.lock = threading.Lock()

    def generate_key(self):
        key_id = str(uuid.uuid4())
        key = Key(key_id)
        with self.lock:
            self.keys[key_id] = key
            self.available_keys.add(key_id)

        # Set a timer to delete the key after expiry time
        # if not kept alive
        threading.Timer(DELETE_DURATION, self._delete_key, [key_id]).start()
        return key_id

    def get_key(self):
        with self.lock:
            if not self.available_keys:
                return None

            key_id = random.choice(list(self.available_keys))
            self.available_keys.remove(key_id)
            self.blocked_keys.add(key_id)
            key = self.keys[key_id]
            key.block()

            # Set a timer to unblock the key after unblock duration
            # if not explicitly done
            threading.Timer(UNBLOCK_DURATION, self.unblock_key, [key_id]).start()
            return key_id

    def unblock_key(self, key_id):
        with self.lock:
            if key_id in self.blocked_keys:
                self.blocked_keys.remove(key_id)
                self.available_keys.add(key_id)
                key = self.keys[key_id]
                key.unblock()

    # delete_key -> Delete the key instantly
    # Used by DELETE `/keys/id/`
    def delete_key(self, key_id):
        with self.lock:
            if key_id in self.keys:
                self.available_keys.discard(key_id)
                self.blocked_keys.discard(key_id)
                del self.keys[key_id]

    def keep_alive(self, key_id):
        with self.lock:
            if key_id in self.keys:
                key = self.keys[key_id]
                key.refresh_keep_alive()

                threading.Timer(
                    DELETE_DURATION, self._delete_key, [key_id]
                ).start()

    def get_key_info(self, key_id):
        with self.lock:
            key = self.keys.get(key_id)
            if key:
                blocked_at = time.ctime(key.blocked_at) if key.blocked_at is not None else "not blocked"
                created_at = time.ctime(key.created_at)
                return {
                    "isBlocked": key.is_blocked(),
                    "blockedAt": blocked_at,
                    "createdAt": created_at,
                }

            return None

    # _delete_key -> Delete the key incase the key is expired
    # Used by Timer
    def _delete_key(self, key_id):
        with self.lock:
            key = self.keys.get(key_id)
            if key and key.is_expired(DELETE_DURATION):
                self.delete_key(key_id)


key_manager = KeyManager()
