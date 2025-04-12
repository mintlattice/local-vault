#!/usr/bin/env bash
set -euo pipefail
git log --pretty=format:'%H %ad %s' --date=iso-strict
