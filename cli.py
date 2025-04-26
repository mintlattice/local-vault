#!/usr/bin/env python3
from pathlib import Path
import argparse
from vault.core import Vault


def main() -> int:
    p = argparse.ArgumentParser("local-vault")
    p.add_argument("command", choices=["init", "put", "get", "list"]) 
    p.add_argument("key", nargs="?")
    p.add_argument("value", nargs="?")
    p.add_argument("--dir", dest="root", default=".")
    p.add_argument("--pass", dest="pw", required=True)
    args = p.parse_args()

    v = Vault(Path(args.root), args.pw)
    if args.command == "init":
        v.init()
        return 0
    v.init()
    if args.command == "put":
        if args.key is None or args.value is None:
            p.error("put requires key and value")
        v.put(args.key, args.value)
        return 0
    if args.command == "get":
        if args.key is None:
            p.error("get requires key")
        value = v.get(args.key)
        if value is None:
            print("")
        else:
            print(value)
        return 0
    if args.command == "list":
        v.init()
        doc = v.load()
        for k in sorted(doc.get("items", {}).keys()):
            print(k)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
