# app/cache.py
import hashlib
import os
import json

CACHE_DIR = "cache"

def compute_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def load_from_cache(text):
    key = compute_hash(text)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_to_cache(text, result):
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = compute_hash(text)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
