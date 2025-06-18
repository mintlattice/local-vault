from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import os
import secrets
import base64
from .storage import JsonStorage


def _xor_bytes(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("key must not be empty")
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ key[i % len(key)]
    return bytes(out)


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    # For the purpose of the toy vault, keep it simple (not for production use).
    raw = (passphrase.encode("utf-8") + salt)[:32]
    return raw.ljust(32, b"\0")


@dataclass
class Vault:
    root: Path
    passphrase: str
    salt: bytes = field(default_factory=lambda: secrets.token_bytes(8))

    def _key(self) -> bytes:
        return _derive_key(self.passphrase, self.salt)

    def _vault_path(self) -> Path:
        return self.root / ".local_vault.json"

    def _store(self) -> JsonStorage:
        return JsonStorage(self._vault_path())

    def init(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        if self._vault_path().exists():
            return
        data = {"salt": base64.b64encode(self.salt).decode("ascii"), "items": {}}
        self._store().write(data)

    def load(self) -> dict:
        doc = self._store().read()
        self.salt = base64.b64decode(doc["salt"])  # refresh salt from file
        return doc

    def save(self, doc: dict) -> None:
        doc["salt"] = base64.b64encode(self.salt).decode("ascii")
        self._store().write(doc)

    def put(self, key: str, value: str) -> None:
        doc = self.load()
        k = self._key()
        cipher = _xor_bytes(value.encode("utf-8"), k)
        doc["items"][key] = base64.b64encode(cipher).decode("ascii")
        self.save(doc)

    def get(self, key: str) -> str | None:
        doc = self.load()
        b64 = doc["items"].get(key)
        if b64 is None:
            return None
        cipher = base64.b64decode(b64)
        plain = _xor_bytes(cipher, self._key())
        return plain.decode("utf-8")

    def delete(self, key: str) -> bool:
        doc = self.load()
        if key in doc.get("items", {}):
            del doc["items"][key]
            self.save(doc)
            return True
        return False
