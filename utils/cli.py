#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path


def base_parser(description: str = "") -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--config", type=Path, default=Path("config.yaml"), help="Path to config file")
    p.add_argument("--in", dest="input_dir", type=Path, default=None, help="Input directory (if applicable)")
    p.add_argument("--out", dest="output_dir", type=Path, default=Path("out"), help="Output directory root")
    p.add_argument("--limit", type=int, default=0, help="Limit items processed (0 = no limit)")
    p.add_argument("--format", choices=["json", "ndjson"], default="json", help="Output format")
    return p
