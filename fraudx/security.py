import re
import time
import hashlib
import hmac
import os
import ipaddress
from pathlib import Path
from typing import Optional, Dict, Tuple, List, Any
from dataclasses import dataclass, field
from functools import wraps

SAFE_HTML_TAGS = {"b", "i", "strong", "em", "br", "p", "span", "div", "ul", "li", "ol"}
SAFE_HTML_ATTRS = {"class", "style"}


def sanitize_html(text: str) -> str:
    if not text or "<" not in text:
        return text
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"javascript\s*:", "", text, flags=re.IGNORECASE)
    text = re.sub(r"on\w+\s*=\s*['\"][^'\"]*['\"]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"on\w+\s*=\s*\S+", "", text, flags=re.IGNORECASE)
    return text


def sanitize_filename(name: str) -> str:
    name = Path(name).name
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\.\.+", ".", name)
    return name[:255]


def sanitize_sql_identifier(identifier: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "", identifier)


def validate_csv(df_rows: int, file_size_bytes: int) -> Tuple[bool, str]:
    MAX_ROWS = 500000
    MAX_SIZE = 500 * 1024 * 1024
    if df_rows > MAX_ROWS:
        return False, f"Trop de lignes ({df_rows} max {MAX_ROWS})"
    if file_size_bytes > MAX_SIZE:
        return False, f"Fichier trop volumineux ({file_size_bytes/1024/1024:.0f} Mo max {MAX_SIZE/1024/1024:.0f} Mo)"
    return True, ""


def validate_transaction_amount(amount: float) -> Tuple[bool, str]:
    if amount <= 0:
        return False, "Le montant doit être positif"
    if amount > 1_000_000_000:
        return False, "Montant anormalement élevé"
    return True, ""


def validate_string_length(value: str, max_len: int = 255) -> str:
    if not value:
        return value
    return str(value)[:max_len]


class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clients: Dict[str, List[float]] = {}

    def is_allowed(self, client_key: str) -> Tuple[bool, int]:
        now = time.time()
        if client_key not in self._clients:
            self._clients[client_key] = []
        self._clients[client_key] = [t for t in self._clients[client_key] if now - t < self.window_seconds]
        if len(self._clients[client_key]) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - self._clients[client_key][0]))
            return False, retry_after
        self._clients[client_key].append(now)
        return True, 0


def hash_tx_value(value: str, salt: str = "") -> int:
    raw = f"{salt}{value}".encode()
    return int(hashlib.sha256(raw).hexdigest()[:8], 16)


def secure_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)
