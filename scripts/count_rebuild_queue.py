#!/usr/bin/env python3
"""Prints count of pending (non-# commented) lines in rebuild-queue.txt."""
import pathlib, sys

queue = pathlib.Path('docs/team/active/rebuild-queue.txt')
if not queue.exists():
    print(0)
    sys.exit(0)

pending = [l.strip() for l in queue.read_text(encoding='utf-8').splitlines()
           if l.strip() and not l.strip().startswith('#')]
print(len(pending))
