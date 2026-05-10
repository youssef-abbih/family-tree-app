"""
Loads and caches family tree data from the JSON file.
"""

import json
import os
from typing import Optional

_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'family_tree.json')

# Simple in-process cache so the file is read only once per server start
_data_cache: Optional[dict] = None


def load_data() -> dict:
    """Return the full family tree dataset, loading from disk if needed."""
    global _data_cache
    if _data_cache is None:
        with open(_DATA_PATH, 'r', encoding='utf-8') as f:
            _data_cache = json.load(f)
    return _data_cache


def reload_data() -> dict:
    """Force a reload from disk (useful during development)."""
    global _data_cache
    _data_cache = None
    return load_data()
