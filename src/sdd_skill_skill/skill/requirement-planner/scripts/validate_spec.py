#!/usr/bin/env python3
import sys

from sdd_skill.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["validate", *sys.argv[1:]]))
