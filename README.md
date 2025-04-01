# Local Vault

A small solo project to manage encrypted local notes and secrets with a simple CLI. This is intentionally minimal and not meant for production.

Goals:
- Minimal dependencies
- Human-friendly vault format
- No network or server — purely local

Quickstart:
- `python cli.py init --pass secret`
- `python cli.py put api_key 123 --pass secret`
- `python cli.py get api_key --pass secret`

This repo evolves in small, realistic commits.
