#!/usr/bin/env python3
import time
from vault.core import _xor_bytes


def run(n=200_000):
    data = b"hello" * 100
    key = b"k" * 32
    t0 = time.time()
    for _ in range(n):
        _ = _xor_bytes(data, key)
    dt = time.time() - t0
    print(f"ops={n} elapsed={dt:.3f}s")


if __name__ == "__main__":
    run()

